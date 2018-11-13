# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.tests import TestCase
from apps.publish import init_app
from .marketplace_ninjs_formatter import MarketplaceNINJSFormatter
from datetime import datetime
import json


def ISODate(dt):
    datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.000+0000")


class TestMarketplaceNINJS(TestCase):
    ingest = [{
        "_id": "urn:newsml:localhost:2018-11-09T03:01:27.558606:2a806251-790c-4615-944f-7856f0d417a3",
        "slugline": "Technology Xiaomi",
        "ingest_provider": "5615d77f069b7f774d66003a",
        "family_id": "urn:newsml:localhost:2018-11-09T03:01:27.558606:2a806251-790c-4615-944f-7856f0d417a3",
        "versioncreated": ISODate("2018-11-08T16:00:00.000+0000"),
        "type": "text",
        "state": "ingested",
        "headline": "XIAOMI LAUNCHES IN THE UK AS NEWEST PHONE RIVAL TO APPLE AND SAMSUNG",
        "uri": "19f5b765-e160-4661-a8bb-b7f0a86a5107HHH-3-1",
        "source": "PAA",
        "ingest_provider_sequence": "3142",
        "archived": ISODate("2018-11-08T16:01:27.000+0000"),
        "guid": "19f5b765-e160-4661-a8bb-b7f0a86a5107HHH-3-1"
    }, {
        "_id": "urn:newsml:localhost:2018-11-08T06:28:29.851340:47ebdba0-bcfa-4fe4-bad7-a186136ed937",
        "ingest_provider": "563181f8069b7f7e6664283a",
        "guid": "tag:reuters.com,2018:newsml_MT1VRT1203021832:184620126",
        "versioncreated": "2018-11-07T19:22:06.000+0000",
        "type": "text",
        "uri": "tag:reuters.com,2018:newsml_MT1VRT1203021832",
        "source": "Reuters",
        "_etag": "3bde3bbd03ff58cedc4114cec9a9dfb2f397c264",
        "version": "184620126",
        "ingest_provider_sequence": "2693",
    }, {
        "_id": "urn:newsml:localhost:2018-11-11T07:16:29.400128:0288d720-f095-4835-86a4-6826af71361f",
        "slugline": "US-MED--FishOil-Vitam",
        "guid": "tag:localhost:2018:861146a6-9a01-48bc-8fb4-7757c7f236af",
        "anpa_take_key": "",
        "_created": ISODate("2018-11-10T20:16:29.000+0000"),
        "headline": "Big studies give mixed news on fish oil, vitamin D"
    }, {
        "_id": "urn:newsml:localhost:2018-11-11T07:16:29.908105:d326a058-fa9b-4855-a579-a587e822d1fd",
        "slugline": "US-MED--FishOil-Vitam",
        "guid": "tag:localhost:2018:0f9827dd-00b7-4a60-acea-02f319315206",
        "anpa_take_key": "1stLd-Writethru",
        "_created": ISODate("2018-11-10T20:16:29.000+0000"),
        "headline": "Big studies give mixed news on fish oil, vitamin D"
    }
    ]

    article = [{
        "_id": "5be33cdec08c285b2e89967f",
        "slugline": "VARIETY-ENTERTAINMENT-FILM/NEWS",
        "event_id": "tag:localhost:2018:51e14b77-0fd9-465a-a107-26750023ed80",
        "urgency": 3,
        "guid": "tag:localhost:2018:9a1b49b0-9026-4215-9a46-fb760fead170",
        "publish_sequence_no": 3587288,
        "subject": [
            {
                "name": "arts, culture and entertainment",
                "qcode": "01000000"
            },
            {
                "name": "cinema",
                "qcode": "01005000"
            },
            {
                "name": "television",
                "qcode": "01016000"
            }
        ],
        "version_creator": None,
        "priority": 3,
        "queue_state": "queued",
        "anpa_category": [
            {
                "name": "Entertainment",
                "qcode": "e"
            }
        ],
        "schedule_settings": {
            "utc_publish_schedule": None,
            "time_zone": None,
            "utc_embargo": None
        },
        "language": "en",
        "pubstatus": "usable",
        "place": [

        ],
        "type": "text",
        "byline": "Brent Lang",
        "unique_name": "#34049135",
        "state": "published",
        "headline": "Fox Quarterly Earnings Climb as Disney Deal Looms",
        "archive_description": "VARIETY-ENTERTAINMENT-FILM/NEWS:Fox Quarterly Earnings Climb as Disney Deal Looms",
        "genre": [
            {
                "name": "Article",
                "scheme": None,
                "qcode": "Article"
            }
        ],
        "source": "Reuters",
        "renditions": {

        },
        "publish_schedule": None,
        "is_take_item": False,
        "version": "184620126",
        "ingest_provider": "563181f8069b7f7e6664283a",
        "family_id": "urn:newsml:localhost:2018-11-08T06:28:29.851340:47ebdba0-bcfa-4fe4-bad7-a186136ed937",
        "body_html": "<p>Body</p>",
        "description_text": "VARIETY-ENTERTAINMENT-FILM/NEWS:Fox Quarterly Earnings Climb as Disney Deal Looms",
        "firstcreated": ISODate("2018-11-07T13:22:31.000+0000"),
        "profile": "58b788bd069b7f6953927e9d",
        "moved_to_legal": True,
        "_current_version": 2,
        "last_published_version": True,
        "target_subscribers": [
            {
                "name": "System - Bulletin Builder Database (TEST)",
                "scheme": None,
                "_id": "5721524fca6a9346e8aab767"
            }
        ],
        "authors": [

        ],
        "ingest_provider_sequence": "2693",
        "operation": "publish",
        "ednote": "",
        "original_creator": "",
        "_created": ISODate("2018-11-07T19:28:30.000+0000"),
        "word_count": 379,
        "item_id": "tag:localhost:2018:9a1b49b0-9026-4215-9a46-fb760fead170",
        "expiry": ISODate("2018-11-10T19:28:30.000+0000"),
        "usageterms": "ANY",
        "format": "HTML",
        "_etag": "8e9c1ae70e046d6df9f50544b9e9a8a54a961e01",
        "_updated": ISODate("2018-11-07T19:28:33.000+0000"),
        "versioncreated": ISODate("2018-11-07T19:28:30.000+0000"),
        "ingest_id": "urn:newsml:localhost:2018-11-08T06:28:29.851340:47ebdba0-bcfa-4fe4-bad7-a186136ed937",
        "firstpublished": ISODate("2018-11-07T19:28:30.000+0000"),
        "unique_id": 34049135,
        "auto_publish": True,
        "last_queue_event": ISODate("2018-11-07T19:28:30.000+0000")
    }, {
        "_id": "5be45dd7c08c285b2e89af3b",
        "slugline": "Technology Xiaomi",
        "event_id": "tag:localhost:2018:538f349f-2951-4072-80ff-e54641c54b6b",
        "urgency": 4,
        "guid": "tag:localhost:2018:68c56cfa-205b-4861-91bd-907423e3471b",
        "publish_sequence_no": 3590314,
        "subject": [
            {
                "name": "economy, business and finance",
                "qcode": "04000000"
            },
            {
                "name": "computing and information technology",
                "qcode": "04003000"
            },
            {
                "name": "media",
                "qcode": "04010000"
            },
            {
                "name": "electrical appliance",
                "qcode": "04011004"
            },
            {
                "name": "joint venture",
                "qcode": "04016023"
            },
            {
                "name": "licensing agreement",
                "qcode": "04016026"
            },
            {
                "name": "new product",
                "qcode": "04016030"
            },
            {
                "name": "patent, copyright and trademark",
                "qcode": "04016031"
            },
            {
                "name": "business (general)",
                "qcode": "04018000"
            },
            {
                "name": "manufacturing and engineering",
                "qcode": "04011000"
            },
            {
                "name": "company information",
                "qcode": "04016000"
            }
        ],
        "version_creator": None,
        "priority": 6,
        "queue_state": "queued",
        "anpa_category": [
            {
                "name": "International News",
                "qcode": "i"
            }
        ],
        "language": "en",
        "pubstatus": "usable",
        "place": [

        ],
        "type": "text",
        "abstract": "Abstract",
        "unique_name": "#34056993",
        "state": "published",
        "headline": "XIAOMI LAUNCHES IN THE UK AS NEWEST PHONE RIVAL TO APPLE AND SAMSUNG",
        "genre": [
            {
                "name": "Article",
                "qcode": "Article"
            }
        ],
        "source": "PAA",
        "publish_schedule": None,
        "ingest_provider": "5615d77f069b7f774d66003a",
        "family_id": "urn:newsml:localhost:2018-11-09T03:01:27.558606:2a806251-790c-4615-944f-7856f0d417a3",
        "body_html": "<p>Body</p>\n",
        "firstcreated": ISODate("2018-11-08T16:00:00.000+0000"),
        "profile": "58b788bd069b7f6953927e9d",
        "moved_to_legal": True,
        "_current_version": 2,
        "last_published_version": True,
        "versioncreated": ISODate("2018-11-08T16:01:27.000+0000"),
        "ingest_provider_sequence": "3142",
        "operation": "publish",
        "ednote": "Advisory: First issued under embargo",
        "byline": "By Martyn Landi, Press Association Technology Correspondent",
        "is_take_item": False,
        "_created": ISODate("2018-11-08T16:01:27.000+0000"),
        "word_count": 489,
        "item_id": "tag:localhost:2018:68c56cfa-205b-4861-91bd-907423e3471b",
        "expiry": ISODate("2018-11-11T16:01:27.000+0000"),
        "format": "HTML",
        "unique_id": 34056993,
        "_etag": "bba81bd8b983060a72d4cd70b4b5dbcb69c7892e",
        "_updated": ISODate("2018-11-08T16:01:31.000+0000"),
        "original_creator": "",
        "ingest_id": "urn:newsml:localhost:2018-11-09T03:01:27.558606:2a806251-790c-4615-944f-7856f0d417a3",
        "firstpublished": ISODate("2018-11-08T16:01:27.000+0000"),
        "keywords": [
            "Xiaomi",
            "marketplace"
        ],
        "flags": {
            "marked_for_legal": False,
            "marked_archived_only": False,
            "marked_for_not_publication": False,
            "marked_for_sms": False
        },
        "auto_publish": True,
        "last_queue_event": ISODate("2018-11-08T16:01:27.000+0000")
    }, {
        "_id": "tag:localhost:2018:5514f993-b342-4231-a74c-b686a8205baf",
        "_current_version": 2,
        "source": "AP",
        "version_creator": None,
        "body_html": "<p>Body</p>",
        "ingest_id": "urn:newsml:localhost:2018-11-11T07:16:29.908105:d326a058-fa9b-4855-a579-a587e822d1fd",
        "family_id": "urn:newsml:localhost:2018-11-11T07:16:29.908105:d326a058-fa9b-4855-a579-a587e822d1fd",
        "unique_id": 34073203,
        "ingest_provider_sequence": "6950",
        "format": "HTML",
        "dateline": {
            "located": {
                "alt_name": "",
                "city_code": "Chicago",
                "dateline": "city",
                "city": "Chicago",
                "country_code": "US",
                "state": "Illinois",
                "state_code": "US.IL",
                "tz": "America/Chicago",
                "country": "United States"
            },
            "source": "AP",
            "text": "CHICAGO, Nov 10 AP -"
        },
        "versioncreated": ISODate("2018-11-10T20:16:29.000+0000"),
        "_updated": ISODate("2018-11-10T20:16:30.000+0000"),
        "language": "en",
        "unique_name": "#34073203",
        "pubstatus": "usable",
        "expiry": ISODate("2018-11-13T20:16:30.000+0000"),
        "genre": [
            {
                "scheme": None,
                "qcode": "Article",
                "name": "Article"
            }
        ],
        "ednote": "Updates with details of the study; comment. With AP Photos.",
        "type": "text",
        "word_count": 1003,
        "byline": "By MARILYNN MARCHIONE",
        "urgency": 3,
        "state": "published",
        "slugline": "US-MED--FishOil-Vitam",
        "profile": "58b788bd069b7f6953927e9d",
        "guid": "tag:localhost:2018:5514f993-b342-4231-a74c-b686a8205baf",
        "firstcreated": ISODate("2018-11-10T20:13:00.000+0000"),
        "_etag": "6af795422576fdb80ddbbc2f954f0dfc0eaed92d",
        "original_creator": "",
        "anpa_take_key": "1stLd-Writethru",
        "ingest_provider": "5625cf04069b7f392758f492",
        "priority": 6,
        "_created": ISODate("2018-11-10T20:16:29.000+0000"),
        "flags": {
            "marked_for_not_publication": False,
            "marked_for_legal": False,
            "marked_archived_only": False,
            "marked_for_sms": False
        },
        "anpa_category": [
            {
                "qcode": "i",
                "name": "International News"
            }
        ],
        "headline": "Big studies give mixed news on fish oil, vitamin D",
        "event_id": "tag:localhost:2018:9cfd2331-61e0-4331-bd2d-8d2328f76d7a",
        "operation": "publish",
        "auto_publish": True,
        "firstpublished": ISODate("2018-11-10T20:16:30.000+0000"),
        "publish_schedule": None
    }
    ]

    def setUp(self):
        self.formatter = MarketplaceNINJSFormatter()
        init_app(self.app)
        self.app.data.insert('ingest', self.ingest)

    def test_update_reuters_id(self):
        seq, doc = self.formatter.format(self.article[0], {'_id': 1, 'name': 'Test Subscriber'})[0]
        ninjs = json.loads(doc)
        self.assertEqual(ninjs['guid'], 'tag:reuters.com,2018:newsml_MT1VRT1203021832')

    def test_update_pa(self):
        seq, doc = self.formatter.format(self.article[1], {'_id': 1, 'name': 'Test Subscriber'})[0]
        ninjs = json.loads(doc)
        self.assertEqual(ninjs['guid'], '19f5b765-e160-4661-a8bb-b7f0a86a5107HHH-1')

    def test_spoof_ap(self):
        seq, doc = self.formatter.format(self.article[2], {'_id': 1, 'name': 'Test Subscriber'})[0]
        ninjs = json.loads(doc)
        self.assertEqual(ninjs['guid'], 'tag:localhost:2018:861146a6-9a01-48bc-8fb4-7757c7f236af')
