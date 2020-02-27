# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from unittests import AAPTestCase
from .accept_assignment import accept_assignment
from bson import ObjectId
from superdesk.utc import utcnow


class AcceptAssignmentTestCase(AAPTestCase):
    def setUp(self):
        self.app.data.insert('assignments', [
            {
                "_id": ObjectId("5e4f140db2825eac7796fbb4"),
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
                    "user": "5b0d58ea1d41c8a4552121f8",
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
        self.app.data.insert('users', [{
            '_id': ObjectId('5b0d58ea1d41c8a4552121f8'),
            'name': 'user1',
            'username': 'user1',
            'user_type': 'administrator',
            'email': 'user1@a.com.au',
            'byline': 'User 1'
        }])

    def test_post(self):
        item = {'body_html': '<div dir=3D"ltr">This email is being sent to an unmonitored (system) addres'
                             's. If you wish to discuss the details of the assignment further, you should'
                             ' contact a member of the team through other channels.<br>Assignment 5e4f140'
                             'db2825eac7796fbb4 has been accepted by <a href=3D"mailto:vnarayanaswamy@aap'
                             '.com.au">vnarayanaswamy@aap.com.au</a> 5b0d58ea1d41c8a4552121f8.</div>'}
        accept_assignment(item)
        assignment = self.app.data.find_one('assignments', None, _id=ObjectId("5e4f140db2825eac7796fbb4"))
        self.assertTrue(assignment.get('accepted'))
