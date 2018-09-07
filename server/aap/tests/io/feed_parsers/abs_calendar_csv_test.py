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
from aap.io.feed_parsers.abs_calendar_csv import ABSCalendarCSVParser
from planning import init_app as planning_init_app


class ABSCalendarCSVTestCase(TestCase):

    filename = 'abs-calendar.txt'

    vocab = [{'_id': 'eventoccurstatus', 'items': [{
        "is_active": True,
        "qcode": "eocstat:eos5",
        "name": "Planned, occurs certainly"
    }]}, {'_id': 'event_calendars', 'items': [{"name": "ABS Statistics",
                                               "qcode": "abs statistics",
                                               "is_active": True}]}]

    def setUp(self):
        planning_init_app(self.app)
        self.app.data.insert('vocabularies', self.vocab)

        dirname = os.path.dirname(os.path.realpath(__file__))
        self.fixture = os.path.normpath(os.path.join(dirname, '../fixtures', self.filename))
        self.provider = {'name': 'Test'}

    def test_headline(self):
        items = ABSCalendarCSVParser().parse(self.fixture, self.provider)
        self.assertTrue(len(items) == 39)
        self.assertEqual(items[0].get('guid'), 'urn:www.abs.gov.au:4307.0.55.001-2016-17')
        self.assertEqual(items[0].get('calendars'), [{'name': 'ABS Statistics',
                                                      'qcode': 'abs statistics', 'is_active': True}])
        self.assertEqual(items[0].get('name'), 'Apparent Consumption of Alcohol, Australia, 2016-17')
