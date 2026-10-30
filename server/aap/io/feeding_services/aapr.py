# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
import requests
import json
import arrow
import superdesk
import html
import textwrap
import lxml.html as lxml_html
from eve.utils import config
from datetime import datetime, timedelta
from superdesk.io.registry import register_feeding_service
from superdesk.io.feeding_services.http_base_service import HTTPFeedingServiceBase
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE
from superdesk.utc import utcnow


logger = logging.getLogger(__name__)


class AAPRFeedingService(HTTPFeedingServiceBase):
    NAME = "AAPR"

    label = "AAPR API"

    fields = HTTPFeedingServiceBase.AUTH_FIELDS + [
        {
            "id": "login_api_url",
            "type": "text",
            "label": "AAPR Login URL",
            "required": True,
        },
        {
            "id": "releases_api_url",
            "type": "text",
            "label": "AAPR Releases URL",
            "required": True,
        },
        {
            "id": "releases_public_url",
            "type": "text",
            "label": "AAPR Public URL",
            "required": True,
        },
        {"id": "token", "type": "text", "label": "token", "readonly": True},
        {
            "id": "token_expiry",
            "type": "text",
            "label": "token expiry",
            "readonly": True,
        },
        # {"id": "kill_email", "type": "text", "label": "Kill notification email"},
        # {"id": "last_deleted_release_id", "type": "text",
        #  "label": "Id of the last processed deleted release", "readonly": True},
        {
            "id": "last_release_id",
            "type": "text",
            "label": "Id of the last processed release",
            "readonly": True,
        },
    ]

    session = None

    def _valid_token(self, provider):
        try:
            if not provider.get("config", {}).get("token"):
                return False

            if (
                utcnow()
                < arrow.get(
                    provider.get("config", {}).get("token_expiry"), "YYYYMMDDTHHmmss"
                ).datetime
            ):
                return True
        except Exception as ex:
            logger.exception(ex)
        return False

    def _login(self, provider):
        r = self.session.post(
            url=provider.get("config", {}).get("login_api_url"),
            json={
                "login": provider.get("config", {}).get("username"),
                "pwd": provider.get("config", {}).get("password"),
            },
            headers={
                "X-Client": provider.get("config", {}).get("username"),
                "User-Agent": "AustralianAssociatedPress",
            },
            timeout=self.HTTP_TIMEOUT,
        )
        r.raise_for_status()
        return r

    def config_test(self, provider=None):
        """
        Ensure that the credentials and at least the login URL are OK
        :param provider:
        :return:
        """
        if not self.session:
            self.session = requests.Session()
        self._login(provider)
        self.session.close()

    def _update(self, provider, update):
        self.provider = provider
        provider["config"]["auth_required"] = False

        cleaner = lxml_html.clean.Cleaner(
            scripts=True,
            javascript=True,
            style=True,
            embedded=False,
            comments=True,
            add_nofollow=True,
            kill_tags=["style", "script"],
            safe_attrs=[
                "alt",
                "src",
                "rel",
                "href",
                "target",
                "title",
                "height",
                "width",
                "frameborder",
                "scrolling",
                "loading",
            ],
        )

        if not self.session:
            self.session = requests.Session()

        if not self._valid_token(provider):
            r = self._login(provider)

            auth_details = json.loads(r.text)
            provider["config"]["token"] = auth_details.get("auth_token")
            provider["config"]["token_expiry"] = auth_details.get("expires")
            # save the token
            superdesk.get_resource_service("ingest_providers").system_update(
                provider[config.ID_FIELD],
                updates={"config": provider["config"]},
                original=provider,
            )

        start_date = (
            provider.get("last_item_update").strftime("%Y%m%dT%H%M%S%z")
            if provider.get("last_item_update")
            else (datetime.utcnow() - timedelta(days=1)).strftime("%Y%m%dT%H%M%S+0000")
        )

        headers = {
            "Authorization": "Bearer " + provider.get("config", {}).get("token"),
            "X-Client": provider.get("config", {}).get("username"),
            "User-Agent": "AustralianAssociatedPress",
        }

        try:
            r = self.session.get(
                url=self.provider.get("config", {}).get("releases_api_url"),
                headers=headers,
                params={
                    "mod_startdate": start_date,
                    "mod_enddate": datetime.utcnow().strftime("%Y%m%dT%H%M%S+0000"),
                    "fields": "title|date|release_id|company|summary|dateline",
                    "show_del": "true",
                },
                timeout=self.HTTP_TIMEOUT,
            )
            r.raise_for_status()
        # on any exception clear the token to start fresh next time
        except Exception as exc:
            provider["config"]["token"] = None
            provider["config"]["token_expiry"] = None
            superdesk.get_resource_service("ingest_providers").system_update(
                provider[config.ID_FIELD],
                updates={"config": provider["config"]},
                original=provider,
            )
            logger.exception(exc)
            return []

        releases = json.loads(r.text)

        items = []

        # sort the entries so most recent is last and we ingest them in order
        entrys = sorted(releases.get("data", []), key=lambda d: d["date"])
        for entry in entrys:
            # Set version in suffix and version in item, it will be preserved in the ninjs output.
            item = {
                ITEM_TYPE: CONTENT_TYPE.TEXT,
                "guid": "AAPR{}:1".format(entry.get("release_id")),
                "version": "1",
            }

            # ignore it if we got it last time
            if provider.get("config", {}).get("last_release_id") == entry.get(
                "release_id"
            ):
                continue

            logger.info("Requesting {}".format(entry.get("url")))
            r = self.session.get(url=entry.get("url"), headers=headers)
            try:
                r.raise_for_status()
            except Exception as exc:
                logger.exception(exc)
                continue
            release = json.loads(r.text)

            data = release.get("data", {})
            item["uri"] = entry.get("url")
            item["slugline"] = "AAPR"

            # appending attachments at bottom of body with download links
            attachmentsHTML = "<br><h3>Attachments</h3>"
            if data.get("multimedia") and len(data.get("multimedia")):
                attachments = data.get("multimedia")
                for attachment in attachments:
                    # Check if attachment is an image file and display it
                    if "image/" in attachment.get("mimetype"):
                        attachmentsHTML += '<img src="%s" alt="%s"><br>' % (
                            attachment.get("href", ""),
                            attachment.get("description", ""),
                        )

                    # Attach download link for each attachment
                    attachmentsHTML += (
                        '<a>Download</a><a href="%s" download> %s</a><br>'
                        % (attachment.get("href", ""), (attachment.get("name", "")))
                    )
            else:
                # Ensure no attachments heading is added if nothing is attached
                attachmentsHTML = ""

            # Construct a link to the original content source at the bottom of the body using ID
            publicLink = provider["config"]["releases_public_url"] + (
                "%s/index.html" % data.get("release_id")
            )

            attachmentsHTML += (
                '<br><p>View the original content: <a href="%s">%s</a></p>'
                % (publicLink, publicLink)
            )

            div_start = "<div>"
            div_end = "</div>"

            # Add the body text followed by the "Attachments" heading then the attachments for display and downloading
            bodyHTML = cleaner.clean_html(
                div_start + data.get("body") + attachmentsHTML + div_end
            )[len(div_start) : -len(div_end)]

            item["body_html"] = bodyHTML

            abstract = entry.get("summary", "")

            item["abstract"] = (
                "<p>"
                + (
                    abstract
                    if len(abstract) <= 450
                    else textwrap.wrap(abstract, 447)[0] + "..."
                )
                + "</p>"
            )

            item["headline"] = html.unescape(data.get("title"))
            item["anpa_category"] = [{"qcode": "j"}]
            item["original_source"] = "AAPR"

            item["firstcreated"] = datetime.strptime(
                data.get("date"), "%Y%m%dT%H%M%S%z"
            )
            item["created"] = datetime.strptime(data.get("date"), "%Y%m%dT%H%M%S%z")
            item["versioncreated"] = datetime.strptime(
                data.get("date"), "%Y%m%dT%H%M%S%z"
            )

            item["place"] = []

            # source_company
            item["anpa_take_key"] = data.get("source_company")

            # Assigning thumbnail from provided attachments if possible
            if data.get("multimedia") and len(data.get("multimedia")):
                attachments = data.get("multimedia")
                thumbnailIndex: int = -1
                smallestImageSize: int = -1
                for i, attachment in enumerate(attachments):
                    # Check if attachment is an image file
                    if "image/" in attachment.get("mimetype"):
                        # Check if description flags this as intended thumbnail
                        if "thumbnail" in attachment.get("description").lower():
                            thumbnailIndex = i
                            break

                        # Track smallest image if none are flagged as thumbnail
                        imageSize = attachment.get("size", smallestImageSize)

                        # If this is first image type, set smallest image size to be able to compare
                        if smallestImageSize == -1:
                            smallestImageSize = imageSize
                            thumbnailIndex = i
                        # Otherwise compare to find the smallest image for the thumbnail
                        elif imageSize < smallestImageSize:
                            smallestImageSize = imageSize
                            thumbnailIndex = i

                # Move thumbnail to front of array
                if thumbnailIndex != -1:
                    attachments.insert(0, attachments.pop(thumbnailIndex))
                    # Set href to new thumbnailurl key
                    attachments[0]["thumbnailurl"] = attachments[0].get("href", "")
                    # Set type to "photo" for Photos to recognise thumbnail
                    attachments[0]["type"] = "photo"

                item["extra"] = {"multimedia": attachments}

            items.append(item)

        if self.session:
            self.session.close()

        if len(entrys) and provider.get("config", {}).get("last_release_id") != entrys[
            -1
        ].get("release_id"):
            provider["config"]["last_release_id"] = entrys[-1].get("release_id")
            superdesk.get_resource_service("ingest_providers").system_update(
                provider[config.ID_FIELD],
                updates={"config": provider["config"]},
                original=provider,
            )

        return [items]


register_feeding_service(AAPRFeedingService)
