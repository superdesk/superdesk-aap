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
from .set_soccer_keyword import set_soccer_keyword_process


class SetSoccerProcessTests(TestCase):
    def test_add_keyword(self):
        item = {
            '_id': 'urn:newsml:localhost:2018-06-21T15:13:19.087640:7048be05-c362-4755-8a92-de16400fda95',
            'headline': 'Soccer MLS Review Latest',
            'original_creator': '',
            'type': 'text',
            'place': [],
            'abstract': '',
            'language': 'en',
            'ingest_provider_sequence': '6148',
            'slugline': 'Soccer MLS Review Latest',
            'source': 'PA',
            'body_html': '<p>Los Angeles FC snatched the final spot in the US Open Cup quarter-finals',
            'format': 'HTML',
            'operation': 'create',
            'keywords': [
                'MLS',
                'Review',
                'Latest'
            ],
            'anpa_category': [
                {
                    'qcode': 's',
                    'name': 'Overseas Sport'
                }
            ],
            'family_id': 'urn:newsml:localhost:2018-06-21T15:13:19.087640:7048be05-c362-4755-8a92-de16400fda95',
        }
        set_soccer_keyword_process(item)
        self.assertEqual(item['keywords'], ['MLS', 'Review', 'Latest', 'RAW SOCCER'])

    def test_empty_keywords(self):
        item = {
            'type': 'text',
            'keywords': []
        }
        set_soccer_keyword_process(item)
        self.assertEqual(item['keywords'], ['RAW SOCCER'])

    def test_no_keywords(self):
        item = {
            'type': 'text'
        }
        set_soccer_keyword_process(item)
        self.assertEqual(item['keywords'], ['RAW SOCCER'])
