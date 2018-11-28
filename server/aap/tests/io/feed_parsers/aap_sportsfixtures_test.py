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
from superdesk.etree import etree
from aap.io.feed_parsers.aap_sportsfixtures import AAPSportsFixturesParser
from superdesk.tests import TestCase
from planning import init_app as planning_init_app


class SportsAPITestCase(TestCase):
    vocab = [{'_id': 'eventoccurstatus', 'items': [{
        "is_active": True,
        "qcode": "eocstat:eos5",
        "name": "Planned, occurs certainly"
    }]}, {'_id': 'event_calendars', 'items': [{"name": "Sport Fixtures",
                                               "qcode": "sport",
                                               "is_active": True},
                                              {"name": "Sport",
                                               "qcode": "sportgeneral",
                                               "is_active": True}]}]

    location = [{
        "_id": "593604461d41c8ad06c1d489",
        "position": {
            "latitude": -34.91560245,
            "altitude": 0.0,
            "longitude": 138.596080040469
        },
        "name": "Adelaide Oval, War Memorial Drive, North Adelaide, 5006, City of Adelaide, South Australia, "
                "5006, Australia",
        "original_creator": "",
        "unique_name": "Adelaide Oval, Adelaide",
        "address": {
            "postal_code": "5006",
            "area": "North Adelaide",
            "country": "Australia",
            "locality": "5006",
            "external": {
                "nominatim": {
                    "lat": "-34.91560245",
                    "osm_type": "way",
                    "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://www.openstreetmap.org/copyright",
                    "importance": 0.301,
                    "address": {
                        "postcode": "5006",
                        "country": "Australia",
                        "city": "5006",
                        "country_code": "au",
                        "road": "War Memorial Drive",
                        "stadium": "Adelaide Oval",
                        "county": "City of Adelaide",
                        "state": "South Australia",
                        "suburb": "North Adelaide"
                    },
                    "type": "stadium",
                    "lon": "138.596080040469",
                    "display_name": "Adelaide Oval, War Memorial Drive, North Adelaide, 5006, City of Adelaide, "
                                    "South Australia, 5006, Australia",
                    "osm_id": "268922032",
                    "class": "leisure",
                    "place_id": "131442053",
                    "boundingbox": [
                        "-34.9171497",
                        "-34.9142795",
                        "138.5946145",
                        "138.5974148"
                    ]
                }
            }
        },
        "guid": "urn:newsml:localhost:2017-06-06T11:24:22.029546:0aaa5460-9a78-41c9-aad0-57c808a35114"
    }]

    def setUp(self):
        planning_init_app(self.app)
        self.app.data.insert('vocabularies', self.vocab)
        self.app.data.insert('locations', self.location)

    def test_fixtures(self):
        filename = 'aap_soccer.xml'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        with open(fixture, 'rb') as f:
            self.xml = f.read()
            fixture = {'fixture_xml': etree.fromstring(self.xml), 'sport_id': '4',
                       'sport_name': 'Soccer', 'comp_name': 'Qualifiers', 'comp_id': 'int-314'}
            items = AAPSportsFixturesParser().parse(fixture, None)
            self.assertTrue(len(items) == 5)

    def test_fixture_list_with_dates(self):
        filename = 'aap_golf.xml'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        with open(fixture, 'rb') as f:
            self.xml = f.read()
            fixture = {'fixture_xml': etree.fromstring(self.xml), 'sport_id': '8',
                       'sport_name': 'Golf', 'comp_name': 'D+D Real Czech Masters', 'comp_id': 'int-26669'}
            items = AAPSportsFixturesParser().parse(fixture, None)
            self.assertTrue(len(items) == 1)
            self.assertEqual(items[0].get('calendars')[0].get('qcode'), 'sport')
            self.assertEqual(items[0].get('calendars')[1].get('qcode'), 'sportgeneral')

    def test_fixture_list_with_no_dates(self):
        filename = 'aap_cricket.xml'
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', filename))
        with open(fixture, 'rb') as f:
            self.xml = f.read()
            fixture = {'fixture_xml': etree.fromstring(self.xml), 'sport_id': '3',
                       'sport_name': 'Cricket', 'comp_name': 'Champions Trophy in England/Wales', 'comp_id': 'dom-436'}
            items = AAPSportsFixturesParser().parse(fixture, None)
            self.assertTrue(len(items) == 2)
