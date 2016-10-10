# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from apps.publish import init_app
from superdesk.tests import TestCase

from .slugline_mapper import SluglineMapper


class SelectorcodeMapperTest(TestCase):

    article1 = {
        'slugline': 'SLUG1',
        'genre': [{
            'name': 'Feature',
            'qcode': 'Feature'},
            {
                'name': 'Another One',
                'qcode': 'Another'}
        ]
    }

    article2 = {
        'slugline': 'SLUG2',
        'genre': [{
            'name': 'Explainer',
            'qcode': 'Explainer'},
            {
                'name': 'Another One',
                'qcode': 'Another'}
        ]
    }
    article3 = {
        'slugline': 'SLUG3',
        'flags': {'marked_for_legal': True},
        'genre': [{
            'name': 'Explainer',
            'qcode': 'Explainer'},
            {
                'name': 'Another One',
                'qcode': 'Another'}
        ]
    }
    article4 = {
        'genre': [{
            'name': 'Explainer',
            'qcode': 'Explainer'},
            {
                'name': 'Another One',
                'qcode': 'Another'}
        ]
    }
    slugline_map = SluglineMapper()

    def setUp(self):
        init_app(self.app)

    def test_finex_explainer_locator(self):
        self.assertEqual(self.slugline_map.map(self.article1, 'F', truncate=True), 'FINEX: SLUG1')
        self.assertEqual(self.slugline_map.map(self.article2, 'F', truncate=True), 'EXP: SLUG2')
        self.assertEqual(self.slugline_map.map(self.article3, 'F', truncate=True), 'Legal: EXP: SLUG3')
        self.assertEqual(self.slugline_map.map(self.article4, 'F', truncate=True), 'EXP: ')
