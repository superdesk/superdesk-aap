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
from aap.io.feed_parsers.bom import BOMParser


class BOMFeedParserTestCase(TestCase):
    provider = {'name': 'test provder', 'provider': {}}

    vocab = [{'_id': 'bom_products', 'items': [{'is_active': True, 'qcode': 'IDN38100',
                                                'name': 'Road Weather Warning'},
                                               {'is_active': True, 'qcode': 'IDY21020',
                                                'name': 'Ocean Wind Warning'}]},
             {'_id': 'locators', 'items': [{'is_active': True, 'name': 'NSW', 'world_region': 'Oceania',
                                            'country': 'Australia',
              'state': 'New South Wales', 'qcode': 'NSW', 'group': 'Australia'}]}]

    def setUp(self):
        self.app.data.insert('vocabularies', self.vocab)

    def test_default_format(self):
        filename = filename = 'IDN38100.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'SOMETHING'
        self.items = BOMParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'Weather Road Weather Warning NSW: Issued 9:27am, July 5')

    def test_antartic_format(self):
        filename = filename = 'IDY21020.tst'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        self.provider['source'] = 'SOMETHING'
        self.items = BOMParser().parse(fixture, self.provider)
        self.assertEqual(self.items.get('headline'), 'Weather Ocean Wind Warning Antarctica: Issued 1859UTC, July 15')
