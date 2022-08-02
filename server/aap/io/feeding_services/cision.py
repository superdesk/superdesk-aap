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
from copy import deepcopy
from superdesk.io.registry import register_feeding_service
from superdesk.io.feeding_services.http_base_service import HTTPFeedingServiceBase
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE
from superdesk.utc import utcnow
from superdesk.io.iptc import subject_codes
from superdesk.text_utils import get_text
from superdesk.emails import send_email
from flask import current_app as app, render_template


logger = logging.getLogger(__name__)


class CisionFeedingService(HTTPFeedingServiceBase):

    NAME = "Cision"

    label = "Cision API"

    fields = HTTPFeedingServiceBase.AUTH_FIELDS + [
        {
            "id": "login_api_url",
            "type": "text",
            "label": "Cision Login URL",
            "required": True,
        },
        {
            "id": "releases_api_url",
            "type": "text",
            "label": "Cision Releases URL",
            "required": True,
        },
        {"id": "token", "type": "text", "label": "token", "readonly": True},
        {"id": "token_expiry", "type": "text", "label": "token expiry", "readonly": True},
        {"id": "kill_email", "type": "text", "label": "Kill notification email"}
    ]

    session = None

    subject_map = {
        "ACC": "04016001",  # Accounting News, Issues
        "TNM": "04016005",  # Acquisitions, Mergers, Takeovers
        "ANW": "08001000",  # Animal Welfare
        "PET": "08001000",  # Animals/Pets
        "ATY": "02003002",  # Attorney/Lawsuit Investigations
        "AWD": "08006000",  # Awards
        "BCY": "04016007",  # Bankruptcy
        "CHI": "14024001",  # Children-Related News
        "TRI": "07005000",  # Clinical Trials/Medical Discoveries
        "RCY": "06002000",  # Conservation/Recycling
        "CON": "04016013",  # Contracts
        "CXP": "04016022",  # Corporate Expansion
        # "CSR": "",  #Corporate Social Responsibility
        # "DEI": "",  #Diversity, Equity Inclusion
        "DIV": "04016015",  # Dividends
        # "POL": "",  #Domestic Policy
        "ERN": "04016018",  # Earnings
        "ERP": "04016016",  # Earnings Projects or Forecasts
        "ECO": "04017000",  # Economic News, Trends and Analysis
        "ENI": "06000000",  # Environmental Issues
        "ENP": "06000000",  # Environmental Policy
        "ESG": "06000000",  # Environmental, Social, and Governance
        # "EGV": "",  #European Government
        # "FDA": "",  #FDA Approval
        # "FEA": "",  #Features
        # "LEG": "",  #Federal and State Legislation
        # "EXE": "",  #Federal Executive Branch, Agency News
        # "FNC": "",  #Financing Agreements
        "FOR": "11002002",  # Foreign policy/International affairs
        # "FVT": "",  #Future Events
        "DIS": "14004000",  # Handicapped/Disabled
        # "HSP": "",  #Hispanic-Oriented News
        # "IMA": "",  #International Medical Approval
        # "INO": "",  #Investments Opinions
        "JVN": "04016023",  # Joint Ventures
        "LBR": "09010000",  # Labor/Union news
        # "LAW": "",  #Legal Issues
        "LGB": "14010001",  # Lesbian/Gay/Bisexual
        "LIC": "04016026",  # Licensing/Marketing Agreements
        "MRR": "04006008",  # Market Research Reports
        # "MAT": "",  #Mature Audience
        # "MAV": "",  #Media Advisory/Invitation
        # "MIN": "",  #Mens Interest
        # "ADM": "",  #MultiVu Audio
        # "PHM": "",  #MultiVu Photo
        # "VDM": "",  #MultiVu Video
        # "NTA": "",  #Native American
        "NAT": "03015001",  # Natural Disasters
        "PDT": "04016030",  # New Products/Services
        # "NPT": "",  #Not for Profit
        # "OBI": "",  #Obituaries
        # "OFR": "",  #Offerings
        # "DSC": "",  #Oil/Gas Discoveries
        "PLW": "04016031",  # Patent Law
        # "PER": "",  #Personnel Announcements
        "CPN": "11003002",  # Political Campaigns
        # "PVP": "",  #Private Placement
        "RCL": "04016053",  # Product Recalls
        # "PSF": "",  #Public Safety
        "RLE": "04004003",  # Real Estate Transactions
        "REL": "12000000",  # Religion
        "RCN": "04016039",  # Restructuring/Recapitalizations
        # "SLS": "",  #Sales Reports
        "SCZ": "14024005",  # Senior Citizens
        # "SHA": "",  #Shareholder Activism
        # "SHM": "",  #Shareholder Meeting
        # "SRP": "",  #Shareholders' Rights Plans
        # "SBS": "",  #Small Business Services
        # "SRI": "",  #Socially Responsible Investing
        "STS": "04016051",  # Stock Split
        "SVY": "11003008",  # Surveys, Polls & Research
        "TRD": "04008033",  # Trade Policy
        # "TDS": "",  #Tradeshow News
        # "STP": "",  #U.S. State Policy News
        # "VEN": "",  #Venture Capital
        "VET": "11001001",  # Veterans
        # "VNR": "",  #Video News Releases
        # "WOM": "",  #Women-related News
    }

    def _valid_token(self, provider):
        try:
            if not provider.get("config", {}).get("token"):
                return False

            if utcnow() < arrow.get(provider.get("config", {}).get("token_expiry"), "YYYYMMDDTHHmmss").datetime:
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
            headers={"X-Client": provider.get("config", {}).get("username"),
                     "User-Agent": "AustralianAssociatedPress"},
            timeout=self.HTTP_TIMEOUT
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
        locator_map = {m['geocode']: m['qcode'] for m in
                       superdesk.get_resource_service('vocabularies').find_one(req=None,
                                                                               _id='prnnewswire_location_map').get(
                           "items", [])}
        locators = {m['qcode']: m for m in
                    superdesk.get_resource_service('vocabularies').find_one(req=None, _id='locators').get("items", [])}
        cleaner = lxml_html.clean.Cleaner(
            scripts=True,
            javascript=True,
            style=True,
            embedded=False,
            comments=True,
            add_nofollow=True,
            kill_tags=["style", "script"],
            safe_attrs=["alt", "src", "rel", "href", "target", "title"],
        )

        if not self.session:
            self.session = requests.Session()

        if not self._valid_token(provider):
            r = self._login(provider)

            auth_details = json.loads(r.text)
            provider["config"]["token"] = auth_details.get("auth_token")
            provider["config"]["token_expiry"] = auth_details.get("expires")
            # save the token
            superdesk.get_resource_service('ingest_providers').system_update(provider[config.ID_FIELD],
                                                                             updates={'config': provider["config"]},
                                                                             original=provider)

        start_date = (
            provider.get("last_item_update").strftime("%Y%m%dT%H%M%S%z")
            if provider.get("last_item_update")
            else (datetime.utcnow() - timedelta(days=1)).strftime("%Y%m%dT%H%M%S+0000")
        )

        headers = {"Authorization": "Bearer " + provider.get("config", {}).get("token"),
                   "X-Client": provider.get("config", {}).get("username"), "User-Agent": "AustralianAssociatedPress"}
        try:
            r = self.session.get(
                url=self.provider.get("config", {}).get("releases_api_url"),
                headers=headers,
                params={"mod_startdate": start_date, "mod_enddate": datetime.utcnow().strftime("%Y%m%dT%H%M%S+0000"),
                        "fields": "title|date|release_id|company|summary|dateline", "show_del": "true"},
                timeout=self.HTTP_TIMEOUT
            )
            r.raise_for_status()
        # on any exception clear the token to start fresh next time
        except Exception as exc:
            provider["config"]["token"] = None
            provider["config"]["token_expiry"] = None
            superdesk.get_resource_service('ingest_providers').system_update(provider[config.ID_FIELD],
                                                                             updates={'config': provider["config"]},
                                                                             original=provider)
            logger.exception(exc)
            return []

        releases = json.loads(r.text)
        items = []
        for entry in releases.get("data", []):
            # Set version in suffix and version in item, it will be preserved in the ninjs output.
            item = {ITEM_TYPE: CONTENT_TYPE.TEXT, "guid": "cision{}:1".format(entry.get("release_id")), "version": "1"}

            try:
                if entry.get("status") == "DELETED":
                    kill_item = superdesk.get_resource_service('archive').find_one(req=None,
                                                                                   ingest_id="cision{}".format(
                                                                                       entry.get("release_id")))
                    if kill_item:
                        updates = {"auto_publish": True, "headline": entry.get("title", ""),
                                   "body_html": entry.get("summary", ""), "abstract": entry.get("title", "")}
                        superdesk.get_resource_service('archive_unpublish').patch(id=kill_item[config.ID_FIELD],
                                                                                  updates=updates)
                    else:
                        logger.warning("Failed to locate {} to kill it".format(entry.get("release_id")))
                    if provider["config"].get("kill_email"):
                        data = deepcopy(entry)
                        data['warning'] = "Warning Kill not published for story" if kill_item is None else None
                        html_body = render_template("cision_delete_email.html", **data)
                        data['summary'] = get_text(data.get('summary', ''), content="html")
                        text_body = render_template("cision_delete_email.txt", **data)
                        send_email(subject="CISION: {}".format(entry.get("title")),
                                   sender=app.config["ADMINS"][0],
                                   recipients=[r.strip() for r in provider["config"]["kill_email"].split(";") if
                                               r.strip()],
                                   html_body=html_body,
                                   text_body=text_body
                                   )
                    continue
            except Exception as exc:
                logger.exception(exc)
                continue

            logger.info("Requesting {}".format(entry.get("url")))
            r = self.session.get(url=entry.get('url'), headers=headers)
            try:
                r.raise_for_status()
            except Exception as exc:
                logger.exception(exc)
                continue
            release = json.loads(r.text)
            data = release.get("data", {})
            item["uri"] = entry.get("url")
            item['slugline'] = 'PRNewswire'

            div_start = "<div>"
            div_end = "</div>"
            item['body_html'] = cleaner.clean_html(div_start + data.get("body") + div_end)[len(div_start):-len(div_end)]

            DATELINE_SOURCE = " /PRNewswire/ --"
            if DATELINE_SOURCE in entry.get("summary", ""):
                abstract = entry.get("dateline", "") + DATELINE_SOURCE + \
                    get_text(entry.get("summary", ""), content="html").split(DATELINE_SOURCE, 1)[1]
            elif DATELINE_SOURCE in item['body_html']:
                abstract = entry.get("dateline", "") + DATELINE_SOURCE + \
                    get_text(item['body_html'], content="html").split(DATELINE_SOURCE, 1)[1]
            else:
                abstract = html.unescape(data.get("title"))

            item["abstract"] = '<p>' + (abstract if len(abstract) <= 450 else
                                        textwrap.wrap(abstract, 447)[0] + "...") + '</p>'

            item['headline'] = html.unescape(data.get("title"))
            item['anpa_category'] = [{'qcode': 'j'}]
            item['original_source'] = 'PRNewswire'

            item["firstcreated"] = datetime.strptime(data.get("date"), "%Y%m%dT%H%M%S%z")
            item["created"] = datetime.strptime(data.get("date"), "%Y%m%dT%H%M%S%z")
            item["versioncreated"] = datetime.strptime(data.get("date"), "%Y%m%dT%H%M%S%z")

            item["place"] = []
            for geo in data.get("geography"):
                if locator_map.get(geo):
                    item["place"].append(locators.get(locator_map.get(geo)))

            # source_company
            item['anpa_take_key'] = data.get("source_company")

            # subject
            for subject in data.get("subject"):
                if self.subject_map.get(subject):
                    if item.get("subject") is None:
                        item['subject'] = []
                    item['subject'].append(
                        {'qcode': self.subject_map.get(subject), 'name': subject_codes[self.subject_map.get(subject)]})

            if data.get("multimedia") and len(data.get("multimedia")):
                item['extra'] = {"multimedia": data.get('multimedia')}

            items.append(item)

        if self .session:
            self.session.close()

        return [items]


register_feeding_service(CisionFeedingService)
