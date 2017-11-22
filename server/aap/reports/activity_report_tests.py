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
from superdesk.utc import get_date
from .activity_report import GenerateActivityCountReport


class ActivityReportTestCase(AAPTestCase):
    history = [
        {
            "operation": "create",
            "_created": get_date("2017-05-09T01:55:47+0000"),
            "item_id": "item1",
            "version": 1,
            "_updated": get_date("2017-05-09T01:55:47+0000"),
            "user_id": "user1"
        },
        {
            "operation": "update",
            "_created": get_date("2017-05-09T01:55:47+0000"),
            "item_id": "item1",
            "version": 2,
            "_updated": get_date("2017-05-09T01:55:47+0000"),
            "user_id": "user1"
        },
        {
            "operation": "create",
            "_created": get_date("2017-05-09T01:55:47+0000"),
            "item_id": "item2",
            "version": 1,
            "_updated": get_date("2017-05-09T01:55:47+0000"),
            "user_id": "user2"
        },
        {
            "operation": "create",
            "_created": get_date("2017-05-09T01:55:47+0000"),
            "item_id": "item3",
            "version": 1,
            "_updated": get_date("2017-05-09T01:55:47+0000"),
            "user_id": "user1"
        },
        {
            "operation": "update",
            "_created": get_date("2017-05-09T01:55:47.000+0000"),
            "item_id": "item3",
            "version": 2,
            "_updated": get_date("2017-05-09T01:55:47+0000"),
            "user_id": "user1"
        },
        {
            "operation": "spike",
            "_created": get_date("2017-05-09T01:55:47+0000"),
            "item_id": "item3",
            "version": 3,
            "_updated": get_date("2017-05-09T01:55:47+0000"),
            "user_id": "user2"
        },
        {
            "operation": "create",
            "_created": get_date("2017-05-10T01:55:47+0000"),
            "item_id": "item4",
            "version": 1,
            "_updated": get_date("2017-05-10T01:55:47+0000"),
            "user_id": "user2"
        }
    ]

    def setUp(self):
        super().setUp()
        self.app.data.insert('archive_history', self.history)

    def test_compare_repos(self):
        with self.app.app_context():
            cmd = GenerateActivityCountReport()
            items = cmd.run(get_date("2017-05-10T23:59:59+0000"))
            self.assertEqual(len(items), 3)
            user1_items = [item for item in items if item['user_id'] == 'user1']
            user2_items = [item for item in items if item['user_id'] == 'user2']
            self.assertEqual(len(user1_items), 1)
            self.assertEqual(len(user2_items), 2)
            self.assertEqual(user1_items[0]['create_count'], 1)
            self.assertEqual(user1_items[0]['update_count'], 1)
            self.assertEqual(user2_items[0]['create_count'], 1)
            self.assertEqual(user2_items[0]['update_count'], 0)
            self.assertEqual(user2_items[1]['create_count'], 1)
            self.assertEqual(user2_items[1]['update_count'], 0)
