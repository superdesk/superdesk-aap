# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import unittest
from copy import deepcopy
from .am_service_content import am_service_content


class AMServiceTestCase(unittest.TestCase):

    def test_genre_not_specified(self):
        item = {'body_html': 'text', 'type': 'text'}
        modified_item = am_service_content(deepcopy(item))
        self.assertEqual(modified_item['genre'][0], {'name': 'AM Service', 'qcode': 'AM Service'})
        self.assertNotIn('genre', item)

    def test_genre_specified(self):
        item = {'body_html': 'text', 'type': 'text', 'genre': [{'name': 'Article', 'qcode': 'Article'}]}
        modified_item = am_service_content(deepcopy(item))
        self.assertEqual(modified_item['genre'][0], {'name': 'AM Service', 'qcode': 'AM Service'})
        self.assertEqual(item['genre'][0], {'name': 'Article', 'qcode': 'Article'})

    def test_not_type_text(self):
        item = {'body_html': 'text', 'type': 'picture', 'genre': [{'name': 'Article', 'qcode': 'Article'}]}
        modified_item = am_service_content(deepcopy(item))
        self.assertEqual(modified_item['genre'][0], {'name': 'Article', 'qcode': 'Article'})
        self.assertEqual(item['genre'][0], {'name': 'Article', 'qcode': 'Article'})

    def test_slugline_not_specified(self):
        item = {'body_html': 'text', 'type': 'text', 'genre': [{'name': 'Article', 'qcode': 'Article'}]}
        modified_item = am_service_content(deepcopy(item))
        self.assertEqual(modified_item['genre'][0], {'name': 'AM Service', 'qcode': 'AM Service'})
        self.assertEqual(item['genre'][0], {'name': 'Article', 'qcode': 'Article'})
        self.assertIsNone(item.get('slugline'))

    def test_slugline_specified(self):
        item = {
            'body_html': 'text',
            'type': 'text',
            'genre': [{'name': 'Article', 'qcode': 'Article'}],
            'slugline': 'foo'
        }
        modified_item = am_service_content(deepcopy(item))
        self.assertEqual(modified_item['genre'][0], {'name': 'AM Service', 'qcode': 'AM Service'})
        self.assertEqual(item['genre'][0], {'name': 'Article', 'qcode': 'Article'})
        self.assertEqual(modified_item.get('slugline'), 'AM foo')
        self.assertEqual(item.get('slugline'), 'foo')

    def test_slugline_starts_with_am(self):
        item = {
            'body_html': 'text',
            'type': 'text',
            'genre': [{'name': 'Article', 'qcode': 'Article'}],
            'slugline': 'AM foo'
        }
        modified_item = am_service_content(deepcopy(item))
        self.assertEqual(modified_item['genre'][0], {'name': 'AM Service', 'qcode': 'AM Service'})
        self.assertEqual(item['genre'][0], {'name': 'Article', 'qcode': 'Article'})
        self.assertEqual(modified_item.get('slugline'), 'AM foo')
        self.assertEqual(item.get('slugline'), 'AM foo')
