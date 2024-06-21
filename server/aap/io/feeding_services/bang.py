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

import lxml.etree
import requests

from superdesk.errors import AlreadyExistsError
from superdesk.io.feeding_services.http_base_service import HTTPFeedingServiceBase
from superdesk.io.registry import register_feeding_service

MUSIC_ID = "music_url"
MOVIES_ID = "movies_url"
SHOWBIZ_ID = "showbiz_url"

logger = logging.getLogger(__name__)


class BangFeedingService(HTTPFeedingServiceBase):
    NAME = "Bang"

    label = "Bang Showbiz"

    HTTP_AUTH = False

    session = None

    # configuration fields for the source url's
    fields = [
        {
            "id": MUSIC_ID,
            "type": "text",
            "label": "Music URL",
        },
        {
            "id": MOVIES_ID,
            "type": "text",
            "label": "Movies URL",
        },
        {
            "id": SHOWBIZ_ID,
            "type": "text",
            "label": "Showbiz URL",
        },
    ]

    @staticmethod
    def _config_test(provider=None):
        return True

    def _update(self, provider, update):
        if not self.session:
            self.session = requests.Session()

        parser = self.get_feed_parser(provider)

        items = []
        for src in self.fields:
            current_url = provider.get("config").get(src.get("id"))
            if current_url:
                feed_items = None
                provider["current_id"] = src.get("id")
                try:
                    r = self.session.get(current_url)
                    r.raise_for_status()

                    # Set the parser to be more tolerant due to stray quotes we get in attributes at times
                    xml_parser = lxml.etree.XMLParser(recover=True)
                    xml = lxml.etree.fromstring(r.content, xml_parser)
                    feed_items = parser.parse(xml, provider=provider)
                except lxml.etree.XMLSyntaxError:
                    logger.exception(f"Syntax error parsing {current_url}")
                # Anything goes wrong we log it and swallow it, so one bad feed doesn't kill them all!
                except Exception:
                    logger.exception(f"Processing url {current_url}")

                if feed_items:
                    items.append(feed_items)

        if self.session:
            self.session.close()

        return items


try:
    register_feeding_service(BangFeedingService)
except AlreadyExistsError:
    pass
