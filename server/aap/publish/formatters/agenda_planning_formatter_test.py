# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from unittest import mock

from superdesk.publish.formatters import Formatter
from superdesk.tests import TestCase
import datetime
import json
from .agenda_planning_formatter import AgendaPlanningFormatter
from planning import init_app as planning_init_app
from aap.agenda import init_app as init_agenda


@mock.patch('superdesk.publish.subscribers.SubscribersService.generate_sequence_number', lambda self, subscriber: 1)
class AgendaPlanningFormatterTest(TestCase):
    locations = [{
        "name": "Sydney",
        "unique_name": "Sydney, New South Wales, Australia",
        "address": {
            "country": "Australia",
            "line": [
                ""
            ],
            "locality": "Sydney"
        },
        "guid": "urn:newsml:localhost:2018-01-17T12:40:44.359182:a66130db-19c1-49e3-9d4d-5c12f97a4ed9",
    }]

    city_map = [{
        "country_id": 16,
        "agenda_id": 106,
        "name": "Sydney",
    }]

    iptc_map = [{
        "agenda_id": 1212,
        "iptc_code": "15073005",
    }]

    def setUp(self):
        self.formatter = AgendaPlanningFormatter()
        self.base_formatter = Formatter()
        planning_init_app(self.app)
        init_agenda(self.app)
        self.app.data.insert('locations', self.locations)
        self.app.data.insert('agenda_city_map', self.city_map)
        self.app.data.insert('agenda_iptc_map', self.iptc_map)

    def test_local(self):
        event = {
            "_id": "urn:newsml:localhost:2018-01-24T15:47:14.863195:040f5fce-f645-42f6-9253-97901d647886",
            "calendars": [
                {
                    "qcode": "finance",
                    "name": "Finance"
                }
            ],
            "dates": {
                "tz": "Australia/Sydney",
            },
            "name": "ABS Dwelling data",
            "definition_short": "release of dwelling data.",
            "guid": "urn:newsml:localhost:2018-01-24T15:47:14.863195:040f5fce-f645-42f6-9253-97901d647886",
            "state": "scheduled",
            "occur_status": {
                "qcode": "eocstat:eos5",
                "name": "Planned, occurs certainly",
                "label": "Confirmed"
            },
            "location": [
                {
                    "qcode": "urn:newsml:localhost:2018-01-17T12:40:44.359182:a66130db-19c1-49e3-9d4d-5c12f97a4ed9",
                    "address": {
                        "country": "Australia",
                        "title": None,
                        "line": [
                            ""
                        ],
                        "locality": "Sydney"
                    },
                    "name": "Sydney"
                }
            ],
            "slugline": "ABS DEWLLINGS",
            "type": "event",
            "definition_long": "long definition",
            "pubstatus": "usable",
            "subject": [
                {
                    "name": "Commonwealth Games",
                    "qcode": "15073005",
                    "parent": "15073000"
                }
            ]
        }
        event['dates']['start'] = datetime.datetime(2018, 1, 23, 13, 0, 0, 0)
        event['dates']['end'] = datetime.datetime(2018, 1, 24, 12, 59, 0, 0)
        doc = self.formatter.format(event, {'name': 'Test Subscriber'})[0]
        item = json.loads(doc[1])
        self.assertEqual(item.get('City').get('ID'), 106)
        self.assertEqual(item.get('Topics')[0].get('Topic').get('ID'), 1212)
        self.assertEqual(item.get('TimeFromZone'), '+11:00')
