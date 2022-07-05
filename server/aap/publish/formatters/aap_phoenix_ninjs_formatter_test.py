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
from .aap_phoenix_ninjs_formatter import PhoenixNINJSFormatter


class AAPNINJSFormatterTest(TestCase):
    def setUp(self):
        self.formatter = PhoenixNINJSFormatter()
        init_app(self.app)
        self.maxDiff = None

    def test_phoenix_composit(self):
        article = {
            "_id": "urn:newsml:localhost:2021-09-19T15:11:22.186979:d6231590-a36e-40c0-8826-ea277427eab2",
            "genre": [
                {
                    "qcode": "Article",
                    "name": "Article"
                }
            ],
            "place": [
                {
                    "state": "New South Wales",
                    "country": "Australia",
                    "qcode": "NSW",
                    "name": "NSW",
                    "world_region": "Oceania",
                    "group": "Australia"
                }
            ],
            "format": "HTML",
            "byline": "The Great Unwashed",
            "family_id": "urn:newsml:localhost:2021-09-19T15:11:22.186979:d6231590-a36e-40c0-8826-ea277427eab2",
            "pubstatus": "usable",
            "source": "AAP",
            "sign_off": "MAR",
            "guid": "urn:newsml:localhost:2021-09-19T15:11:22.186979:d6231590-a36e-40c0-8826-ea277427eab2",
            "priority": 6,
            "groups": [
                {
                    "refs": [
                        {
                            "idRef": "main"
                        },
                        {
                            "idRef": "fact box"
                        }
                    ],
                    "id": "root",
                    "role": "grpRole:NEP"
                },
                {
                    "refs": [
                        {
                            "_current_version": 2,
                            "residRef": "urn:newsml:localhost:2021-09-07T16:34:24.155686:c2e98892-04e5-4be6-80bd-"
                                        "4472e6d13a6b",
                            "guid": "urn:newsml:localhost:2021-09-07T16:34:24.155686:c2e98892-04e5-4be6-80bd-"
                                    "4472e6d13a6b",
                            "itemClass": "icls:text",
                            "location": "archive",
                            "headline": "TEST 5",
                            "type": "text",
                            "slugline": "TEST 5",
                            "renditions": {}
                        },
                        {
                            "_current_version": 2,
                            "residRef": "urn:newsml:localhost:2021-09-07T18:08:16.007933:a69f6efd-2376-4dcd-9bff-"
                                        "16c434b07a52",
                            "guid": "urn:newsml:localhost:2021-09-07T18:08:16.007933:a69f6efd-2376-4dcd-9bff-"
                                    "16c434b07a52",
                            "itemClass": "icls:text",
                            "location": "archive",
                            "headline": "TEST 6",
                            "type": "text",
                            "slugline": "TEST 6",
                            "renditions": {}
                        }
                    ],
                    "role": "grpRole:main",
                    "id": "main"
                },
                {
                    "refs": [
                        {
                            "_current_version": 2,
                            "residRef": "urn:newsml:localhost:2021-09-07T16:28:56.706126:d0036019-a485-4dd2-82fb-"
                                        "2a2236502f80",
                            "guid": "urn:newsml:localhost:2021-09-07T16:28:56.706126:d0036019-a485-4dd2-82fb-"
                                    "2a2236502f80",
                            "itemClass": "icls:text",
                            "location": "archive",
                            "headline": "TEST 4",
                            "type": "text",
                            "slugline": "TEST 4",
                            "renditions": {}
                        }
                    ],
                    "role": "grpRole:fact box",
                    "id": "fact box"
                }
            ],
            "language": "en",
            "unique_id": 41204,
            "urgency": 3,
            "event_id": "tag:localhost:2021:64872ba1-6d0b-4589-89e4-3122cc5a2b7c",
            "operation": "publish",
            "type": "composite",
            "slugline": "Package 2",
            "extra": {
                "package_description": "<p>This is a package decription</p>",
                "package_fact_box_description": "<p>Main section blurb</p>"
            },
            "_current_version": 3,
            "state": "published",
            "version": 1,
            "headline": "Test package 2",
            "unique_name": "#41204",
            "original_creator": "57bcfc5d1d41c82e8401dcc0",
            "subject": [
                {
                    "qcode": "01000000",
                    "name": "arts, culture and entertainment"
                }
            ],
            "anpa_category": [
                {
                    "qcode": "a",
                    "name": "Australian General News"
                }
            ]
        }
        seq, doc = self.formatter.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        formatted = json.loads(doc)
        self.assertEqual(formatted['original_item'], 'urn:newsml:localhost:2021-09-19T15:11:22.186979:d6231590'
                                                     '-a36e-40c0-8826-ea277427eab2')
        self.assertEqual(formatted['sections'][0]['items'][0]['html'], '<p>This is a package decription</p>')
        self.assertEqual(formatted['sections'][1]['items'][0]['guid'], 'urn:newsml:localhost:2021-09-07T16:34:24.'
                                                                       '155686:c2e98892-04e5-4be6-80bd-4472e6d13a6b')

    def test_phoenix_sms(self):
        article = {
            "_id": "urn:newsml:localhost:2021-10-14T10:55:34.438044:e00641f4-a8dc-4a1c-ba19-a8c5f3ec0e85",
            "_current_version": 1,
            "urgency": 3,
            "guid": "urn:newsml:localhost:2021-10-14T10:55:34.438044:e00641f4-a8dc-4a1c-ba19-a8c5f3ec0e85",
            "genre": [
                {
                    "qcode": "Article",
                    "name": "Article"
                }
            ],
            "type": "text",
            "state": "in_progress",
            "flags": {
                "marked_for_sms": True,
            },
            "format": "HTML",
            "dateline": {
                "located": {
                    "city_code": "Wagga Wagga",
                    "alt_name": "",
                    "state_code": "NSW",
                    "dateline": "city",
                    "state": "New South Wales",
                    "city": "Wagga Wagga",
                    "tz": "Australia/Sydney",
                    "country": "Australia",
                    "country_code": "AU"
                },
                "text": "WAGGA WAGGA, Oct 14 AAP -",
                "date": "2021-10-13T23:55:34.000Z",
                "source": "AAP"
            },
            "family_id": "urn:newsml:localhost:2021-10-14T10:55:34.438044:e00641f4-a8dc-4a1c-ba19-a8c5f3ec0e85",
            "firstcreated": "2021-10-13T23:55:34.000Z",
            "unique_name": "#41269",
            "version_creator": "57bcfc5d1d41c82e8401dcc0",
            "version": 1,
            "operation": "update",
            "_created": "2021-10-13T23:55:34.000Z",
            "source": "AAP",
            "event_id": "tag:localhost:2021:9bf87f1d-da05-4469-9c5c-09870e5e513f",
            "_updated": "2021-10-13T23:55:54.000Z",
            "language": "en",
            "place": [
                {
                    "group": "Australia",
                    "name": "NSW",
                    "qcode": "NSW",
                    "state": "New South Wales",
                    "country": "Australia",
                    "world_region": "Oceania"
                }
            ],
            "byline": "The Great Unwashed",
            "priority": 6,
            "sign_off": "MAR",
            "pubstatus": "usable",
            "sms_message": "test sms message"
        }
        seq, doc = self.formatter.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        formatted = json.loads(doc)
        self.assertEqual(formatted['sms_message'], 'test sms message')
