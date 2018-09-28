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
from .traffic import traffic_story
from aap.traffic_incidents import init_app
from superdesk.utc import utcnow
from datetime import timedelta
import os


class TrafficTestCase(TestCase):
    incident = [{
        "_id": "5ba851f41d41c846143c91f8",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [
                    151.22122,
                    -33.83105
                ],
                [
                    151.2217,
                    -33.83124
                ],
                [
                    151.2218,
                    -33.83125
                ],
                [
                    151.22229,
                    -33.83142
                ],
                [
                    151.22238,
                    -33.83149
                ]
            ]
        },
        "state": "NSW",
        "incident_description": "Roadworks on Military Road Westbound in Neutral Bay between Young "
                                "Street and Wycombe Road.",
        "to_cross_street_name": "Wycombe Road",
        "incident_type": "Roadworks",
        "to_street_name": "Military Road",
        "guid": 465485,
        "from_crossStreet_ame": "Young Street",
        "from_street_name": "Military Road",
        "city": "Neutral Bay"
    }, {
        "_id": "5ba851f41d41c846143c924e",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [
                    151.04451,
                    -33.842
                ],
                [
                    151.04466,
                    -33.84186
                ],
                [
                    151.0447,
                    -33.84169
                ],
                [
                    151.04481,
                    -33.84162
                ],
                [
                    151.04495,
                    -33.84141
                ],
                [
                    151.04506,
                    -33.8412
                ],
                [
                    151.04535,
                    -33.84089
                ],
                [
                    151.04555,
                    -33.84059
                ],
                [
                    151.04609,
                    -33.83994
                ]
            ]
        },
        "state": "NSW",
        "incident_description": "Broken down lorr(y/ies) on Silverwater Road Southbound in Silverwater (sydney) "
                                "between Western Motorway and Carnarvon Street.",
        "to_cross_street_name": "Carnarvon Street",
        "incident_type": "Broken down lorr(y/ies)",
        "_etag": "332f784019f1dbd9b74f6d84c56d98fc71b25cdf",
        "to_street_name": "Silverwater Road",
        "guid": 470748,
        "from_crossStreet_ame": "Western Motorway",
        "from_street_name": "Silverwater Road",
        "city": "Silverwater (sydney)",
    }]

    def setUp(self):
        init_app(self.app)
        self.incident[0]['start_date'] = utcnow() - timedelta(hours=10)
        self.incident[0]['end_date'] = utcnow() + timedelta(hours=100)
        self.incident[1]['start_date'] = utcnow() - timedelta(hours=10)
        self.incident[1]['end_date'] = utcnow() + timedelta(hours=100)
        self.app.data.insert('traffic_incidents', self.incident)
        self.app.config['INIT_DATA_PATH'] = os.path.abspath(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../data'))

    def test_roadworks(self):
        item = traffic_story({'place': [{'qcode': 'NSW'}], 'body_html': 'road works go here {{roadworks}}'})
        self.assertEqual(item.get('body_html'),
                         'road works go here <p><b>North</b></p><p>Roadworks on Military Road Westbound in '
                         'Neutral Bay between Young Street and Wycombe Road.</p>')

    def test_incidents(self):
        item = traffic_story({'place': [{'qcode': 'NSW'}], 'body_html': 'incidents go here {{incidents}}'})
        self.assertEqual(item.get('body_html'),
                         'incidents go here <p><b>West</b></p><p>Broken down truck on Silverwater Road '
                         'Southbound in Silverwater (sydney) between Western Motorway and Carnarvon Street.</p>')
