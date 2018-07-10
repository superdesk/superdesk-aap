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
from superdesk.tests import TestCase
from superdesk.utc import utcnow
from aap.io.feed_parsers.asianet import AsiaNetFeedParser


class AsiaNetFeedParserTestCase(TestCase):
    filename = 'asianet_{}.tst'
    year = utcnow().year

    headers = [
        {
            'headline': 'Media Release: Digital Turbine, Inc.',
            'anpa_take_key': 'Digital Turbine, Inc.',
            'original_source': 'AsiaNet',
            'first_line': '<pre>MEDIA RELEASE PR67276\nDigital Turbine Partners with'
        },
        {
            'headline': 'Media Release: Queen Elizabeth Prize',
            'anpa_take_key': 'Queen Elizabeth Prize',
            'original_source': 'AsiaNet',
            'first_line': '<pre>MEDIA RELEASE PR67254\nQueen Elizabeth Prize'
        },
        {
            'headline': 'Media Release: Escola Aguia de Ouro',
            'anpa_take_key': 'Escola Aguia de Ouro',
            'original_source': 'AsiaNet',
            'first_line': '<pre>MEDIA RELEASE PR67255\nAnimal rights come to Brazil'
        },
        {
            'headline': 'Media Release: Essence',
            'anpa_take_key': 'Essence',
            'original_source': 'AsiaNet',
            'first_line': '<pre>MEDIA RELEASE PR67257\nDigital Agency Essence Builds on Enormous Growth'
        },
        {
            'headline': 'Media Release: OMRON Corporation',
            'anpa_take_key': 'OMRON Corporation',
            'original_source': 'AsiaNet',
            'first_line': '<pre>MEDIA RELEASE PR67261\nOMRON Launches Promotional Website for AI-equipped'
        },
        {
            'headline': 'Media Release: OnApp',
            'anpa_take_key': 'OnApp',
            'original_source': 'AsiaNet',
            'first_line': '<pre>MEDIA RELEASE PR67266\nOnApp v5.3 Simplifies Add-on Services'
        },
        {
            'headline': 'Media Release: Shinetech Software Inc.',
            'anpa_take_key': 'Shinetech Software Inc.',
            'original_source': 'AsiaNet',
            'first_line': '<pre>MEDIA RELEASE PR67271\nShinetech Software, Inc. Reports 16% Growth in 2016'
        },
        {
            'headline': 'Media Release: Huntsman Family Investments',
            'anpa_take_key': 'Huntsman Family Investme',
            'original_source': 'AsiaNet',
            'first_line': '<pre>MEDIA RELEASE PR67275\nHuntsman Family Investments to Acquire GTA TeleGuam'
        },
        {
            'headline': 'Media Release: Neovia Oncology Ltd',
            'anpa_take_key': 'Neovia Oncology Ltd',
            'original_source': 'AsiaNet',
            'first_line': '<pre>MEDIA RELEASE PR67278\nNeovia Enrolls First Patient in Cancer Trial'
        }
    ]

    def setUp(self):
        self.provider = {'name': 'Test'}
        self.maxDiff = None

    def test_can_parse(self):
        for i in range(1, 10):
            self.assertTrue(AsiaNetFeedParser().can_parse(self._get_fixture(i)))

    def test_feed_parser(self):
        test_keys = ['headline', 'anpa_take_key',
                     'original_source']
        for i in range(1, 10):
            item = AsiaNetFeedParser().parse(self._get_fixture(i), self.provider)
            expected = self.headers[i - 1]

            for key in test_keys:
                self.assertEqual(item[key], expected[key])

            self.assertGreater(item['word_count'], 0)

            # This tests for the body content, as well as as html escaping
            self.assertTrue(item['body_html'].startswith(expected['first_line']))

    def _get_fixture(self, index):
        dirname = os.path.dirname(os.path.realpath(__file__))
        return os.path.normpath(os.path.join(dirname, '../fixtures', self.filename.format(index)))
