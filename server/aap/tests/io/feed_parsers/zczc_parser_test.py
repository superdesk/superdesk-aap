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
import pytz
from unittest import mock
from datetime import datetime

from superdesk.tests import TestCase
from aap.io.feed_parsers.zczc import ZCZCFeedParser
from aap.io.feed_parsers.zczc_bob import ZCZCBOBParser
from aap.io.feed_parsers.zczc_medianet import ZCZCMedianetParser


class ZCZCTestCase(TestCase):
    provider = {'name': 'test provder', 'provider': {}}

    validators = [
        {
            'schema': {
                'slugline': {
                    'required': True,
                    'maxlength': 30,
                    'empty': False,
                    'nullable': False,
                    'type': "string"
                }
            },
            'type': 'text',
            'act': 'auto_publish',
            '_id': 'auto_publish_text'
        }
    ]

    vocab = [{'_id': 'locators', 'items': [{
        "name": "VIC",
        "state": "Victoria",
        "group": "Australia",
        "qcode": "VIC",
        "country": "Australia",
        "is_active": True,
        "world_region": "Oceania"},
        {"name": "QLD", "qcode": "QLD"},
        {"name": "FED", "qcode": "FED"}]},
        {'_id': 'genre',
         'items': [{
             "name": "Broadcast Script",
             "is_active": True,
             "qcode": "Broadcast Script"},
             {
                 "name": "Results (sport)",
                 "is_active": True,
                 "qcode": "Results (sport)"},
             {
                 "name": "AM Service",
                 "is_active": True,
                 "qcode": "AM Service"},
             {
                 "name": "Racing Data",
                 "is_active": True,
                 "qcode": "Racing Data"}
         ]}]

    def setUp(self):
        self.app.data.insert('validators', self.validators)
        self.app.data.insert('vocabularies', self.vocab)

    def test_default_format(self):
        filename = 'Standings__2014_14_635535729050675896.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'SOMETHING'
        self.items = ZCZCFeedParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'MOTOR:  Collated results/standings after Sydney NRMA 500')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'T')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15039001')
        self.assertIn('versioncreated', self.items)

    def test_medianet_format(self):
        filename = 'ED_841066_2_1.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'MNET'
        self.items = ZCZCMedianetParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'Media Release: Australian Financial Security Authority')
        self.assertEqual(self.items.get('place')[0], {'qcode': 'FED', 'name': 'FED'})
        self.assertEqual(self.items.get('subject')[0]['qcode'], '04000000')
        self.assertEqual(len(self.items.get('anpa_take_key')), 24)

    def test_medianet_investor_relations_format(self):
        filename = 'ED_867485_4_2.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'MNET'
        self.items = ZCZCMedianetParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'IRW News Release: Master Builders Australia')

    def test_tabular_format(self):
        filename = 'ED_900942_2_1.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'MNET'
        self.items = ZCZCMedianetParser().parse(fixture, self.provider)
        self.assertTrue(self.items.get('body_html').startswith('<pre>Media release distributed by Medianet.'))
        self.assertTrue(self.items.get('body_html').find('                    Dividend     Total Winners     '
                                                         'Total Prizes Payable') != -1)

    def test_bob(self):
        filename = '1487e8f1-f7f5-40f5-8c0f-0eba3c2e162d.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'BOB'
        self.items = ZCZCBOBParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('slugline'), 'Legionella_BC1')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'A')
        self.assertEqual(self.items.get('headline'), 'QLD: Legionella found in Qld hospital')
        self.assertEqual(self.items.get('anpa_take_key'), '(BRISBANE)')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '07000000')
        self.assertTrue(self.items.get('body_html').startswith('<p>Legionella bacteria has been found in a regional'))
        self.assertTrue(self.items.get('genre')[0]['qcode'], 'Broadcast Script')

    @mock.patch('aap.io.feed_parsers.zczc_bob.utcnow', lambda: datetime(2018, 11, 6, 2, 0, 0, 0, pytz.utc))
    def test_bob_am_headlines(self):
        filename = 'bob_am_headlines.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'AAP'

        self.items = ZCZCBOBParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('slugline'), 'AM Sydney headlines')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'A')
        self.assertEqual(self.items.get('headline'), 'Sydney headlines round-up Nov 06, 1200')
        self.assertEqual(self.items.get('abstract'), 'Sydney headlines round-up Nov 06, 1200')
        self.assertEqual(self.items.get('anpa_take_key'), '1200')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '07000000')
        self.assertTrue(self.items.get('body_html').startswith('<p>Here are this morning\'s latest headlines'))
        self.assertEqual(self.items.get('genre')[0]['qcode'], 'AM Service')
        self.assertEqual(self.items.get('dateline')['located']['city'], 'Sydney')
        self.assertEqual(self.items.get('dateline')['source'], 'AAP')
        self.assertEqual(self.items.get('dateline')['text'], 'SYDNEY, Nov 6 AAP -')

    def test_bob_empty_header_line(self):
        filename = '612fa1dc-c476-425d-8c80-d40bdc9cc1d5.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'BOB'
        self.items = ZCZCBOBParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('slugline'), 'Legal: Causevic_BC6')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'A')
        self.assertEqual(self.items.get('headline'), 'Vic: GPS device to come off Vic teen ')
        self.assertEqual(self.items.get('anpa_take_key'), '(MELBOURNE)')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '02000000')
        self.assertTrue(self.items.get('body_html').startswith('<p>A former Melbourne terror suspect no '
                                                               'longer needs to wear'))
        self.assertEqual(self.items.get('place')[0].get('state'), 'Victoria')
        self.assertEqual(self.items.get('genre')[0].get('name'), 'Broadcast Script')
