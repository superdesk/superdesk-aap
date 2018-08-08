# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import os

from superdesk.tests import TestCase

from aap.io.feed_parsers.ticker_parser import TickerFileParser


class TickerFileTestCase(TestCase):

    filename = 'ticker_sample.txt'

    def setUp(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        self.fixture = os.path.normpath(os.path.join(dirname, '../fixtures', self.filename))
        self.provider = {'name': 'Test'}

    def test_ticker_story(self):
        item = TickerFileParser().parse(self.fixture, self.provider)
        self.assertTrue(item['headline'].startswith('AAP Ticker on'))
        self.assertEqual(item['format'], 'preserved')
        self.assertEqual(item['type'], 'text')
        self.assertTrue(item['body_html'].startswith('<pre>TRUMP PLANS TO INVITE PUTIN TO WASHINGTON **'))
