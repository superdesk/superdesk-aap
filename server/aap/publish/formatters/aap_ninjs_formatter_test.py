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
            }
        ])

    def test_aap_ninjs(self):
        article = {
            "guid": "20150723001158606583",
            "_current_version": 1,
            "type": "text",
            "family_id": "1234",
        }
        seq, doc = self.formatter.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        formatted = json.loads(doc)
        self.assertEqual(formatted['original_item'], '1234')
