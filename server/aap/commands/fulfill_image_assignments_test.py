# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015, 2016, 2017 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from bson.objectid import ObjectId
from unittest import mock
from unittests import AAPTestCase
from .fulfill_image_assignments import FullfillImageAssignments
from superdesk.utc import utcnow
from httmock import urlmatch, HTTMock
from eve_elastic.elastic import ElasticCursor
import os


class FullfillImageAssignmentsTest(AAPTestCase):
    def setUp(self):
        self.setupMock(self)
        self.app.data.insert('assignments', [
            {
                "_id": ObjectId("5e1692406bb0d58d639f6996"),
                "original_creator": "57bcfc5d1d41c82e8401dcc0",
                "priority": 2,
                "planning": {
                    "scheduled": utcnow(),
                    "slugline": "Thursday test 2",
                    "genre": None,
                    "g2_content_type": "picture"
                },
                "type": "assignment",
                "description_text": None,
                "planning_item": "urn:newsml:localhost:2020-01-09T13:38:55.038020:74bd445f-fb28-4135-b4a1-2143b5308a1c",
                "coverage_item": "urn:newsml:localhost:2020-01-09T13:38:56.294369:a275ef88-b67c-44f8-a850-775b6e8c6bc5",
                "assigned_to": {
                    "assignor_desk": "57bcfc5d1d41c82e8401dcc0",
                    "assigned_date_desk": "2020-01-09T02:38:56.000Z",
                    "contact": None,
                    "user": None,
                    "desk": "54e68fcd1024542de76d6643",
                    "state": "assigned",
                    "coverage_provider": {
                        "qcode": "stringer",
                        "name": "Stringer",
                        "contact_type": "stringer"
                    }
                }
            }
        ])
        self.app.data.insert('search_providers', [{
            "_id": ObjectId("57439f8b78b25422601f89c4"),
            "search_provider": "aapmm",
            "source": "aapmm",
            "is_default": False,
            "is_closed": False,
            "config": {
                "username": '',
                "password": ''
            }
        }])
        self.app.data.insert('users', [{
            '_id': ObjectId('57bcfc5d1d41c82e8401dcc0'),
            'name': 'user1',
            'username': 'user1',
            'user_type': 'administrator',
            'email': 'user1@a.com.au',
            'byline': 'User 1'
        }])
        self.app.config['DC_URL'] = 'http://a.b.c/rest/aap'

        self.script = FullfillImageAssignments()

    def setupMock(self, context):
        context.mock = HTTMock(*[self.mock_dc, self.mock_imagearc_dc, self.mock_dc_login])
        context.mock.__enter__()

    @urlmatch(scheme='http', netloc='a.b.c', path='/rest/aap/archives/imagearc')
    def mock_imagearc_dc(self, url, request):
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../tests/io/fixtures', 'dc_response.xml'))
        with open(fixture, 'r') as f:
            xml_raw = f.read()
        return {'status_code': 200, 'content': xml_raw}

    @urlmatch(scheme='http', netloc='a.b.c', path='/rest/aap')
    def mock_dc_login(self, url, request):
        return {'status_code': 200, 'content': b'<dc_rest_application></dc_rest_application>'}

    @urlmatch(scheme='http', netloc='a.b.c', path='/rest/aap/archives/aapimage')
    def mock_dc(self, url, request):
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../tests/io/fixtures', 'dc_response.xml'))
        with open(fixture, 'r') as f:
            xml_raw = f.read()
        return {'status_code': 200, 'content': xml_raw}

    def mock_find(resource, req, lookup, p):
        doc = {'fetch_endpoint': 'search_providers_proxy', 'pubstatus': 'usable', 'slugline': 'Fish on a bike',
               'byline': 'Fred Smith/AAP PHOTOS', '_id': '20200108001362610429',
               '_type': 'externalsource', 'original_source': 'AAP Image/AAP',
               'description_text': 'Sydney to the Gong some years ago', 'guid': '20200108001362610429',
               'type': 'picture', 'firstcreated': utcnow(), 'ednote': 'Not for publication',
               'source': 'AAP Image', 'headline': 'Fish on a bike', 'versioncreated': utcnow(),
               'archive_description': 'Sydney to the Gong some years ago'}
        hits = {'docs': [doc], 'total': 1}
        return ElasticCursor(docs=hits['docs'], hits={'hits': hits, 'aggregations': None})

    def mock_find_progress(resource, req, lookup, p):
        doc = {}
        hits = {'docs': [doc], 'total': 0}
        return ElasticCursor(docs=hits['docs'], hits={'hits': hits, 'aggregations': None})

    def test_check_complete(self):
        assignments = self.script._get_outstanding_photo_assignments()
        self.assertTrue(assignments.count() == 1)

    @mock.patch('aap_mm.aap_mm_datalayer.AAPMMDatalayer.find', mock_find)
    def test_run(self):
        self.script.run()
        assignments = self.app.data.find('assignments', None, None)
        self.assertEqual(assignments[0].get('assigned_to').get('state'), 'completed')
        planning_history = self.app.data.find('planning_history', None, None)
        self.assertEqual(planning_history[0].get('user_id'), ObjectId('57bcfc5d1d41c82e8401dcc0'))

    @mock.patch('aap_mm.aap_mm_datalayer.AAPMMDatalayer.find', mock_find_progress)
    def test_in_progress(self):
        self.script.run()
        assignments = self.app.data.find('assignments', None, None)
        self.assertEqual(assignments[0].get('assigned_to').get('state'), 'in_progress')
