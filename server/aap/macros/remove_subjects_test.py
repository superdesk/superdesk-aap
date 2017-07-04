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
from .remove_subjects import remove_subjects


class RemoveSubjectsTests(TestCase):
    def simple_case_test(self):
        item = {
            "_id": "tag:localhost:2017:77b03a97-df04-446e-a112-94941f1bb12c",
            "subject": [
                {
                    "name": "lifestyle and leisure",
                    "qcode": "10000000"
                },
                {
                    "name": "politics",
                    "qcode": "11000000"
                },
                {
                    "name": "diplomacy",
                    "qcode": "11002000"
                },
                {
                    "name": "human rights",
                    "qcode": "11007000"
                },
                {
                    "name": "immigration",
                    "qcode": "14003002"
                },
                {
                    "name": "social issue",
                    "qcode": "14000000"
                },
                {
                    "name": "demographics",
                    "qcode": "14003000"
                }
            ]
        }
        remove_subjects(item)
        self.assertEqual(item['subject'], [])
