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

from aap.io.feed_parsers.news_bites import NewsBitesFeedParser


class NewsBitesFileTestCase(TestCase):

    filename = 'AAP201606060716291.tst'

    def setUp(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        self.fixture = os.path.normpath(os.path.join(dirname, '../fixtures', self.filename))
        self.provider = {'name': 'Test'}

    def test_headline(self):
        item = NewsBitesFeedParser().parse(self.fixture, self.provider)
        self.assertEqual(item['headline'], 'UGL continues project delay negotiation')
        self.assertEqual(item['format'], 'HTML')
        # Note left sloping apostrophe in string below, causes grief in html, use the
        # ruleset function to replace it.
        self.assertTrue(item['body_html'].startswith('<p>UGL’s construction'))
