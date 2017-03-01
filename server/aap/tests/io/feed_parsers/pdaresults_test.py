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
from aap.io.feed_parsers.pdaresults import PDAResultsParser
from superdesk.tests import TestCase


class PDAResultsTestCase(TestCase):
    provider = {'name': 'test provder', 'provider': {}}

    vocab = [{'_id': 'genre',
              'items': [{
                  "name": "Results (sport)",
                  "is_active": True,
                  "qcode": "Results (sport)"}]}]

    def setUp(self):
        self.app.data.insert('vocabularies', self.vocab)

    def test_default_format(self):
        filename = 'RR_20161025_CRANBOURNE_6.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'SOMETHING'
        self.items = PDAResultsParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'Cranbourne Gallop Result 6 Melbourne Tuesday')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'r')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15030001')
        self.assertEqual(self.items.get('slugline'), 'Cranbourne Gallop')
        self.assertEqual(self.items.get('genre')[0]['name'], 'Results (sport)')
        self.assertIn('versioncreated', self.items)

    def test_news_format(self):
        filename = 'NLRR_20161026_DOOMBEN_6.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'SOMETHING'
        self.items = PDAResultsParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'News: Doomben Gallop Result 6 Brisbane Wednesday')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'r')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15030001')
        self.assertEqual(self.items.get('slugline'), 'News: Doomben Gallop')
        self.assertIn('versioncreated', self.items)

    def test_shdrace_format(self):
        filename = 'HRRR_20161026_CANTERBURY_6.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'SOMETHING'
        self.items = PDAResultsParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'Shdrace: Canterbury Gallop Result 6 Sydney Wednesday')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'r')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15030001')
        self.assertEqual(self.items.get('slugline'), 'Shdrace: Canterbury Gallop')
        self.assertIn('versioncreated', self.items)

    def test_multiple_race_number_format(self):
        filename = 'RR_20161026_CANTERBURY_1-1.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'SOMETHING'
        self.items = PDAResultsParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'RPTG CRTG Canterbury Gallop Results 1-1 Sydney Wednesday')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'r')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15030001')
        self.assertEqual(self.items.get('slugline'), 'Canterbury Gallop')
        self.assertEqual(self.items.get('anpa_take_key'), 'Results 1-1 Sydney')
        self.assertIn('versioncreated', self.items)

    def test_can_parse(self):
        filename = 'RR_20161026_CANTERBURY_1-1.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        result = PDAResultsParser().can_parse(fixture)
        self.assertTrue(result)
