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
from .pollution_report import generate_pollution_story
from datetime import datetime


class AMServiceTestCase(TestCase):

    desks = [
        {
            "desk_type": "production",
            "name": "Politic Desk",
            "members": [],
            "desk_metadata": {},
            "description": "Test",
            "source": "AAP",
            "content_profiles": {},
            "content_expiry": 1440
        }
    ]

    articles = [
        {
            'guid': '123', '_id': '123',
            'type': 'text',
            'body_html': '<p>FORECAST FOR SYDNEY POLLUTION ISSUED {{time}} {{date}}</p><p>Today the Air Quality '
                         'Index Levels between {{time_range}} in Sydney were as follows:</p><p><br></p><p>'
                         '{{sydney_east_description}} in Sydney East with an index of {{sydney_east_value}},'
                         '</p><p>{{sydney_north_west_description}} in Sydney North West with an index of '
                         '{{sydney_north_west_value}}</p><p>{{sydney_south_west_description}} in Sydney South West'
                         ' with an index of {{sydney_south_west_value}} and</p><p><br></p><p>Air Quality Index '
                         'levels are '
                         'forecast to be {{sydney_forecast}} {{forecast_day}}</p><p><br></p><p>The pollution levels '
                         'in Wollongong were as follows:</p><p>{{wollongong_description}} in Wollongong City '
                         'with an index of {{wollongong_value}}</p><p>{{albion_park_sth_decsription}} in Albion'
                         ' Park with an index of {{albion_park_sth_value}}</p><p><br></p><p>The pollution levels '
                         'in Newcastle were as follows:</p><p>{{wallsend_description}} in Wallsend with an '
                         'index of {{wallsend_value}}</p><p>{{newcastle_description }} Newcastle City '
                         'with an index of {{newcastle_value}}</p><p>{{beresfield_description}} in Beresfield '
                         'with an index of {{beresfield_value}}</p>',
            'headline': 'Sydney pollution forecast issued {{time}}',
            'anpa_take_key': 'Sydney {{time}}',
            'abstract': 'abstract',
            'state': 'in_progress',
            '_current_version': 1,
            'unique_id': 1,
            'unique_name': '#1',
            'versioncreated': datetime(year=2018, month=8, day=1, hour=12, minute=12, second=0, microsecond=0)
        }
    ]

    validators = [
        {
            'schema': {},
            'type': 'text',
            'act': 'publish',
            '_id': 'publish_text'
        },
        {
            '_id': 'publish_composite',
            'act': 'publish',
            'type': 'composite',
            'schema': {}
        }
    ]

    def setUp(self):
        self.app.data.insert('desks', self.desks)
        for article in self.articles:
            article['task'] = {
                'desk': self.desks[0].get('_id'),
                'stage': self.desks[0].get('incoming_stage')
            }
        self.app.data.insert('archive', self.articles)
        self.app.data.insert('validators', self.validators)

    def test_parse_web_page(self):
        item = generate_pollution_story(self.articles[0])
        self.assertTrue('Very good in Sydney East' in item['body_html'] or
                        'Good in Sydney East' in item['body_html'] or
                        'Fair in Sydney East' in item['body_html'] or
                        'Poor in Sydney East' in item['body_html'] or
                        'Very poor in Sydney East' in item['body_html'] or
                        'Hazardous in Sydney East' in item['body_html'])
        self.assertTrue('Air Quality Index levels are forecast to be VERY GOOD' in item['body_html'] or
                        'Air Quality Index levels are forecast to be GOOD' in item['body_html'] or
                        'Air Quality Index levels are forecast to be FAIR' in item['body_html'] or
                        'Air Quality Index levels are forecast to be POOR' in item['body_html'] or
                        'Air Quality Index levels are forecast to be VERY POOR' in item['body_html'] or
                        'Air Quality Index levels are forecast to be HAZARDOUS' in item['body_html'])
