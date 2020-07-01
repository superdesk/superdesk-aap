# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from apps.publish import init_app
from .golf_collation import golf_collation
from bson import ObjectId
from datetime import timedelta
from superdesk.utc import utcnow
from unittests import AAPTestCase


class TestGolfCollation(AAPTestCase):
    def setUp(self):
        init_app(self.app)
        self.app.config['DEFAULT_TIMEZONE'] = 'Australia/Sydney'
        self.app.data.insert('archive', [
            {"place": [{"qcode": "WA"}],
             "task": {
                 "desk": ObjectId("5e1e9474d70421b46535ebe6"),
                 "stage": ObjectId("5e1e9474d70421b46535ebe4")
            },
                "headline": "Included 1",
                "slugline": "The links A",
                "subject": [{"qcode": "15027000"}],
                "state": "submitted",
                "versioncreated": utcnow() - timedelta(hours=5),
                "body_html": "<p>LINKS A: somebody something</p>"
            },
            {"place": [{"qcode": "WA"}],
             "task": {
                 "desk": ObjectId("5e1e9474d70421b46535ebe6"),
                 "stage": ObjectId("5e1e9474d70421b46535ebe4")
            },
                "headline": "Excluded due to slugline",
                "slugline": "Golf Results",
                "subject": [{"qcode": "15027000"}],
                "state": "submitted",
                "versioncreated": utcnow() - timedelta(hours=5),
                "body_html": "<p>LINKS A: somebody something</p>"
            },
            {"place": [{"qcode": "WA"}],
             "task": {
                 "desk": ObjectId("5e1e9474d70421b46535ebe6"),
                 "stage": ObjectId("5e1e9474d70421b46535ebe4")
            },
                "headline": "Excluded due to age",
                "slugline": "The links A",
                "subject": [{"qcode": "15027000"}],
                "state": "submitted",
                "versioncreated": utcnow() - timedelta(hours=25),
                "body_html": "<p>LINKS A: somebody something</p>"
            },
            {"place": [{"qcode": "SA"}],
             "task": {
                 "desk": ObjectId("5e1e9474d70421b46535ebe6"),
                 "stage": ObjectId("5e1e9474d70421b46535ebe4")
            },
                "headline": "Included 1",
                "slugline": "Echung",
                "subject": [{"qcode": "15027000"}],
                "state": "submitted",
                "versioncreated": utcnow() - timedelta(hours=5),
                "body_html": "<p>ECHUNGA: somebody something</p>"
            },
            {"place": [{"qcode": "SA"}],
             "task": {
                 "desk": ObjectId("5e1e9474d70421b46535ebe6"),
                 "stage": ObjectId("5e1e9474d70421b46535ebe4")
            },
                "headline": "Included 2",
                "slugline": "Gawler",
                "subject": [{"qcode": "15027000"}],
                "state": "submitted",
                "versioncreated": utcnow() - timedelta(hours=5),
                "body_html": "<p>GAWLER: somebody something</p>"
            },
            {"place": [{"qcode": "SA"}],
             "task": {
                 "desk": ObjectId("5e1e9474d70421b46535ebe6"),
                 "stage": ObjectId("5e1e9474d70421b46535ebe4")
            },
                "headline": "Included 3",
                "slugline": "Penola",
                "subject": [{"qcode": "15027000"}],
                "state": "submitted",
                "versioncreated": utcnow() - timedelta(hours=5),
                "body_html": "<p>PENOLA: somebody something</p>"
            },
            {"place": [{"qcode": "SA"}],
             "task": {
                 "desk": ObjectId("5e1e9474d70421b46535ebe6"),
                 "stage": ObjectId("5e1e9474d70421b46535ebe4")
            },
                "headline": "Excluded due to slugline",
                "slugline": "Golf Results",
                "subject": [{"qcode": "15027000"}],
                "state": "submitted",
                "versioncreated": utcnow() - timedelta(hours=5),
                "body_html": "<p>LINKS A: somebody something</p>"
            },
            {"place": [{"qcode": "SA"}],
             "task": {
                 "desk": ObjectId("5e1e9474d70421b46535ebe6"),
                 "stage": ObjectId("5e1e9474d70421b46535ebe4")
            },
                "headline": "Excluded due to age",
                "slugline": "The links A",
                "subject": [{"qcode": "15027000"}],
                "state": "submitted",
                "versioncreated": utcnow() - timedelta(hours=25),
                "body_html": "<p>LINKS A: somebody something</p>"
            }
        ])
        self.app.data.insert('desks', [
            {'_id': ObjectId("5e1e9474d70421b46535ebe6"), "name": "Copytakers"},
            {'_id': ObjectId("123456789009876543221123"), "name": "Nothing to see here"}
        ])
        self.app.data.insert('stages', [
            {"_id": ObjectId("5e1e9474d70421b46535ebe4"), "name": "Some Hold stage",
             "desk": ObjectId("5e1e9474d70421b46535ebe6")},
            {"_id": ObjectId("abababababababababababab"), "name": "Nothing to see here",
             "desk": ObjectId("5e1e9474d70421b46535ebe6")}
        ])

    def testWAGolf(self):
        item = {'place': [{'qcode': 'WA'}]}
        golf_collation(item)
        self.assertEqual(item.get('body_html'), '<p>LINKS A: somebody something</p>')

    def testSAGolf(self):
        item = {'place': [{'qcode': 'SA'}], 'anpa_take_key': 'Country'}
        golf_collation(item)
        self.assertEqual(item.get('body_html'), '<p>ECHUNGA: somebody something</p>')

    def testSACollatedGolf(self):
        item = {'place': [{'qcode': 'SA'}]}
        golf_collation(item)
        self.assertTrue(1)
        self.assertEqual(item.get('body_html'), '<p>Metropolitan</p><p>ECHUNGA: somebody something</p>'
                                                '<p>GAWLER: somebody something</p><p>Country</p>'
                                                '<p>South East</p><p>PENOLA: somebody something</p>')
