# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import datetime
import json
import logging
import urllib
from io import BytesIO

import urllib3
from eve.io.base import DataLayer
from eve_elastic.elastic import ElasticCursor
from flask import url_for
import pytz
from PIL import Image, ImageOps

from superdesk.errors import SuperdeskApiError
from superdesk.io.iptc import subject_codes
from superdesk.media.media_operations import process_file_from_stream
from superdesk.media.renditions import (
    generate_renditions,
    delete_file_on_error,
    get_renditions_spec,
)
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, PUB_STATUS
from superdesk.utc import utcnow
from titlecase import titlecase
from superdesk import get_resource_service
from typing import Any

urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class AAPMMDatalayer(DataLayer):
    def __set_auth_cookie(self, app: Any) -> bool:
        try:
            if self._username is not None and self._password is not None:
                url = app.config["AAP_MM_SEARCH_URL"] + "/Users/login"
                values = {"username": self._username, "password": self._password}
                r = self._http.urlopen(
                    "POST",
                    url,
                    headers={"Content-Type": "application/json"},
                    body=json.dumps(values),
                )
            else:
                url = app.config["AAP_MM_SEARCH_URL"] + "/Users/AnonymousToken"
                r = self._http.request("GET", url, redirect=False)
        except Exception as ex:
            logger.exception(ex)
            r = None
        finally:
            # If the login failed then do not set the headers
            if r and not r.status // 100 in {4, 5}:
                self._headers = {
                    "cookie": r.getheader("set-cookie"),
                    "Content-Type": "application/json",
                }
                self._login_tries = 0
                return True
            else:
                self._login_tries += 1
                return False

    def set_credentials(self, username: str, password: str) -> None:
        if (
            username
            and username != self._username
            and password
            and password != self._password
        ):
            self._username = username
            self._password = password
            self.__set_auth_cookie(self._app)

    def init_app(self, app: Any) -> None:
        self._app = app
        self._headers = None
        self._login_tries = 0
        self._username = None
        self._password = None
        self._http = urllib3.PoolManager()

    def _set_byline(self, out_doc: dict, in_doc: dict) -> None:
        """
        Set the byline for the image as follows :-
        Photos that are credit AAP get the byline set to that real byline suffixed with AAP PHOTOS, for photos from
        other sources just get the credit suffixed with PHOTO

        :param out_doc:
        :param in_doc:
        :return:
        """
        if in_doc.get("Credit", "").upper().startswith("AAP"):
            type_str = "AAP VIDEO" if in_doc["AssetType"] == "VIDEO" else "AAP PHOTOS"
            out_doc["byline"] = (
                titlecase(in_doc.get("Byline", "")) + "/" + type_str
                if in_doc.get("Byline")
                else type_str
            )
            if (
                in_doc.get("Source", "").upper().startswith("SUPPLIED")
                and in_doc["AssetType"] == "VIDEO"
            ):
                out_doc["byline"] = "SUPPLIED/" + in_doc.get("Byline", "")
        elif in_doc.get("Credit", "").upper().startswith("PR HANDOUT"):
            out_doc["byline"] = "HANDOUT/" + in_doc.get("Source", "")
        elif (
            in_doc.get("Credit", "").upper().startswith("SUPPLIED")
            and in_doc["AssetType"] == "VIDEO"
        ):
            out_doc["byline"] = "SUPPLIED/" + in_doc.get("Byline", "")
        else:
            out_doc["byline"] = in_doc.get("Credit", "").upper() + " PHOTO"

    def find(self, resource, req, lookup):
        """
        Called to execute a search against the AAP Mulitmedia API. It attempts to translate the search request
        passed in req to a suitable form for a search request against the API. It parses the response into a
        suitable ElasticCursor, the front end will never know.
        :param resource:
        :param req:
        :param lookup:
        :return:
        """
        if self._headers is None:
            if not self.__set_auth_cookie(self._app):
                raise SuperdeskApiError.internalError(
                    "Unable to log into the image archive"
                )

        url = self._app.config["AAP_MM_SEARCH_URL"] + "/Assets/search"
        query_keywords = "*"
        if "query" in req.get("query", {}).get("filtered", ""):
            query_keywords = req["query"]["filtered"]["query"]["query_string"]["query"]
            query_keywords = query_keywords.replace("slugline:", "objectname:")
            query_keywords = query_keywords.replace(
                "description_text:", "captionabstract:"
            )

        fields = {}
        query_filter = req.get("query", {}).get("bool", {}).get("filter", [])
        for criterion in query_filter:
            term = criterion.get("term")
            if term:
                if "type" in term:
                    fields["MediaTypes"] = [
                        self.map_types(key, False) for key in json.loads(term["type"])
                    ]
                elif "creditqcode" in term:
                    credits = json.loads(term["creditqcode"])
                    credit_values = [
                        k.get("value") for k in credits if k and "value" in k
                    ]
                    if credit_values:
                        fields["Credits"] = credit_values
                elif "category" in term:
                    categories = json.loads(term["category"])
                    cat_list = []
                    for cat in categories:
                        q_codes = [
                            code
                            for code, value in subject_codes.items()
                            if value == cat
                        ]
                        cat_list.extend(q_codes or [cat])
                    fields["Categories"] = cat_list

        for criterion in req.get("post_filter", {}).get("and", {}):
            # parse out the date range if possible
            if "range" in criterion:
                start = None
                end = None
                daterange = None
                if "firstcreated" in criterion.get("range", {}):
                    if "gte" in criterion["range"]["firstcreated"]:
                        start = criterion["range"]["firstcreated"]["gte"][0:10]
                    if "lte" in criterion["range"]["firstcreated"]:
                        end = criterion["range"]["firstcreated"]["lte"][0:10]
                # if there is a special start and no end it's one of the date buttons
                if start and not end:
                    if start == "now-24H":
                        daterange = {"Dates": ["[NOW/HOUR-24HOURS TO NOW]"]}
                    if start == "now-1w" or start == "now-7d":
                        daterange = {"Dates": ["[NOW/DAY-7DAYS TO NOW/DAY]"]}
                    if start == "now-30d":
                        daterange = {"Dates": ["[NOW/DAY-1MONTH TO NOW/DAY]"]}
                # we've got something but no daterange set above
                if (start or end) and not daterange:
                    daterange = {
                        "DateRange": [{"Start": start, "End": end}],
                        "DateCreatedFilter": "true",
                    }
                if daterange:
                    fields.update(daterange)

            if "terms" in criterion:
                if "type" in criterion.get("terms", {}):
                    fields.update(
                        {
                            "MediaTypes": [
                                self.map_types(key, False)
                                for key in criterion["terms"]["type"]
                            ]
                        }
                    )
                if "credit" in criterion.get("terms", {}):
                    fields.update({"Credits": criterion["terms"]["credit"]})
                if "anpa_category.name" in criterion.get("terms", {}):
                    cat_list = []
                    for cat in criterion["terms"]["anpa_category.name"]:
                        qcode = [
                            key for key, value in subject_codes.items() if value == cat
                        ]
                        if qcode:
                            for code in qcode:
                                cat_list.append(code)
                        else:
                            cat_list.append(cat)
                    fields.update({"Categories": cat_list})

        if (
            req.get("sort")
            and len(req.get("sort"))
            and list(req.get("sort")[0].items())[0][0] == "firstcreated"
        ):
            fields.update({"SortBy": list(req.get("sort")[0].items())[0][1]})

        size = int(req.get("size", "25")) if int(req.get("size", "25")) > 0 else 25
        query = {
            "Query": query_keywords,
            "pageSize": str(size),
            "pageNumber": str(int(req.get("from", "0")) // size + 1),
        }
        try:
            r = self._http.urlopen(
                "POST",
                url + "?" + urllib.parse.urlencode(query),
                body=json.dumps(fields),
                headers=self._headers,
            )
        except Exception as ex:
            logger.exception(ex)
            r = None
        finally:
            # if the response is unathorized or an error or exception try again a few times
            if not r or r.status // 100 in {4, 5}:
                if self._login_tries < 3:
                    self._headers = None
                    return self.find(resource, req, lookup)
                else:
                    SuperdeskApiError.internalError(
                        "Unable to access the image archive"
                    )

        hits = self._parse_hits(json.loads(r.data.decode("UTF-8")))
        return ElasticCursor(
            docs=hits["docs"],
            hits={"hits": hits, "aggregations": self._parse_aggregations(hits)},
        )

    def _get_dimension(self, value):
        try:
            return int(value)
        except ValueError:
            return None

    def _parse_doc(self, doc: dict):
        new_doc = {
            "_id": doc["AssetId"],
            "guid": doc["AssetId"],
            "headline": doc["Title"],
            "description_text": doc["Description"],
            "archive_description": doc["Description"],
            "source": doc["Credit"],
        }
        if "Source" in doc:
            new_doc["original_source"] = (
                doc["Credit"] + "/" + str(doc.get("Source", ""))
            )
        else:
            new_doc["original_source"] = doc["Credit"]
        new_doc["versioncreated"] = self._datetime(doc["CreationDate"])
        new_doc["firstcreated"] = self._datetime(doc["CreationDate"])
        new_doc["pubstatus"] = "usable"
        # This must match the action
        new_doc["_type"] = "externalsource"
        # entry that the client can use to identify the fetch endpoint
        new_doc["fetch_endpoint"] = "search_providers_proxy"
        new_doc[ITEM_TYPE] = self.map_types(doc["AssetType"].lower())
        if doc["AssetType"] == "VIDEO":
            new_doc["state"] = "draft"
            try:
                purl = doc.get("Preview", {})[0].get("Href", "")
            except IndexError:
                logger.info(f"Missing preview for {doc['AssetId']}")
                new_doc["pubstatus"] = PUB_STATUS.HOLD
                new_doc["_fetchable"] = False
                purl = ""
            new_doc["renditions"] = {
                "original": {"href": purl, "mimetype": "video/mp4"},
                "thumbnail": {"href": doc.get("Layout", {}).get("Href")},
            }
        else:
            height = self._get_dimension(doc.get("OriginalImageHeight"))
            width = self._get_dimension(doc.get("OriginalImageWidth"))

            new_doc["renditions"] = {
                "viewImage": {"href": doc.get("Preview", doc.get("Layout"))["Href"]},
                "thumbnail": {"href": doc.get("Thumbnail", doc.get("Layout"))["Href"]},
                "original": {"href": doc.get("Preview", doc.get("Layout"))["Href"]},
                "baseImage": {"href": doc.get("Preview", doc.get("Layout"))["Href"]},
            }
            new_doc["pubstatus"] = PUB_STATUS.USABLE
            new_doc["state"] = "draft"
            if height and width:
                new_doc["renditions"]["original"]["height"] = height
                new_doc["renditions"]["original"]["width"] = width
                # The resolution of the image needs to be at least as large as the biggest crop
                crops = get_resource_service("vocabularies").find_one(
                    req=None, _id="crop_sizes"
                )
                if crops:
                    for crop in crops.get("items"):
                        if height < crop.get("height") or width < crop.get("width"):
                            new_doc["pubstatus"] = PUB_STATUS.HOLD
                            new_doc["_fetchable"] = False
                            break
        new_doc["slugline"] = doc["Title"]
        self._set_byline(new_doc, doc)
        new_doc["ednote"] = doc["SpecialInstructions"]
        doc.clear()
        doc.update(new_doc)

    def _parse_hits(self, hits):
        hits["docs"] = hits.pop("Assets")
        hits["total"] = hits.pop("Total")
        for doc in hits["docs"]:
            self._parse_doc(doc)
        return hits

    def _parse_aggregation(self, aggregations, facet, aggregation, hits):
        """
        Converts the "facet" to the "aggregate" based on the FacetResults in hits returns the equivalent
        aggregation in aggregations
        :param aggregations:
        :param facet:
        :param aggregation:
        :param hits:
        :return:
        """
        if "FacetResults" in hits and facet in hits.get("FacetResults", {}):
            buckets = []
            name_set = set()
            for cat in hits.get("FacetResults", {}).get(facet, {}):
                if cat["DisplayName"] in name_set:
                    buckets.append(
                        {
                            "doc_count": cat["Count"],
                            "key": cat["DisplayName"] + "/" + cat["Name"],
                            "qcode": cat["Name"],
                        }
                    )

                elif facet == "MediaTypes":
                    buckets.append(
                        {
                            "doc_count": cat["Count"],
                            "key": self.map_types(cat["DisplayName"].lower()),
                            "qcode": cat["Name"],
                        }
                    )
                    name_set.add(cat["DisplayName"])
                else:
                    buckets.append(
                        {
                            "doc_count": cat["Count"],
                            "key": cat["DisplayName"],
                            "qcode": cat["Name"],
                        }
                    )
                    name_set.add(cat["DisplayName"])
            aggregations[aggregation] = {"buckets": buckets}

    def _parse_aggregation_dates(self, aggregations, hits):
        """
        Extract the date related facets and convert into aggregations
        :param aggregations:
        :param hits:
        :return:
        """
        if "FacetResults" in hits and "Dates" in hits.get("FacetResults", {}):
            for date in hits.get("FacetResults", {}).get("Dates", {}):
                if date["Name"] == "[NOW/HOUR-24HOURS TO NOW/HOUR]":
                    aggregations["day"] = {
                        "buckets": [{"doc_count": date["Count"], "key": date["Name"]}]
                    }
                if date["Name"] == "[NOW/DAY-7DAYS TO NOW/DAY]":
                    aggregations["week"] = {
                        "buckets": [{"doc_count": date["Count"], "key": date["Name"]}]
                    }
                if date["Name"] == "[NOW/DAY-1MONTH TO NOW/DAY]":
                    aggregations["month"] = {
                        "buckets": [{"doc_count": date["Count"], "key": date["Name"]}]
                    }

    def _parse_aggregations(self, hits):
        """
        Given the hits returned from the AAP Mulitmedia API it will convert them to the same format as the
        Aggregations returned from the superdesk search against Elastic
        :param hits:
        :return: The converted aggregations
        """
        aggregations = {}
        self._parse_aggregation(aggregations, "Categories", "category", hits)
        self._parse_aggregation(aggregations, "MediaTypes", "type", hits)
        self._parse_aggregation(aggregations, "Credits", "credit", hits)
        self._parse_aggregation_dates(aggregations, hits)
        hits.pop("FacetResults")
        return aggregations

    def _datetime(self, string):
        try:
            dt = datetime.datetime.strptime(
                string[0:19] + string[19:25].replace(":", ""), "%Y-%m-%dT%H:%M:%S%z"
            ).astimezone(pytz.utc)
        except BaseException:
            dt = utcnow()
        return dt

    def _get_resolutions(self, id):
        url = self._app.config["AAP_MM_SEARCH_URL"] + "/Assets/Resolutions"
        values = [id]
        headers = dict(self._headers)
        headers["Content-Type"] = "application/json"
        r = self._http.urlopen("POST", url, headers=headers, body=json.dumps(values))
        return json.loads(r.data.decode("UTF-8"))

    def find_all(self, resource, max_results=1000):
        raise NotImplementedError

    def find_one(self, resource, req, **lookup):
        raise NotImplementedError

    def find_one_raw(self, resource, _id):
        if self._headers is None:
            self.__set_auth_cookie(self._app)

        url = self._app.config["AAP_MM_SEARCH_URL"] + "/Assets/{}".format(_id)
        r = self._http.request("GET", url, headers=self._headers)
        doc = json.loads(r.data.decode("UTF-8"))
        self._parse_doc(doc)
        if "fetch_endpoint" in doc:
            del doc["fetch_endpoint"]

        # Only if we have credentials can we download the original if the account has that privilege
        if self._username is not None and self._password is not None:
            resolutions = self._get_resolutions(_id)
            if doc[ITEM_TYPE] == CONTENT_TYPE.PICTURE:
                if any(i["Name"] == "Original" for i in resolutions["Image"]):
                    url = self._app.config[
                        "AAP_MM_SEARCH_URL"
                    ] + "/Assets/{}/Original/download".format(_id)
                    mime_type = "image/jpeg"
                else:
                    raise FileNotFoundError
            elif doc[ITEM_TYPE] == CONTENT_TYPE.VIDEO:
                if any(v["Name"] == "Original" for v in resolutions["Video"]):
                    url = self._app.config[
                        "AAP_MM_SEARCH_URL"
                    ] + "/Assets/{}/Original/download".format(_id)
                    mime_type = doc.get("renditions").get("original").get("mimetype")
                else:
                    raise FileNotFoundError
            else:
                raise NotImplementedError
        else:
            if doc[ITEM_TYPE] == CONTENT_TYPE.VIDEO:
                mime_type = doc.get("renditions").get("original").get("mimetype")
            else:
                mime_type = "image/jpeg"
            url = doc["renditions"]["original"]["href"]

        r = self._http.request("GET", url, headers=self._headers)
        out = BytesIO(r.data)

        file_name, content_type, metadata = process_file_from_stream(out, mime_type)

        # fix the orientation if the image is rotated
        if doc[ITEM_TYPE] == CONTENT_TYPE.PICTURE and metadata.get("orientation") in [
            "3",
            "6",
            "8",
        ]:
            out = self._fixorientation(out, content_type)

        inserted = []

        # Save the url of the thubnail for the video
        video_thumbnail_url = (
            doc["renditions"]["thumbnail"]["href"]
            if doc[ITEM_TYPE] == CONTENT_TYPE.VIDEO
            else False
        )

        try:
            logger.debug("Going to save media file with %s " % file_name)
            out.seek(0)
            file_id = self._app.media.put(
                out, filename=file_name, content_type=content_type, metadata=None
            )
            doc["mimetype"] = content_type
            # set the version created to now to bring it to the top of the desk, images can be quite old
            doc["versioncreated"] = utcnow()
            inserted = [file_id]
            file_type = content_type.split("/")[0]
            rendition_spec = get_renditions_spec(no_custom_crops=True)

            renditions = generate_renditions(
                out,
                file_id,
                inserted,
                file_type,
                content_type,
                rendition_spec,
                self.url_for_media,
                insert_metadata=False,
            )
            doc["renditions"] = renditions

            thumb_id = None
            if video_thumbnail_url:
                thumbnail_request = self._http.request("GET", video_thumbnail_url)
                thumb_out = BytesIO(thumbnail_request.data)
                thumb_name, thumb_type, thumb_metadata = process_file_from_stream(
                    thumb_out, "image/jpeg"
                )
                thumb_out.seek(0)
                thumb_id = self._app.media.put(
                    thumb_out,
                    filename=thumb_name,
                    content_type=thumb_type,
                    metadata=None,
                )
                thumb_url = self.url_for_media(thumb_id, thumb_type)

                doc["renditions"].update(
                    {
                        "thumbnail": {
                            "href": thumb_url,
                            "media": thumb_id,
                            "mimetype": thumb_type,
                        }
                    }
                )
        except Exception as io:
            logger.exception(io)
            for file_id in inserted:
                delete_file_on_error(doc, file_id)
            if thumb_id:
                self._app.media.delete(thumb_id)

            raise SuperdeskApiError.internalError("Generating renditions failed")

        return doc

    def url_for_media(self, media_id, mimetype=None):
        return url_for(
            "upload_raw.get_upload_as_data_uri",
            media_id=media_id,
            _external=True,
            _scheme=self._app.config["URL_PROTOCOL"],
        )

    def _fixorientation(self, file_stream: BytesIO, content_type: str) -> BytesIO:
        """
        Given an image filestream with a none up-right orientation transpose it to correct the orientation
        :param file_stream:
        :return: stream
        """
        file_stream.seek(0)
        try:
            file_type, ext = content_type.split("/")
            img = Image.open(file_stream)
            img2 = ImageOps.exif_transpose(img)
            out_stream = BytesIO()
            img2.save(out_stream, ext)
            out_stream.seek(0)
            return out_stream
        except Exception as e:
            logger.exception(e)
            file_stream.seek(0)
            return file_stream

    def map_types(self, key, to_superdesk=True):
        """

        :param key:
        :param to_superdesk:
        :return:
        """
        aap_to_superdesk = {
            "image": "picture",
            "video": "video",
            "audio": "audio",
            "graphics": "graphic",
            "interactive": "interactive",
        }

        superdesk_to_aap = dict(reversed(item) for item in aap_to_superdesk.items())

        return (
            aap_to_superdesk.get(key, "Unknown")
            if to_superdesk
            else superdesk_to_aap.get(key, "Unknown")
        )
