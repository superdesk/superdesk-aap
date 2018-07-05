# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015, 2016, 2017 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import os
from xml.etree import ElementTree
from superdesk.tests import TestCase
from aap.io.feed_parsers.ReutersNewsMLTwoFeedParser import ReutersNewsMLTwoFeedParser
from superdesk.io.feed_parsers.newsml_2_0 import NewsMLTwoFeedParser


class ReutersNewsmlFeedParserTestCase(TestCase):
    filename = 'reuters_newsml.xml'

    def setUp(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        self.fixture = os.path.normpath(os.path.join(dirname, '../fixtures', self.filename))
        self.provider = {'name': 'Reuters', 'feeding_service': 'reuters_http', 'feed_parser': 'reutersnewsml2'}

    def test_parse_reuters_newsml(self):
        with open(self.fixture, 'rb') as f:
            parser = ReutersNewsMLTwoFeedParser()
            xml = ElementTree.parse(f)
            items = parser.parse(xml.getroot(), self.provider)
            self.assertEqual(items[0]['headline'], 'Pope Francis leaves Peru at end of Latin American trip')
            self.assertEqual(items[0]['place'], [])

    def test_parse_newsml(self):
        with open(self.fixture, 'rb') as f:
            parser = NewsMLTwoFeedParser()
            xml = ElementTree.parse(f)
            items = parser.parse(xml.getroot(), self.provider)
            self.assertEqual(items[0]['headline'], 'Pope Francis leaves Peru at end of Latin American trip')
            self.assertEqual(items[0]['place'], [{'name': 'Euro Zone'}])
