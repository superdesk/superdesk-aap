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
from .intelematics_fuel import fuel_story
from aap.fuel import init_app
from datetime import datetime
import os


class FuelTestCase(TestCase):
    fuel = [{
        "_id": 1,
        "address": {
            "country": "AUS",
            "suburb": "Bronx",
            "state": "NSW",
            "street": "9 Wallaby Way"
        },
        "price": 113.9,
        "sample_date": datetime.now().isoformat()[:10],
        "location": {
            "coordinates": [
                151.1491,
                -33.8971
            ],
            "type": "Point"
        },
        "market": "Sydney",
        "fuel_type": "ULP",
    }]

    provider = [{
        "_id": 1,
        "name": "Intelematics Fuel",
        "config": {
            "api_url": "http://a.b.c/incidents/rest/all.geojson",
        },
        "content_types": [],
        "feeding_service": "intelematics_incident_api_feed",
        "source": "Intelematics"
    }]

    item = [{'_id': 1, 'place': [{'qcode': 'NSW'}], 'body_html': '{{sydney_max_ulp}} '
                                                                 '{{sydney_avg_ulp}} '
                                                                 '{{sydney_min_ulp}} '
                                                                 '{{sydney_cheap_ulp}}'}]

    def setUp(self):
        init_app(self.app)
        self.app.data.insert('fuel', self.fuel)
        self.app.data.insert('ingest_providers', self.provider)
        self.app.data.insert('archive', [{'_id': 1}])
        self.app.config['INIT_DATA_PATH'] = os.path.abspath(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../data'))

    def test_min(self):
        item = fuel_story(self.item[0])
        self.assertEqual(item.get('body_html'), '113.9 113.9 113.9 Bronx')

    def test_area(self):
        item = fuel_story({'_id': 1, 'place': [{'qcode': 'NSW'}], 'body_html': '{{sydney_inner_west_max_ulp}} '
                                                                               '{{sydney_inner_west_avg_ulp}} '
                                                                               '{{sydney_inner_west_min_ulp}} '
                                                                               '{{sydney_inner_west_cheap_ulp}}'})
        self.assertEqual(item.get('body_html'), '113.9 113.9 113.9 Bronx')
