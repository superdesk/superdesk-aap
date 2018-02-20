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

    def test_planning(self):
        planning = {
            "_id": "urn:newsml:localhost:2018-02-15T12:38:14.817988:baf0fa2b-b4c6-46ca-94b6-0ac95083a260",
            "subject": [
                {
                    "name": "education",
                    "qcode": "05000000",
                    "parent": None
                }
            ],
            "type": "planning",
            "guid": "urn:newsml:localhost:2018-02-15T12:38:14.817988:baf0fa2b-b4c6-46ca-94b6-0ac95083a260",
            "ednote": "ed notes",
            "original_creator": "57bcfc5d1d41c82e8401dcc0",
            "description_text": "Test Description",
            "coverages": [
                {
                    "planning": {
                        "slugline": "TEST",
                        "scheduled": "REPLACE ME",
                        "g2_content_type": "text",
                        "genre": [
                            {
                                "name": "Article (news)",
                                "qcode": "Article"
                            }
                        ]
                    },
                    "news_coverage_status": {
                        "label": "Planned",
                        "name": "coverage intended",
                        "qcode": "ncostat:int"
                    },
                    "coverage_id": "urn:newsml:localhost:2018-02-15T12:38:15.344350:"
                                   "af31ffb9-d0f7-4c42-9a62-598b55dbf808",
                }
            ],
            "urgency": 2,
            "state": "scheduled",
            "flags": {
                "marked_for_not_publication": False
            },
            "internal_note": "internal note",
            "slugline": "TEST",
            "agendas": [],
            "item_class": "plinat:newscoverage",
            "anpa_category": [
                {
                    "name": "Australian General News",
                    "qcode": "a"
                }
            ],
            "_planning_schedule": [
                {
                    "coverage_id": "urn:newsml:localhost:2018-02-15T12:38:15.344350:"
                                   "af31ffb9-d0f7-4c42-9a62-598b55dbf808"
                }
            ],
            "pubstatus": "usable"
        }
        planning['coverages'][0]['planning']['scheduled'] = datetime.datetime(2018, 1, 23, 13, 0, 0, 0)
        doc = self.formatter.format(planning, {'name': 'Test Subscriber'})[0]
        item = json.loads(doc[1])
        self.assertEqual(item.get('Title'), 'TEST')

    def test_planning_with_event(self):
        planning = {
            "_id": "urn:newsml:localhost:2018-02-19T13:46:51.861773:edf0e41f-524e-4f14-b416-6183e25fd067",
            "slugline": "SHOW AND TELL",
            "headline": "Superdesk - Show & Tell",
            "type": "planning",
            "coverages": [
                {
                    "news_coverage_status": {
                        "name": "coverage intended",
                        "qcode": "ncostat:int",
                        "label": "Planned"
                    },
                    "original_creator": "57bcfc5d1d41c82e8401dcc0",
                    "planning": {
                        "scheduled": "REPLACE",
                        "g2_content_type": "text"
                    },
                    "coverage_id": "urn:newsml:localhost:2018-02-19T13:47:"
                                   "43.338910:41af3708-33f1-46f6-9f05-626907e83fa0"
                }
            ],
            "description_text": "Superdesk - Show & Tell",
            "flags": {
                "marked_for_not_publication": False
            },
            "item_class": "plinat:newscoverage",
            "guid": "urn:newsml:localhost:2018-02-19T13:46:51.861773:edf0e41f-524e-4f14-b416-6183e25fd067",
            "state": "draft",
            "pubstatus": "usable",
            "event_item": "urn:newsml:localhost:2018-02-16T12:56:39.270372:02da2a3e-d5bc-4ab4-9fef-3fd78a0935fd",
            "internal_note": "A planning item"
        }
        planning['coverages'][0]['planning']['scheduled'] = datetime.datetime(2018, 1, 23, 13, 0, 0, 0)

        event = {
            "_id": "urn:newsml:localhost:2018-02-16T12:56:39.270372:02da2a3e-d5bc-4ab4-9fef-3fd78a0935fd",
            "state": "scheduled",
            "source": "Events",
            "ingest_provider": "5a7b968d1d41c846dadaa3ce",
            "ingest_provider_sequence": "1240",
            "family_id": "urn:newsml:localhost:2018-02-16T12:56:39.248135:bbe61f6b-92dd-4101-b653-89d8ceb767b8",
            "type": "event",
            "format": "preserved",
            "occur_status": {
                "name": "Planned, occurs certainly",
                "qcode": "eocstat:eos5",
                "label": "Confirmed"
            },
            "location": [
                {
                    "geo": "",
                    "name": "Rhodes 5.5 IT Conference (CB)",
                    "qcode": ""
                }
            ],
            "_etag": "faec457578cf076c7aed71647ab67699af651fed",
            "recurrence_id": "urn:newsml:localhost:2018-02-16T12:56:39.252448:eb55544c-685b-4204-b784-6a53731cd1c6",
            "definition_short": "Superdesk Planning",
            "dates": {
                "recurring_rule": {
                    "byday": "MO",
                    "frequency": "WEEKLY",
                    "interval": 2
                },
                "tz": "Australia/Sydney",
            },
            "name": "Superdesk Planning",
            "organizer": [
                {
                    "name": "mailto:mdhamanwala@aap.com.au",
                    "qcode": ""
                }
            ],
            "definition_long": "long string",
            "guid": "urn:newsml:localhost:2018-02-16T12:56:39.270372:02da2a3e-d5bc-4ab4-9fef-3fd78a0935fd",
            "calendars": [
                {
                    "qcode": "entertainment",
                    "name": "Entertainment"
                }
            ],
            "slugline": "superdesk planning",
            "pubstatus": "usable"
        }
        event['dates']['start'] = datetime.datetime(2018, 1, 23, 13, 0, 0, 0)
        event['dates']['end'] = datetime.datetime(2018, 1, 24, 12, 59, 0, 0)
        self.app.data.insert('events', [event])
        self.app.data.insert('planning', [planning])

        doc = self.formatter.format(planning, {'name': 'Test Subscriber'})[0]
        item = json.loads(doc[1])
        self.assertEqual(item.get('Title'), 'Superdesk Planning')
        self.assertEqual(len(item.get('Coverages')), 1)
