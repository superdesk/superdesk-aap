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
from .remove_place_with_no_qcode import remove_place_with_no_qcode


class RemovePlaceTests(TestCase):
    def simple_case_test(self):
        item = {
            "_id": "tag:localhost:2017:77b03a97-df04-446e-a112-94941f1bb12c",
            "place": [
                {
                    "name": "United States"
                }
            ]
        }
        remove_place_with_no_qcode(item)
        self.assertEqual(item['place'], [])

    def multiple_case_test(self):
        item = {
            "_id": "tag:localhost:2017:77b03a97-df04-446e-a112-94941f1bb12c",
            "place": [
                {
                    "name": "United States"
                },
                {
                    "name": "Wagga Wagga"
                }

            ]
        }

        remove_place_with_no_qcode(item)
        self.assertEqual(item['place'], [])

    def keep_one_case_test(self):
        item = {
            "_id": "tag:localhost:2017:77b03a97-df04-446e-a112-94941f1bb12c",
            "place": [
                {
                    "name": "United States"
                },
                {
                    "name": "Wagga Wagga",
                    "qcode": '1'
                }

            ]
        }

        remove_place_with_no_qcode(item)
        self.assertEqual(item['place'], [{"name": "Wagga Wagga", "qcode": '1'}])
