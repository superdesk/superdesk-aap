# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2018 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import datetime
from superdesk.tests import TestCase
from .market_place_route import market_place_route


class MarketPlaceTestCase(TestCase):

    def test_reuters_with_dateline(self):
        item = dict()
        item['source'] = 'Reuters'
        item['firstcreated'] = datetime.datetime(2015, 10, 26, 11, 45, 19, 0)
        item['body_html'] = '<p>DETROIT (Reuters) - General Motors Co <GM.N> Chief Financial Officer Chuck Stevens \
            said on Wednesday the macroeconomic challenges in Brazil will remain in the near term but the company \
            has \"huge upside leverage once the macro situation changes\" in South America\'s largest \
            economy.</p>\n<p>GM\'s car sales so far in October are up versus a year ago, Stevens said to reporters \
            after the No. 1 U.S. automaker reported third-quarter financial results.</p>\n<p>Stevens also \
            reaffirmed GM\'s past forecasts that it will show profit in Europe in 2016. It would be GM\'s first \
            profit in Europe since 1999.</p>\n<p> (Reporting by Bernie Woodall and Joseph White; \
            Editing by Chizu Nomiyamam and Jeffrey Benkoe)</p>'

        market_place_route(item)
        self.assertEqual(item['dateline']['located']['city'], 'Detroit')
        self.assertIn('marketplace', item.get('keywords'))
        self.assertNotIn('DETROIT (Reuters) - ', item.get('body_html'))
        self.assertTrue(item.get('body_html').startswith('<p>General Motors Co'))

    def test_unknown_datetline(self):
        item = dict()
        item['source'] = 'ABC'
        item['firstcreated'] = datetime.datetime(2015, 10, 26, 11, 45, 19, 0)
        item['body_html'] = '<p>DETROIT (ABC) - General Motors Co <GM.N> Chief Financial Officer Chuck Stevens \
            said on Wednesday the macroeconomic challenges in Brazil will remain in the near term but the company \
            has \"huge upside leverage once the macro situation changes\" in South America\'s largest \
            economy.</p>\n<p>GM\'s car sales so far in October are up versus a year ago, Stevens said to reporters \
            after the No. 1 U.S. automaker reported third-quarter financial results.</p>\n<p>Stevens also \
            reaffirmed GM\'s past forecasts that it will show profit in Europe in 2016. It would be GM\'s first \
            profit in Europe since 1999.</p>\n<p> (Reporting by Bernie Woodall and Joseph White; \
            Editing by Chizu Nomiyamam and Jeffrey Benkoe)</p>'

        market_place_route(item)
        self.assertIn('marketplace', item.get('keywords'))
        self.assertIn('DETROIT (ABC) - ', item.get('body_html'))
        self.assertTrue(item.get('body_html').startswith('<p>DETROIT (ABC) - General Motors Co'))
