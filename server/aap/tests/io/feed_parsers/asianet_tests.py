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
from datetime import datetime

from superdesk.tests import TestCase
from superdesk.utc import utc

from aap.io.feed_parsers.asianet import AsiaNetFeedParser


class AsiaNetFeedParserTestCase(TestCase):
    filename = 'asianet_{}.tst'

    headers = [
        {
            'slugline': 'Digital Turbine, Inc.',
            'headline': 'Digital Turbine Partners with Axiata Digital On Carrier Billing Platform Integration',
            'anpa_take_key': 'PR67276',
            'original_source': 'AsiaNet',
            'versioncreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'firstcreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'dateline': {
                'date': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
                'source': 'PRNewswire-AsiaNet',
                'text': 'AUSTIN, Texas, Feb. 1, 2017',
                'located': {
                    'dateline': 'city', 'country': 'United States', 'tz': 'America/Chicago', 'city_code': 'Austin',
                    'state': 'Texas', 'state_code': 'US.TX', 'city': 'Austin', 'alt_name': '', 'country_code': 'US'}
            },
            'first_line': '<pre>Digital Turbine, Inc. ( https://www.digitalturbine.com/ ) (Nasdaq: APPS), a'
        },
        {
            'slugline': 'Queen Elizabeth Prize',
            'headline': 'Queen Elizabeth Prize for Engineering Awarded to the Creators of Digital Imaging Sensors',
            'anpa_take_key': 'PR67254',
            'original_source': 'AsiaNet',
            'versioncreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'firstcreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'dateline': {
                'date': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
                'source': 'PRNewswire',
                'text': 'LONDON, Feb. 1, 2017',
                'located': {'dateline': 'city', 'country': 'Canada', 'tz': 'America/Toronto', 'city_code': 'London',
                            'state': 'Ontario', 'state_code': 'CA.08', 'city': 'London', 'alt_name': '',
                            'country_code': 'CA'}
            },
            'first_line': '<pre>    Four engineers responsible for the creation of digital imaging sensors were'
        },
        {
            'slugline': 'Escola Aguia de Ouro',
            'headline': 'Animal rights come to Brazil\'s Carnival for a show with no feathers',
            'anpa_take_key': 'PR67255',
            'original_source': 'AsiaNet',
            'versioncreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'firstcreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'dateline': {
                'date': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
                'source': 'PRNewswire-AsiaNet',
                'text': 'SAO PAULO, Feb. 1, 2017',
                'located': {'dateline': 'city', 'country': 'Brazil', 'tz': 'America/Sao_Paulo',
                            'city_code': 'Sao Paulo', 'state': 'São Paulo', 'state_code': 'BR.27',
                            'city': 'Sao Paulo', 'alt_name': '', 'country_code': 'BR'}
            },
            'first_line': '<pre>    -- Aguia de Ouro samba school to present theme on raising awareness of'
        },
        {
            'slugline': 'Essence',
            'headline': 'Digital Agency Essence Builds on Enormous Growth in APAC; Promotes Jovy Gill to Managing '
                        'Director of Australia',
            'anpa_take_key': 'PR67257',
            'original_source': 'AsiaNet',
            'versioncreated': datetime(2017, 2, 2, 0, 0, tzinfo=utc),
            'firstcreated': datetime(2017, 2, 2, 0, 0, tzinfo=utc),
            'dateline': {
                'date': datetime(2017, 2, 2, 0, 0, tzinfo=utc),
                'source': 'PRNewswire-AsiaNet',
                'text': 'SINGAPORE, Feb. 2, 2017',
                'located': {'dateline': 'city', 'country': 'Singapore', 'tz': 'Asia/Singapore',
                            'city_code': 'Singapore', 'state': 'Singapore (general)', 'state_code': 'SG.00',
                            'city': 'Singapore', 'alt_name': '', 'country_code': 'SG'}
            },
            'first_line': '<pre>- New Appointment Helps Essence Meet Increasing Demand for Data-Driven'
        },
        {
            'slugline': 'OMRON Corporation',
            'headline': 'OMRON Launches Promotional Website for AI-equipped Mobile Robot LD Series',
            'anpa_take_key': 'PR67261',
            'original_source': 'AsiaNet',
            'versioncreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'firstcreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'dateline': {
                'date': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
                'source': 'Kyodo JBN-AsiaNet',
                'text': 'KYOTO, Japan, Feb. 1, 2017',
                'located': {'city_code': 'KYOTO', 'city': 'KYOTO', 'tz': 'UTC', 'dateline': 'city'}
            },
            'first_line': '<pre>OMRON Corporation announced on February 1 the launch of a promotional website'
        },
        {
            'slugline': 'OnApp',
            'headline': 'OnApp v5.3 Simplifies Add-on Services for Cloud Providers',
            'anpa_take_key': 'PR67266',
            'original_source': 'AsiaNet',
            'versioncreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'firstcreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'dateline': {
                'date': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
                'source': 'PRNewswire-AsiaNet',
                'text': 'LONDON, Feb. 1',
                'located': {'dateline': 'city', 'country': 'Canada', 'tz': 'America/Toronto', 'city_code': 'London',
                            'state': 'Ontario', 'state_code': 'CA.08', 'city': 'London', 'alt_name': '',
                            'country_code': 'CA'}
            },
            'first_line': '<pre>- Makes it easy for cloud service providers and enterprises to offer a catalog'
        },
        {
            'slugline': 'Shinetech Software Inc.',
            'headline': 'Shinetech Software, Inc. Reports 16% Growth in 2016',
            'anpa_take_key': 'PR67271',
            'original_source': 'AsiaNet',
            'versioncreated': datetime(2017, 2, 2, 0, 0, tzinfo=utc),
            'firstcreated': datetime(2017, 2, 2, 0, 0, tzinfo=utc),
            'dateline': {
                'date': datetime(2017, 2, 2, 0, 0, tzinfo=utc),
                'source': 'PRNewswire-AsiaNet',
                'text': 'NEW YORK, LONDON and BEIJING, Feb. 2, 2017',
                'located': {'dateline': 'city', 'country': 'Canada', 'tz': 'America/Toronto', 'city_code': 'London',
                            'state': 'Ontario', 'state_code': 'CA.08', 'city': 'London', 'alt_name': '',
                            'country_code': 'CA'}
            },
            'first_line': '<pre>    -- Company continues strong rate of global business expansion, adds new'
        },
        {
            'slugline': 'Huntsman Family Investments',
            'headline': 'Huntsman Family Investments to Acquire GTA TeleGuam',
            'anpa_take_key': 'PR67275',
            'original_source': 'AsiaNet',
            'versioncreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'firstcreated': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
            'dateline': {
                'date': datetime(2017, 2, 1, 0, 0, tzinfo=utc),
                'source': 'PRNewswire-AsiaNet',
                'text': 'TAMUNING, Guam, Feb. 1, 2017',
                'located': {'city_code': 'TAMUNING', 'city': 'TAMUNING', 'tz': 'UTC', 'dateline': 'city'}
            },
            'first_line': '<pre>Huntsman Family Investments and its affiliates (&quot;HFI&quot;) announced today that'
        },
        {
            'slugline': 'Neovia Oncology Ltd',
            'headline': 'Neovia Enrolls First Patient in Cancer Trial for Immunotherapy Enhancing Drug',
            'anpa_take_key': 'PR67278',
            'original_source': 'AsiaNet',
            'versioncreated': datetime(2017, 2, 2, 0, 0, tzinfo=utc),
            'firstcreated': datetime(2017, 2, 2, 0, 0, tzinfo=utc),
            'dateline': {
                'date': datetime(2017, 2, 2, 0, 0, tzinfo=utc),
                'source': 'PRNewswire-AsiaNet',
                'text': 'BEIJING, Feb. 2, 2017',
                'located': {'dateline': 'city', 'country': 'China', 'tz': 'Asia/Harbin', 'city_code': 'Beijing',
                            'state': 'Beijing', 'state_code': 'CN.22', 'city': 'Beijing', 'alt_name': '',
                            'country_code': 'CN'}
            },
            'first_line': '<pre>Neovia Oncology,  (Beijing, Taiwan, &amp; Seattle), has begun its first Phase 1'
        }
    ]

    def setUp(self):
        self.provider = {'name': 'Test'}

    def test_can_parse(self):
        for i in range(1, 10):
            self.assertTrue(AsiaNetFeedParser().can_parse(self._get_fixture(i)))

    def test_feed_parser(self):
        test_keys = ['slugline', 'headline', 'firstcreated', 'versioncreated', 'anpa_take_key',
                     'original_source', 'dateline']
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
