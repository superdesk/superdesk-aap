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
    locations = [
        dict(name="Bombardier", unique_name="Sydney, New South Wales, Australia", address={
            "locality": "Victoria",
            "country": "Australia",
            "line": [
                "35-45 Frankston-Dandenong Road"
            ],
            "area": "Dandenong"},
            guid="urn:newsml:localhost:2018-01-17T12:40:44.359182:a66130db-19c1-49e3-9d4d-5c12f97a4ed9"),
        dict(guid="urn:newsml:localhost:2018-03-16T13:43:30.478955:d04fcfb9-469e-4494-99b2-a6cfba4ce6dc",
             name="City of London", address={"country": "United Kingdom", "line": [""], "locality": "City of London"},
             unique_name="City of London")]

    city_map = [{
        "country_id": 16,
        "agenda_id": 106,
        "name": "Dandenong",
    }]

    iptc_map = [{
        "agenda_id": 1212,
        "iptc_code": "15073005",
    }]

    contacts = [{
        "_id": 1,
        "is_active": True,
        "first_name": "John",
        "honorific": "Mr",
        "public": True,
        "contact_email": [
            "jdoe@a.com.au"
        ],
        "organisation": "AAP",
        "last_name": "Doe",
        "contact_phone": [
            {
                "public": True,
                "number": "02 5555 5555",
                "usage": "Business"
            }
        ],
        "mobile": [
            {
                "number": "1234567890",
                "public": True,
                "usage": "Business"
            }
        ],
        "job_title": "Spokesperson"
    }]

    def setUp(self):
        self.formatter = AgendaPlanningFormatter()
        self.base_formatter = Formatter()
        planning_init_app(self.app)
        init_agenda(self.app)
        self.app.data.insert('locations', self.locations)
        self.app.data.insert('agenda_city_map', self.city_map)
        self.app.data.insert('agenda_iptc_map', self.iptc_map)
        self.app.data.insert('contacts', self.contacts)

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
                    "qcode": "urn:newsml:localhost:2018-01-17T12:40:44.359182:a66130db-19c1-49e3-9d4d-5c12f97a4ed9"
                }],
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
            ],
            "event_contact_info": [1]
        }
        event['dates']['start'] = datetime.datetime(2018, 1, 23, 13, 0, 0, 0)
        event['dates']['end'] = datetime.datetime(2018, 1, 24, 12, 59, 0, 0)
        doc = self.formatter.format(event, {'name': 'Test Subscriber'})[0]
        item = json.loads(doc[1])
        self.assertEqual(item.get('City').get('ID'), 106)
        self.assertEqual(item.get('Topics')[0].get('Topic').get('ID'), 1212)
        self.assertEqual(item.get('TimeFromZone'), '+11:00')
        self.assertEqual(item.get('Contact').get('DisplayString'), 'Mr John Doe Spokesperson (AAP) '
                                                                   'jdoe@a.com.au Tel: 02 5555 5555 Mob: 1234567890')
        self.assertEqual(item.get('Address').get('DisplayString'), 'Bombardier, 35-45 Frankston-Dandenong Road, '
                                                                   'Dandenong, Victoria, Australia')

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
                    "assigned_to": {"user": "123"}
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
        self.assertEqual(item['Coverages'][0]['Resources'][0].get('ID'), '123')

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
                                   "43.338910:41af3708-33f1-46f6-9f05-626907e83fa0",
                    "assigned_to": {"user": "123"}
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
        self.assertEqual(item.get('Type'), 'event')
        self.assertEqual(item['Coverages'][0]['Resources'][0].get('ID'), '123')

    def test_place(self):
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
                    "qcode": "urn:newsml:localhost:2018-03-16T13:43:30.478955:d04fcfb9-469e-4494-99b2-a6cfba4ce6dc",
                    "name": "City of London",
                    "address": {
                        "country": "United Kingdom",
                        "line": [
                            ""
                        ],
                        "locality": "City of London"
                    }
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
            ],
            "place": [
                {
                    "world_region": "Oceania",
                    "group": "Australia",
                    "name": "NSW",
                    "state": "New South Wales",
                    "country": "Australia",
                    "qcode": "NSW"
                }
            ]
        }
        event['dates']['start'] = datetime.datetime(2018, 1, 23, 13, 0, 0, 0)
        event['dates']['end'] = datetime.datetime(2018, 1, 24, 12, 59, 0, 0)
        doc = self.formatter.format(event, {'name': 'Test Subscriber'})[0]
        item = json.loads(doc[1])
        self.assertEqual(item.get('City').get('DisplayString'), 'City of London')
        self.assertEqual(item.get('Topics')[0].get('Topic').get('ID'), 1212)
        self.assertEqual(item.get('TimeFromZone'), '+11:00')
        self.assertEqual(item.get('Region').get('ID'), 3)

    def test_planning_only(self):
        planning = {
            '_id': 'urn:newsml:localhost:2018-04-16T11:37:27.193250:ea06594b-e3e1-4064-9500-415968943356',
            'anpa_category': [
                {
                    'qcode': 'a',
                    'name': 'Australian General News'
                }
            ],
            'urgency': 5,
            'guid': 'urn:newsml:localhost:2018-04-16T11:37:27.193250:ea06594b-e3e1-4064-9500-415968943356',
            '_planning_schedule': [
                {
                    'coverage_id': None,
                    'scheduled': '2018-04-16T03:00:00.093Z'
                }
            ],
            'type': 'planning',
            'original_creator': '57bcfc5d1d41c82e8401dcc0',
            'subject': [
                {
                    'parent': '10003000',
                    'qcode': '10003001',
                    'name': 'organic foods'
                }
            ],
            'description_text': 'Monday Sushi day',
            'flags': {
                'marked_for_not_publication': False
            },
            'slugline': 'Lunch',
            'internal_note': 'get some seaweed as well',
            'coverages': [],
            'state': 'scheduled',
            'item_class': 'plinat:newscoverage',
            'agendas': [
                '59af943d1d41c8d43dddcf7b'
            ],
            'planning_date': '2018-04-16T03:00:00.093Z',
            'place': [
                {
                    'country': 'Australia',
                    'world_region': 'Oceania',
                    'state': 'New South Wales',
                    'qcode': 'NSW',
                    'name': 'NSW',
                    'group': 'Australia'
                }
            ],
            'pubstatus': 'usable'
        }
        planning['planning_date'] = datetime.datetime(2018, 4, 16, 3, 0, 0, 0)

        doc = self.formatter.format(planning, {'name': 'Test Subscriber'})[0]
        item = json.loads(doc[1])
        self.assertEqual(item.get('Title'), 'Lunch')

    def test_planning_long_internal_note(self):
        planning = {
            '_id': 'urn:newsml:localhost:2018-04-16T11:37:27.193250:ea06594b-e3e1-4064-9500-415968943356',
            'anpa_category': [
                {
                    'qcode': 'a',
                    'name': 'Australian General News'
                }
            ],
            'urgency': 5,
            'guid': 'urn:newsml:localhost:2018-04-16T11:37:27.193250:ea06594b-e3e1-4064-9500-415968943356',
            '_planning_schedule': [
                {
                    'coverage_id': None,
                    'scheduled': '2018-04-16T03:00:00.093Z'
                }
            ],
            'type': 'planning',
            'original_creator': '57bcfc5d1d41c82e8401dcc0',
            'subject': [
                {
                    'parent': '10003000',
                    'qcode': '10003001',
                    'name': 'organic foods'
                }
            ],
            'description_text': 'Monday Sushi day',
            'flags': {
                'marked_for_not_publication': False
            },
            'slugline': 'Lunch',
            'internal_note':
                'x' * 1000 + ' not this bit!',
            'coverages': [],
            'state': 'scheduled',
            'item_class': 'plinat:newscoverage',
            'agendas': [
                '59af943d1d41c8d43dddcf7b'
            ],
            'planning_date': '2018-04-16T03:00:00.093Z',
            'place': [
                {
                    'country': 'Australia',
                    'world_region': 'Oceania',
                    'state': 'New South Wales',
                    'qcode': 'NSW',
                    'name': 'NSW',
                    'group': 'Australia'
                }
            ],
            'pubstatus': 'usable'
        }
        planning['planning_date'] = datetime.datetime(2018, 4, 16, 3, 0, 0, 0)

        doc = self.formatter.format(planning, {'name': 'Test Subscriber'})[0]
        item = json.loads(doc[1])
        self.assertEqual(len(item.get('SpecialInstructions')), 1000)

    def test_planning_with_event_event_first(self):
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
            "internal_note": "A planning item",
            'unique_id': "1234"
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

        doc = self.formatter.format(event, {'name': 'Test Subscriber'})[0]
        item = json.loads(doc[1])
        events = self.app.data.find('events', None, None)
        self.assertEqual(events[0][0]['unique_id'], '1234')
        self.assertEqual(item.get('Title'), 'Superdesk Planning')
        self.assertEqual(len(item.get('Coverages')), 1)
        self.assertEqual(item.get('Type'), 'event')

    def test_missing_mapping_for_content_types(self):
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
                        "g2_content_type": "bogus",
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
                    }
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
        self.assertEqual(item.get('Coverages')[0]['Role'], {'ID': 1})
