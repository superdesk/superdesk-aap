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
from .reuters_route_process import reuters_route_process
import datetime


class RemoveSubjectsTests(TestCase):
    def simple_case_test(self):
        firstcreated = datetime.datetime(2015, 10, 26, 11, 45, 19, 0)
        item = {
            "_id": "tag:localhost:2017:77b03a97-df04-446e-a112-94941f1bb12c",
            "firstcreated": firstcreated,
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
            ],
            "place": [
                {
                    "name": "United States"
                }
            ],
            'body_html': '<p>DETROIT (Reuters) - General Motors Co <GM.N> Chief Financial Officer Chuck Stevens \
            said on Wednesday the macroeconomic challenges in Brazil will remain in the near term but the company \
            has \"huge upside leverage once the macro situation changes\" in South America\'s largest \
            economy.</p>\n<p>GM\'s car sales so far in October are up versus a year ago, Stevens said to reporters \
            after the No. 1 U.S. automaker reported third-quarter financial results.</p>\n<p>Stevens also \
            reaffirmed GM\'s past forecasts that it will show profit in Europe in 2016. It would be GM\'s first \
            profit in Europe since 1999.</p>\n<p> (Reporting by Bernie Woodall and Joseph White; \
            Editing by Chizu Nomiyamam and Jeffrey Benkoe)</p>'
        }
        reuters_route_process(item)
        self.assertEqual(item['subject'], [])
        self.assertEqual(item['place'], [])
        self.assertEqual(item['dateline']['located']['city'], 'Detroit')
