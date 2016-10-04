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
from aap.io.feed_parsers.zczc import ZCZCFeedParser
from aap.io.feed_parsers.zczc_bob import ZCZCBOBParser
from aap.io.feed_parsers.zczc_pmf import ZCZCPMFParser
from aap.io.feed_parsers.zczc_medianet import ZCZCMedianetParser
from aap.io.feed_parsers.zczc_racing import ZCZCRacingParser
from aap.io.feed_parsers.zczc_sportsresults import ZCZCSportsResultsParser


class ZCZCTestCase(TestCase):
    provider = {'name': 'test provder', 'provider': {}}

    validators = [
        {
            'schema': {
                'headline': {
                    'required': True,
                    'maxlength': 64,
                    'empty': False,
                    'nullable': False,
                    'type': "string"
                },
                'slugline': {
                    'required': True,
                    'maxlength': 24,
                    'empty': False,
                    'nullable': False,
                    'type': "string"
                }

            },
            'type': 'text',
            'act': 'publish',
            '_id': 'publish_text'
        }
    ]

    vocab = [{'_id': 'locators', 'items': [{
        "name": "VIC",
        "state": "Victoria",
        "group": "Australia",
        "qcode": "VIC",
        "country": "Australia",
        "is_active": True,
        "world_region": "Oceania"
    }]}, {'_id': 'genre', 'items': [{
        "name": "Broadcast Script",
        "is_active": True,
        "qcode": "Broadcast Script"},
        {
            "name": "Results (sport)",
            "is_active": True,
            "qcode": "Results (sport)"}
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

    def test_sports_results_format(self):
        filename = 'Standings__2014_14_635535729050675896.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'SOMETHING'
        self.items = ZCZCSportsResultsParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'MOTOR:  Collated results/standings after Sydney NRMA 500')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'T')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15039001')
        self.assertEqual(self.items.get('genre')[0]['qcode'], 'Results (sport)')
        self.assertIn('versioncreated', self.items)

    def test_medianet_format(self):
        filename = 'ED_841066_2_1.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'MNET'
        self.items = ZCZCMedianetParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'Media Release: Australian Financial Security Authority')

    def test_pagemasters_format(self):
        filename = 'Darwin GR - Greys - Sun 11 Oct, 2015.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'PMF'
        self.items = ZCZCPMFParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'Darwin Greyhound Fields Sunday')
        self.assertEqual(self.items.get('slugline'), 'Darwin Grey')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'r')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15082000')
        self.assertEqual(self.items.get('genre')[0]['qcode'], 'Results (sport)')

    def test_racing_format(self):
        filename = 'viflda004_7257.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'BRA'
        self.items = ZCZCRacingParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), ' Racing.Com Park FIELDS Thursday')
        self.assertEqual(self.items.get('slugline'), ' Racing.Com Park FIELDS ')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'r')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15030001')

    def test_trot_tab_divs(self):
        filename = 'Wagga Trot VIC TAB DIVS 1-4 Friday.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'PMF'
        self.items = ZCZCPMFParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'VIC TAB DIVS 1-4 Friday')
        self.assertEqual(self.items.get('slugline'), 'Wagga Trot')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'r')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15030003')

    def test_leading_jockeys(self):
        filename = 'vinlpt_8390.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'BRA'
        self.items = ZCZCRacingParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'Leading jockeys (Sydney)')
        self.assertEqual(self.items.get('slugline'), 'Leading jockeys (Sydney)')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'r')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15030001')

    def test_weights(self):
        filename = 'viwhtn01_8594.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'BRA'
        self.items = ZCZCRacingParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'STRADBROKE HANDICAP 1400M .=!')
        self.assertEqual(self.items.get('slugline'), 'STRADBROKE HANDICAP 1400')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'r')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '15030001')

    def test_bob(self):
        filename = '1487e8f1-f7f5-40f5-8c0f-0eba3c2e162d.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'BOB'
        self.items = ZCZCBOBParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('slugline'), 'Legionella_BC1')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'A')
        self.assertEqual(self.items.get('headline'), 'Legionella found in Qld hospital')
        self.assertEqual(self.items.get('anpa_take_key'), '(BRISBANE)')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '07000000')
        self.assertTrue(self.items.get('body_html').startswith('<p>Legionella bacteria has been found in a regional'))

    def test_bob_empty_header_line(self):
        filename = '612fa1dc-c476-425d-8c80-d40bdc9cc1d5.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'BOB'
        self.items = ZCZCBOBParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('slugline'), 'Legal: Causevic_BC6')
        self.assertEqual(self.items.get('anpa_category')[0]['qcode'], 'A')
        self.assertEqual(self.items.get('headline'), 'GPS device to come off Vic teen ')
        self.assertEqual(self.items.get('anpa_take_key'), '(MELBOURNE)')
        self.assertEqual(self.items.get('subject')[0]['qcode'], '02000000')
        self.assertTrue(self.items.get('body_html').startswith('<p>A former Melbourne terror suspect no '
                                                               'longer needs to wear'))
        self.assertEqual(self.items.get('place')[0].get('state'), 'Victoria')
        self.assertEqual(self.items.get('genre')[0].get('name'), 'Broadcast Script')
