# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

"""Superdesk"""

from superdesk.tests import TestCase
from httmock import urlmatch, HTTMock
from .remote_sync import RemoteSyncCommand
import json


class RemoteSuncBaseTest(TestCase):
    desk = None
    stage = None
    search_count = 0

    def setUp(self):
        self.setupRemoteSyncMock(self)
        self.desk = self.app.data.insert('desks', [{"name": "test", "content_expiry": 0}])
        self.stage = self.app.data.insert('stages',
                                          [{"working_stage": True, "default_incoming": True, "desk": self.desk[0]}])

    @urlmatch(scheme='https', netloc='superdesk.com.au', path='/api/auth')
    def login_request(self, url, request):
        return {'status_code': 200,
                'content': b'{"token": "b57d50c0-0513-4c9f-8824-a2bd77d4db46"}'
                }


class RemoteSyncTest(RemoteSuncBaseTest):
    def test_single_text_item(self):
        cmd = RemoteSyncCommand()
        cmd.run('https://superdesk.com.au/api', 'test', 'test')
        published = self.app.data.find('published', None, None)
        self.assertEqual(published.count(), 1)

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.login_request, self.search_request])
        context.mock.__enter__()

    @urlmatch(scheme='https', netloc='superdesk.com.au', path='/api/search')
    def search_request(self, url, request):
        if self.search_count == 0:
            resp = {'_items': [
                {'archive_item': {'_id': '1', 'state': 'published', 'headline': 'test1',
                                  'sluglline': 'slugline', 'anpa_take_key': 'take',
                                  'task': {'desk': str(self.desk[0]), 'stage': str(self.stage[0])}}}
            ]}
        else:
            resp = {'_items': []}
        self.search_count += 1

        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }


class RemoteSyncTakeStory(RemoteSuncBaseTest):
    def test_takes_items(self):
        cmd = RemoteSyncCommand()
        cmd.run('https://superdesk.com.au/api', 'test', 'test')
        published = self.app.data.find("published", None, None)
        self.assertEqual(published.count(), 2)

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.login_request, self.search_request, self.archive_request])
        context.mock.__enter__()

    @urlmatch(scheme='https', netloc='superdesk.com.au', path='/api/auth')
    def login_request(self, url, request):
        return {'status_code': 200,
                'content': b'{"token": "b57d50c0-0513-4c9f-8824-a2bd77d4db46"}'
                }

    @urlmatch(scheme='https', netloc='superdesk.com.au', path='/api/archive')
    def archive_request(self, url, request):

        resp = {
            "_id": "urn:newsml:localhost:2017-01-24T13:00:58.541182:c6910856-62ad-49fe-a15b-95fa64a7fa4a",
            "source": "AAP",
            "_current_version": 3,
            "urgency": 3,
            "last_take": "urn:newsml:localhost:2017-01-24T13:00:58.486933:05917203-7162-4f3d-aec2-51d7342731b7",
            "dateline": {
                "source": "AAP",
                "located": {
                    "city_code": "Wagga Wagga",
                    "country_code": "AU",
                    "city": "Wagga Wagga",
                    "tz": "Australia/Sydney",
                    "state": "New South Wales",
                    "country": "Australia",
                    "dateline": "city",
                    "alt_name": "",
                    "state_code": "NSW"
                },
                "date": "2017-01-24T02:00:17.000Z",
                "text": "WAGGA WAGGA, Jan 24 AAP -"
            },
            "language": "en",
            "place": [
                {
                    "world_region": "Oceania",
                    "country": "Australia",
                    "qcode": "NSW",
                    "group": "Australia",
                    "state": "New South Wales",
                    "name": "NSW"
                }
            ],
            "schedule_settings": {},
            "groups": [
                {
                    "role": "grpRole:NEP",
                    "id": "root",
                    "refs": [
                        {
                            "idRef": "main"
                        }
                    ]
                },
                {
                    "role": "grpRole:main",
                    "id": "main",
                    "refs": [
                        {
                            "type": "text",
                            "residRef": "urn:newsml:localhost:2017-01-24T13:00:17.447175:ee7b6fb5-c2c1-4242-a412"
                                        "-cb48f9f599ee",
                            "guid": "urn:newsml:localhost:2017-01-24T13:00:17.447175:ee7b6fb5-c2c1-4242-a412"
                                    "-cb48f9f599ee",
                            "location": "archive",
                            "_current_version": 2,
                            "is_published": True,
                            "itemClass": "icls:text",
                            "slugline": "take1",
                            "renditions": {},
                            "headline": "headline"
                        },
                        {
                            "type": "text",
                            "residRef": "urn:newsml:localhost:2017-01-24T13:00:58.486933:05917203-7162-4f3d-aec2"
                                        "-51d7342731b7",
                            "guid": "urn:newsml:localhost:2017-01-24T13:00:58.486933:05917203-7162-4f3d-aec2"
                                    "-51d7342731b7",
                            "location": "archive",
                            "_current_version": 4,
                            "slugline": "take1",
                            "is_published": True,
                            "itemClass": "icls:text",
                            "renditions": {},
                            "headline": "headline"
                        }
                    ]
                }
            ],
            "pubstatus": "usable",
            "sign_off": "MAR",
            "format": "HTML",
            "slugline": "take1",
            "operation": "publish",
            "state": "published",
            "task": {'desk': str(self.desk[0]), 'stage': str(self.stage[0])},
            "family_id": "urn:newsml:localhost:2017-01-24T13:00:58.541182:c6910856-62ad-49fe-a15b-95fa64a7fa4a",
            "event_id": "tag:localhost:2017:d85f4e82-8af4-4dde-ac6a-8647cabc6cc8",
            "original_creator": "57bcfc5d1d41c82e8401dcc0",
            "guid": "urn:newsml:localhost:2017-01-24T13:00:58.541182:c6910856-62ad-49fe-a15b-95fa64a7fa4a",
            "unique_id": 27230,
            "type": "composite",
            "priority": 6,
            "headline": "headline",
            "unique_name": "#27230",
            "genre": [
                {
                    "qcode": "Article",
                    "name": "Article (news)"
                }
            ],
            "_etag": "a765e670ff6010137e0711d32d70093d41b1cebe",
            "subject": [
                {
                    "parent": None,
                    "scheme": None,
                    "qcode": "01000000",
                    "name": "arts, culture and entertainment"
                }
            ],
            "anpa_category": [
                {
                    "scheme": None,
                    "qcode": "a",
                    "name": "Australian General News"
                }
            ],
            "publish_schedule": None,
            "body_html": "<p>test take 1</p><br><p>take 2</p>"
        }
        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }

    @urlmatch(scheme='https', netloc='superdesk.com.au', path='/api/search')
    def search_request(self, url, request):
        if self.search_count == 0:
            resp = {'_items': [
                {'archive_item':
                    {
                        "_id": "urn:newsml:localhost:2017-01-24T13:00:17.447175:ee7b6fb5-c2c1-4242-a412-cb48f9f599ee",
                        "source": "AAP",
                        "_current_version": 2,
                        "urgency": 3,
                        "dateline": {
                            "source": "AAP",
                            "located": {
                                "city_code": "Wagga Wagga",
                                "country_code": "AU",
                                "city": "Wagga Wagga",
                                "tz": "Australia/Sydney",
                                "state": "New South Wales",
                                "country": "Australia",
                                "dateline": "city",
                                "alt_name": "",
                                "state_code": "NSW"
                            },
                            "date": "2017-01-24T02:00:17.000Z",
                            "text": "WAGGA WAGGA, Jan 24 AAP -"
                        },
                        "language": "en",
                        "unique_name": "#27228",
                        "version": 1,
                        "format": "HTML",
                        "unique_id": 27228,
                        "pubstatus": "usable",
                        "operation": "publish",
                        "state": "published",
                        "task": {'desk': str(self.desk[0]), 'stage': str(self.stage[0])},
                        "family_id": "urn:newsml:localhost:2017-01-24T13:00:17.447175:ee7b6fb5-c2c1-4242-a412"
                                     "-cb48f9f599ee",
                        "event_id": "tag:localhost:2017:d85f4e82-8af4-4dde-ac6a-8647cabc6cc8",
                        "original_creator": "57bcfc5d1d41c82e8401dcc0",
                        "type": "text",
                        "priority": 6,
                        "guid": "urn:newsml:localhost:2017-01-24T13:00:17.447175:ee7b6fb5-c2c1-4242-a412-cb48f9f599ee",
                        "place": [
                            {
                                "world_region": "Oceania",
                                "country": "Australia",
                                "qcode": "NSW",
                                "group": "Australia",
                                "state": "New South Wales",
                                "name": "NSW"
                            }
                        ],
                        "genre": [
                            {
                                "qcode": "Article",
                                "name": "Article (news)"
                            }
                        ],
                        "sign_off": "MAR",
                        "_etag": "5d5f808ac90dfc4fa9f9588120be3663a90d20cd",
                        "body_html": "<p>test take 1</p>",
                        "sms_message": "",
                        "headline": "headline",
                        "word_count": 3,
                        "slugline": "take1",
                        "linked_in_packages": [
                            {
                                "package": "urn:newsml:localhost:2017-01-24T13:00:58.541182:c6910856-62ad-49fe"
                                           "-a15b-95fa64a7fa4a"
                            }
                        ],
                        "subject": [
                            {
                                "parent": None,
                                "scheme": None,
                                "qcode": "01000000",
                                "name": "arts, culture and entertainment"
                            }
                        ],
                        "anpa_category": [
                            {
                                "scheme": None,
                                "qcode": "a",
                                "name": "Australian General News"
                            }
                        ]
                    }},
                {'archive_item': {
                    "_id": "urn:newsml:localhost:2017-01-24T13:00:58.486933:05917203-7162-4f3d-aec2-51d7342731b7",
                    "source": "AAP",
                    "_current_version": 4,
                    "urgency": 3,
                    "dateline": {
                        "source": "AAP",
                        "located": {
                            "city_code": "Wagga Wagga",
                            "country_code": "AU",
                            "city": "Wagga Wagga",
                            "tz": "Australia/Sydney",
                            "state": "New South Wales",
                            "country": "Australia",
                            "dateline": "city",
                            "alt_name": "",
                            "state_code": "NSW"
                        },
                        "date": "2017-01-24T02:00:17.000Z",
                        "text": "WAGGA WAGGA, Jan 24 AAP -"
                    },
                    "language": "en",
                    "place": [
                        {
                            "world_region": "Oceania",
                            "country": "Australia",
                            "qcode": "NSW",
                            "group": "Australia",
                            "state": "New South Wales",
                            "name": "NSW"
                        }
                    ],
                    "pubstatus": "usable",
                    "headline": "headline",
                    "sign_off": "MAR",
                    "format": "HTML",
                    "slugline": "take1",
                    "firstcreated": "2017-01-24T02:00:58.000Z",
                    "operation": "publish",
                    "anpa_take_key": "=2",
                    "state": "published",
                    "task": {'desk': str(self.desk[0]), 'stage': str(self.stage[0])},
                    "family_id": "urn:newsml:localhost:2017-01-24T13:00:58.486933:05917203-7162-4f3d-aec2-51d7342731b7",
                    "event_id": "tag:localhost:2017:d85f4e82-8af4-4dde-ac6a-8647cabc6cc8",
                    "original_creator": "57bcfc5d1d41c82e8401dcc0",
                    "unique_id": 27229,
                    "type": "text",
                    "priority": 6,
                    "guid": "urn:newsml:localhost:2017-01-24T13:00:58.486933:05917203-7162-4f3d-aec2-51d7342731b7",
                    "unique_name": "#27229",
                    "genre": [
                        {
                            "qcode": "Article",
                            "name": "Article (news)"
                        }
                    ],
                    "_etag": "b0afe557d3857584c2505385541e94bf8ef7d19c",
                    "linked_in_packages": [
                        {
                            "package": "urn:newsml:localhost:2017-01-24T13:00:58.541182:c6910856-62ad-49fe-a15b"
                                       "-95fa64a7fa4a"
                        }
                    ],
                    "body_html": "<p>take 2</p>",
                    "version": 2,
                    "sms_message": "",
                    "word_count": 2,
                    "subject": [
                        {
                            "parent": None,
                            "scheme": None,
                            "qcode": "01000000",
                            "name": "arts, culture and entertainment"
                        }
                    ],
                    "anpa_category": [
                        {
                            "scheme": None,
                            "qcode": "a",
                            "name": "Australian General News"
                        }
                    ],
                }}
            ]}
        else:
            resp = {'_items': []}
        self.search_count += 1

        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }


class RemoteSyncUpdatedStory(RemoteSuncBaseTest):
    def test_updated_item(self):
        cmd = RemoteSyncCommand()
        cmd.run('https://superdesk.com.au/api', 'test', 'test')
        published = self.app.data.find("published", None, None)
        self.assertEqual(published.count(), 1)
        for item in published:
            self.assertEqual(item['body_html'], '<p>Update second published</p>')

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.login_request, self.search_request, self.archive_request])
        context.mock.__enter__()

    @urlmatch(scheme='https', netloc='superdesk.com.au', path='/api/archive')
    def archive_request(self, url, request):

        resp = {
            "_id": "urn:newsml:localhost:2017-01-24T15:58:45.916146:42e12bf2-4ae6-4c6f-92dc-51c6ef5eab75",
            "source": "AAP",
            "_current_version": 2,
            "urgency": 3,
            "schedule_settings": {},
            "dateline": {
                "source": "AAP",
                "located": {
                    "city_code": "Wagga Wagga",
                    "country_code": "AU",
                    "city": "Wagga Wagga",
                    "alt_name": "",
                    "state": "New South Wales",
                    "country": "Australia",
                    "dateline": "city",
                    "tz": "Australia/Sydney",
                    "state_code": "NSW"
                },
                "date": "2017-01-24T04:56:49.000Z",
                "text": "WAGGA WAGGA, Jan 24 AAP -"
            },
            "language": "en",
            "place": [
                {
                    "world_region": "Oceania",
                    "country": "Australia",
                    "qcode": "NSW",
                    "group": "Australia",
                    "state": "New South Wales",
                    "name": "NSW"
                }
            ],
            "subject": [
                {
                    "parent": None,
                    "qcode": "03000000",
                    "scheme": None,
                    "name": "disaster and accident"
                }
            ],
            "groups": [
                {
                    "role": "grpRole:NEP",
                    "id": "root",
                    "refs": [
                        {
                            "idRef": "main"
                        }
                    ]
                },
                {
                    "role": "grpRole:main",
                    "id": "main",
                    "refs": [
                        {
                            "type": "text",
                            "residRef": "urn:newsml:localhost:2017-01-24T15:58:08.595544:d78dff44-32e9-4e7f-8641"
                                        "-005ac8e92b51",
                            "guid": "urn:newsml:localhost:2017-01-24T15:58:08.595544:d78dff44-32e9-4e7f-8641"
                                    "-005ac8e92b51",
                            "location": "archive",
                            "_current_version": 3,
                            "slugline": "update",
                            "is_published": True,
                            "itemClass": "icls:text",
                            "renditions": {},
                            "headline": "Update test"
                        }
                    ]
                }
            ],
            "pubstatus": "usable",
            "sign_off": "MAR",
            "format": "HTML",
            "slugline": "update",
            "operation": "publish",
            "state": "published",
            "rewrite_of": "urn:newsml:localhost:2017-01-24T15:57:45.531104:5565cc79-ccb8-4f59-b721-15eb8306d06c",
            "task": {'desk': str(self.desk[0]), 'stage': str(self.stage[0])},
            "family_id": "urn:newsml:localhost:2017-01-24T15:58:45.916146:42e12bf2-4ae6-4c6f-92dc-51c6ef5eab75",
            "event_id": "tag:localhost:2017:85387818-4b31-47e8-bbc5-077aafa17365",
            "original_creator": "57bcfc5d1d41c82e8401dcc0",
            "_etag": "29e00af7f4d10b8574b2d16cf603f5fec8469d28",
            "guid": "urn:newsml:localhost:2017-01-24T15:58:45.916146:42e12bf2-4ae6-4c6f-92dc-51c6ef5eab75",
            "unique_id": 27237,
            "type": "composite",
            "priority": 6,
            "headline": "Update test",
            "unique_name": "#27237",
            "genre": [
                {
                    "qcode": "Article",
                    "name": "Article (news)"
                }
            ],
            "rewrite_sequence": 1,
            "anpa_category": [
                {
                    "qcode": "a",
                    "scheme": None,
                    "name": "Australian General News"
                }
            ],
            "last_take": "urn:newsml:localhost:2017-01-24T15:58:08.595544:d78dff44-32e9-4e7f-8641-005ac8e92b51",
            "body_html": "<p>Update second published</p>"
        }
        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }

    @urlmatch(scheme='https', netloc='superdesk.com.au', path='/api/search')
    def search_request(self, url, request):
        if self.search_count == 0:
            resp = {'_items': [
                {"archive_item":
                    {
                        "_id": "urn:newsml:localhost:2017-01-24T15:56:49.476634:02f7fe82-69fb-4113-98b2-0f71facf35ab",
                        "source": "AAP",
                        "_current_version": 2,
                        "urgency": 3,
                        "dateline": {
                            "source": "AAP",
                            "located": {
                                "city_code": "Wagga Wagga",
                                "country_code": "AU",
                                "city": "Wagga Wagga",
                                "tz": "Australia/Sydney",
                                "state": "New South Wales",
                                "country": "Australia",
                                "dateline": "city",
                                "alt_name": "",
                                "state_code": "NSW"
                            },
                            "date": "2017-01-24T04:56:49.000Z",
                            "text": "WAGGA WAGGA, Jan 24 AAP -"
                        },
                        "language": "en",
                        "unique_name": "#27234",
                        "version": 1,
                        "format": "HTML",
                        "unique_id": 27234,
                        "pubstatus": "usable",
                        "operation": "publish",
                        "state": "published",
                        "task": {'desk': str(self.desk[0]), 'stage': str(self.stage[0])},
                        "family_id": "urn:newsml:localhost:2017-01-24T15:56:49.476634:02f7fe82-69fb-4113-98b2"
                                     "-0f71facf35ab",
                        "event_id": "tag:localhost:2017:85387818-4b31-47e8-bbc5-077aafa17365",
                        "original_creator": "57bcfc5d1d41c82e8401dcc0",
                        "type": "text",
                        "priority": 6,
                        "guid": "urn:newsml:localhost:2017-01-24T15:56:49.476634:02f7fe82-69fb-4113-98b2-0f71facf35ab",
                        "place": [
                            {
                                "world_region": "Oceania",
                                "country": "Australia",
                                "qcode": "NSW",
                                "group": "Australia",
                                "state": "New South Wales",
                                "name": "NSW"
                            }
                        ],
                        "genre": [
                            {
                                "qcode": "Article",
                                "name": "Article (news)"
                            }
                        ],
                        "sign_off": "MAR",
                        "_etag": "138aaf57839476b8e872e23c21bd8d07c5f11fb9",
                        "body_html": "<p>Update first published</p>",
                        "subject": [
                            {
                                "parent": None,
                                "scheme": None,
                                "qcode": "03000000",
                                "name": "disaster and accident"
                            }
                        ],
                        "sms_message": "",
                        "word_count": 3,
                        "headline": "Update test",
                        "slugline": "update",
                        "anpa_category": [
                            {
                                "scheme": None,
                                "qcode": "a",
                                "name": "Australian General News"
                            }
                        ],
                        "linked_in_packages": [
                            {
                                "package": "urn:newsml:localhost:2017-01-24T15:57:45.531104:5565cc79-ccb8-4f59-b721"
                                           "-15eb8306d06c"
                            }
                        ],
                        "rewritten_by": "urn:newsml:localhost:2017-01-24T15:58:08.595544:d78dff44-32e9-4e7f-8641"
                                        "-005ac8e92b51"
                    }},
                {"archive_item":
                    {
                        "_id": "urn:newsml:localhost:2017-01-24T15:58:08.595544:d78dff44-32e9-4e7f-8641-005ac8e92b51",
                        "source": "AAP",
                        "urgency": 3,
                        "dateline": {
                            "source": "AAP",
                            "located": {
                                "city_code": "Wagga Wagga",
                                "country_code": "AU",
                                "city": "Wagga Wagga",
                                "alt_name": "",
                                "state": "New South Wales",
                                "country": "Australia",
                                "dateline": "city",
                                "tz": "Australia/Sydney",
                                "state_code": "NSW"
                            },
                            "date": "2017-01-24T04:56:49.000Z",
                            "text": "WAGGA WAGGA, Jan 24 AAP -"
                        },
                        "place": [
                            {
                                "world_region": "Oceania",
                                "country": "Australia",
                                "qcode": "NSW",
                                "group": "Australia",
                                "state": "New South Wales",
                                "name": "NSW"
                            }
                        ],
                        "subject": [
                            {
                                "parent": None,
                                "qcode": "03000000",
                                "scheme": None,
                                "name": "disaster and accident"
                            }
                        ],
                        "pubstatus": "usable",
                        "headline": "Update test",
                        "language": "en",
                        "format": "HTML",
                        "slugline": "update",
                        "operation": "publish",
                        "anpa_take_key": "update",
                        "state": "published",
                        "rewrite_of": "urn:newsml:localhost:2017-01-24T15:57:45.531104:5565cc79-ccb8-4f59-b721"
                                      "-15eb8306d06c",
                        "task": {'desk': str(self.desk[0]), 'stage': str(self.stage[0])},
                        "family_id": "urn:newsml:localhost:2017-01-24T15:56:49.476634:02f7fe82-69fb-4113-98b2"
                                     "-0f71facf35ab",
                        "event_id": "tag:localhost:2017:85387818-4b31-47e8-bbc5-077aafa17365",
                        "sign_off": "MAR",
                        "body_html": "<p>Update second published</p>",
                        "_etag": "355aa8163b82b8bbbb6182e90debe2319230b8be",
                        "original_creator": "57bcfc5d1d41c82e8401dcc0",
                        "unique_id": 27236,
                        "word_count": 3,
                        "type": "text",
                        "priority": 6,
                        "guid": "urn:newsml:localhost:2017-01-24T15:58:08.595544:d78dff44-32e9-4e7f-8641-005ac8e92b51",
                        "unique_name": "#27236",
                        "genre": [
                            {
                                "qcode": "Article",
                                "name": "Article (news)"
                            }
                        ],
                        "rewrite_sequence": 1,
                        "anpa_category": [
                            {
                                "qcode": "a",
                                "scheme": None,
                                "name": "Australian General News"
                            }
                        ],
                        "_current_version": 3,
                        "version": 2,
                        "sms_message": "",
                        "linked_in_packages": [
                            {
                                "package": "urn:newsml:localhost:2017-01-24T15:58:45.916146:42e12bf2-4ae6-4c6f-92dc"
                                           "-51c6ef5eab75"
                            }
                        ],
                    }}
            ]}
        else:
            resp = {'_items': []}
        self.search_count += 1

        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }
