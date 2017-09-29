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
from .aap_ninjs_formatter import AAPNINJSFormatter


class AAPNINJSFormatterTest(TestCase):
    def setUp(self):
        self.formatter = AAPNINJSFormatter()
        init_app(self.app)
        self.maxDiff = None

    def test_picture_formatter(self):
        article = {
            'guid': '20150723001158606583',
            '_current_version': 1,
            'slugline': "AMAZING PICTURE",
            'original_source': 'AAP',
            'renditions': {
                'viewImage': {
                    'width': 640,
                    'href': 'http://localhost:5000/api/upload/55b032041d41c8d278d21b6f/raw?_schema=http',
                    'mimetype': 'image/jpeg',
                    "height": 401
                },
                'original': {
                    'href': 'https://one-api.aap.com.au/api/v3/Assets/20150723001158606583/Original/download',
                    'mimetype': 'image/jpeg'
                },
            },
            'byline': 'MICKEY MOUSE',
            'headline': 'AMAZING PICTURE',
            'versioncreated': '2015-07-23T00:15:00.000Z',
            'ednote': 'TEST ONLY',
            'type': 'picture',
            'pubstatus': 'usable',
            'source': 'AAP',
            'description': 'The most amazing picture you will ever see',
            'guid': '20150723001158606583',
            'body_footer': '<p>call helpline 999 if you are planning to quit smoking</p>',
            'alt_text': 'alt text',
            'description_text': 'description text'
        }
        seq, doc = self.formatter.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        expected = {
            "body_text": "alt text",
            "byline": "MICKEY MOUSE",
            "renditions": {
                "original": {
                    "href": "https://one-api.aap.com.au/api/v3/Assets/20150723001158606583/Original/download",
                    "mimetype": "image/jpeg"
                },
            },
            "headline": "AMAZING PICTURE",
            "pubstatus": "usable",
            "version": "1",
            "versioncreated": "2015-07-23T00:15:00.000Z",
            "guid": "20150723001158606583",
            "description_html":
                "The most amazing picture you will ever see<p>call helpline 999 if "
                "you are planning to quit smoking</p>",
            "type": "picture",
            "priority": 5,
            "slugline": "AMAZING PICTURE",
            'ednote': 'TEST ONLY',
            'source': 'AAP',
            'description_text': 'description text'
        }
        self.assertEqual(expected, json.loads(doc))

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
                    "name": "Article (news)"
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
            "abstract": "<p>Article abstract</p>",
            "sms_message": "",
            "headline": "Article Headline",
            "word_count": 2,
            "body_html": "<p>Article Body</p>",
            "associations": {
                "featuremedia": {
                    "unique_name": "#32468",
                    "original_source": "AAP Image/AAP",
                    "flags": {
                        "marked_for_legal": False,
                        "marked_archived_only": False,
                        "marked_for_sms": False,
                        "marked_for_not_publication": False
                    },
                    "slugline": "RACING WINX ROSEHILL TRACKWORK",
                    "version_creator": "57bcfc5d1d41c82e8401dcc0",
                    "mimetype": "image/jpeg",
                    "state": "fetched",
                    "event_id": "tag:localhost:2017:8b4d1098-4e9a-4f81-b4fa-fb5362e00ae0",
                    "versioncreated": "2017-08-31T01:43:19+0000",
                    "operation": "fetch",
                    "format": "HTML",
                    "family_id": "20170831001315774144",
                    "_current_version": 1,
                    "archive_description": "Champion thoroughbred Winx is paraded in the mounting yard wearing her ear "
                                           "muffs after a run down the straight at Rosehill Racecourse during track "
                                           "work in Sydney, Thursday, August 31, 2017. Winx is aiming for her 19th "
                                           "consecutive victory this Saturday in the Tattersalls Chelmsford Stakes at "
                                           "Royal Randwick. (AAP Image/Dean Lewins) NO ARCHIVING",
                    "_updated": "2017-08-31T01:43:22+0000",
                    "_latest_version": 1,
                    "_created": "2017-08-31T01:43:22+0000",
                    "language": "en",
                    "ednote": "",
                    "_links": {
                        "parent": {
                            "title": "home",
                            "href": "/"
                        },
                        "collection": {
                            "title": "archive",
                            "href": "archive"
                        },
                        "self": {
                            "title": "Archive",
                            "href": "archive/tag:localhost:2017:087d0a10-c538-4f79-8045-b1021a4212ee"
                        }
                    },
                    "urgency": 3,
                    "pubstatus": "usable",
                    "byline": "DEAN LEWINS",
                    "_id": "tag:localhost:2017:087d0a10-c538-4f79-8045-b1021a4212ee",
                    "headline": "Picture Title",
                    "ingest_id": "20170831001315774144",
                    "source": "AAP",
                    "renditions": {
                        "4-3": {
                            "CropBottom": 3712,
                            "mimetype": "image/jpeg",
                            "CropRight": 5568,
                            "CropTop": 0,
                            "height": 600,
                            "CropLeft": 636,
                            "width": 800,
                            "media": "59a769f61d41c88f16818b29",
                            "poi": {
                                "x": 2760,
                                "y": 1484
                            },
                            "href": "http://localhost:5000/api/upload-raw/59a769f61d41c88f16818b29.jpg"
                        },
                        "thumbnail": {
                            "width": 180,
                            "mimetype": "image/jpeg",
                            "href": "http://localhost:5000/api/upload-raw/59a769b81d41c88f16818b1f?_schema=http",
                            "poi": {
                                "x": 109,
                                "y": 48
                            },
                            "height": 120,
                            "media": "59a769b81d41c88f16818b1f"
                        },
                        "original": {
                            "width": 5568,
                            "mimetype": "image/jpeg",
                            "href": "http://localhost:5000/api/upload-raw/59a769b71d41c88f16818b14.jpg",
                            "poi": {
                                "x": 3396,
                                "y": 1484
                            },
                            "height": 3712,
                            "media": "59a769b71d41c88f16818b14"
                        },
                        "baseImage": {
                            "width": 1400,
                            "mimetype": "image/jpeg",
                            "href": "http://localhost:5000/api/upload-raw/59a769ba1d41c88f16818b23?_schema=http",
                            "poi": {
                                "x": 854,
                                "y": 373
                            },
                            "height": 933,
                            "media": "59a769ba1d41c88f16818b23"
                        },
                        "viewImage": {
                            "width": 640,
                            "mimetype": "image/jpeg",
                            "href": "http://localhost:5000/api/upload-raw/59a769b91d41c88f16818b21?_schema=http",
                            "poi": {
                                "x": 390,
                                "y": 170
                            },
                            "height": 426,
                            "media": "59a769b91d41c88f16818b21"
                        },
                        "16-9": {
                            "CropBottom": 3143,
                            "mimetype": "image/jpeg",
                            "CropRight": 5568,
                            "CropTop": 0,
                            "height": 720,
                            "CropLeft": 0,
                            "width": 1280,
                            "media": "59a769f81d41c88f16818b2c",
                            "poi": {
                                "x": 3396,
                                "y": 1484
                            },
                            "href": "http://localhost:5000/api/upload-raw/59a769f81d41c88f16818b2c.jpg"
                        }
                    },
                    "description_text": "Picture Caption",
                    "alt_text": "alt text",
                    "poi": {
                        "x": 0.61,
                        "y": 0.4
                    },
                    "sign_off": "MAR",
                    "expiry": "2017-08-31T01:44:22+0000",
                    "priority": 6,
                    "ingest_provider": "57fc31271d41c8ac963ea536",
                    "firstcreated": "2017-08-30T19:58:33+0000",
                    "original_creator": "57bcfc5d1d41c82e8401dcc0",
                    "genre": [
                        {
                            "qcode": "Article",
                            "name": "Article (news)"
                        }
                    ],
                    "unique_id": 32468,
                    "guid": "20170831001315774144",
                    "anpa_category": [
                        {
                            "qcode": "i",
                            "name": "International News"
                        }
                    ],
                    "type": "picture",
                    "used": True
                }
            }
        }
        seq, doc = self.formatter.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        expected = {"guid": "urn:newsml:localhost:2017-08-31T11:40:29.408059:fd448b37-f35d-4bb2-a565-2433dcf1c338",
                    "headline": "Article Headline", "description_text": "Article abstract", "language": "en",
                    "located": "Milton Keynes",
                    "ednote": "Article ed note", "source": "AAP", "firstcreated": "2017-08-31T01:40:29.000Z",
                    "description_html": "<p>Article abstract</p>", "byline": "Article Byline",
                    "body_html": "<p>Article Body</p>", "slugline": "Article Slugline",
                    "subject": [{"name": "arts, culture and entertainment", "code": "01000000"}],
                    "versioncreated": "2017-08-31T01:44:24.000Z",
                    "service": [{"name": "International News", "code": "i"}], "type": "text", "version": "2",
                    "genre": [{"name": "Article (news)", "code": "Article"}], "priority": 6, "urgency": 3,
                    "readtime": 0,
                    "associations": {
                        "featuremedia": {"body_text": "alt text", "byline": "DEAN LEWINS", "headline": "Picture Title",
                                         "renditions": {"original": {"poi": {"x": 3396, "y": 1484},
                                                                     "href": "http://localhost:5000/api/"
                                                                             "upload-raw/59a769b71d41c88f16818b14.jpg",
                                                                     "media": "59a769b71d41c88f16818b14",
                                                                     "height": 3712, "mimetype": "image/jpeg",
                                                                     "width": 5568}},
                                         "description_text": "Picture Caption", "source": "AAP",
                                         "versioncreated": "2017-08-31T01:43:19+0000",
                                         "service": [{"name": "International News", "code": "i"}],
                                         "genre": [{"name": "Article (news)", "code": "Article"}], "type": "picture",
                                         "language": "en", "version": "1", "urgency": 3, "pubstatus": "usable",
                                         "priority": 6, "ednote": "", "mimetype": "image/jpeg",
                                         "slugline": "RACING WINX ROSEHILL TRACKWORK",
                                         "firstcreated": "2017-08-30T19:58:33+0000", "guid": "20170831001315774144"}},
                    "profile": "58cf62e01d41c8208dc20375", "place": [{"name": "NSW", "code": "NSW"}],
                    "pubstatus": "usable"}
        self.assertEqual(expected, json.loads(doc))
