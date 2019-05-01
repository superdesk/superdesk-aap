# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import json
from superdesk.tests import TestCase
from apps.publish import init_app
from .aap_newsroom_ninjs_formatter import AAPNewsroomNinjsFormatter


class AAPNINJSFormatterTest(TestCase):
    def setUp(self):
        self.formatter = AAPNewsroomNinjsFormatter()
        init_app(self.app)
        self.maxDiff = None
        self.app.data.insert('vocabularies', [
            {
                "_id": "locators",
                "display_name": "Locators",
                "type": "unmanageable",
                "unique_field": "qcode",
                "items": [
                    {"is_active": True, "name": "NSW", "qcode": "NSW", "state": "New South Wales",
                     "country": "Australia", "world_region": "Oceania", "group": "Australia"},
                ],
            },
            {
                "_id": "crop_sizes",
                "display_name": "Image Crop Sizes",
                "type": "manageable",
                "items": [
                    {
                        "width": 800,
                        "is_active": True,
                        "height": 600,
                        "name": "4-3"
                    },
                    {
                        "width": 1280,
                        "is_active": True,
                        "height": 720,
                        "name": "16-9"
                    }
                ],
                "unique_field": "name",
                "selection_type": "do not show"
            }
        ])

    def test_associated_media_formatter(self):
        article = {
            "_id": "urn:newsml:localhost:2017-08-31T11:40:29.408059:fd448b37-f35d-4bb2-a565-2433dcf1c338",
            "dateline": {
                "source": "AAP",
                "text": "MILTON KEYNES, Aug 31 AAP -",
                "date": "2017-08-31T01:40:29.000Z",
                "located": {
                    "tz": "Europe/London",
                    "city_code": "Milton Keynes",
                    "country": "United Kingdom",
                    "city": "Milton Keynes",
                    "dateline": "city",
                    "state": "England",
                    "alt_name": "",
                    "country_code": "GB",
                    "state_code": "GB.ENG"
                }
            },
            "pubstatus": "usable",
            "profile": "58cf62e01d41c8208dc20375",
            "flags": {
                "marked_archived_only": False,
                "marked_for_sms": False,
                "marked_for_not_publication": False,
                "marked_for_legal": False
            },
            "version_creator": "57bcfc5d1d41c82e8401dcc0",
            "version": 1,
            "state": "in_progress",
            "event_id": "tag:localhost:2017:39642f28-ebb6-4767-863e-58ac9e5810fd",
            "unique_name": "#32467",
            "operation": "update",
            "versioncreated": "2017-08-31T01:44:24.000Z",
            "_created": "2017-08-31T01:40:29.000Z",
            "type": "text",
            "format": "HTML",
            "family_id": "urn:newsml:localhost:2017-08-31T11:40:29.408059:fd448b37-f35d-4bb2-a565-2433dcf1c338",
            "_current_version": 2,
            "sign_off": "MAR",
            "priority": 6,
            "firstcreated": "2017-08-31T01:40:29.000Z",
            "source": "AAP",
            "original_creator": "57bcfc5d1d41c82e8401dcc0",
            "language": "en",
            "unique_id": 32467,
            "guid": "urn:newsml:localhost:2017-08-31T11:40:29.408059:fd448b37-f35d-4bb2-a565-2433dcf1c338",
            "anpa_category": [
                {
                    "qcode": "i",
                    "scheme": None,
                    "name": "International News"
                }
            ],
            "place": [
                {
                    "name": "NSW",
                    "country": "Australia",
                    "group": "Australia",
                    "qcode": "NSW",
                    "state": "New South Wales",
                    "world_region": "Oceania"
                }
            ],
            "urgency": 3,
            "genre": [
                {
                    "qcode": "Article",
                    "name": "Article"
                }
            ],
            "slugline": "Article Slugline",
            "anpa_take_key": "takekey",
            "ednote": "Article ed note",
            "byline": "Article Byline",
            "subject": [
                {
                    "qcode": "01000000",
                    "name": "arts, culture and entertainment",
                }
            ],
            "abstract": "<p>“Article abstract“</p>",
            "sms_message": "",
            "headline": "‘Article Headline’",
            "word_count": 2,
            "body_html": "<p>“Article Body“</p>",
        }

        seq, doc = self.formatter.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        expected = {"guid": "urn:newsml:localhost:2017-08-31T11:40:29.408059:fd448b37-f35d-4bb2-a565-2433dcf1c338",
                    "headline": "'Article Headline'", "description_text": "\"Article abstract\"", "language": "en",
                    "located": "Milton Keynes",
                    "ednote": "Article ed note", "source": "AAP", "firstcreated": "2017-08-31T01:40:29.000Z",
                    "description_html": "<p>\"Article abstract\"</p>", "byline": "Article Byline", "charcount": 14,
                    "body_html": "<p>\"Article Body\"</p>", "slugline": "Article Slugline",
                    "subject": [{"name": "arts, culture and entertainment", "code": "01000000"}],
                    "versioncreated": "2017-08-31T01:44:24.000Z", "wordcount": 2,
                    "service": [{"name": "International News", "code": "i"}], "type": "text", "version": "2",
                    "genre": [{"name": "Article", "code": "Article"}], "priority": 6, "urgency": 3,
                    "readtime": 0,
                    "profile": "58cf62e01d41c8208dc20375", "place": [{"name": "New South Wales", "code": "NSW"}],
                    "pubstatus": "usable", "products": []}
        self.assertEqual(expected, json.loads(doc))
