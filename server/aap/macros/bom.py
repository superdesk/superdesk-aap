# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
import xml.etree.ElementTree as et
from flask import render_template_string
from superdesk.utils import config
from superdesk import get_resource_service
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE
from datetime import datetime
from superdesk.ftp import ftp_connect
from io import BytesIO
from flask import current_app as app


logger = logging.getLogger(__name__)

# This is a list of the names of the forecast locations that we are interested in
met_forecast_areas = {'NSW': ['Sydney', 'Parramatta', 'Campbelltown', 'Penrith', 'Wollongong', 'Newcastle'],
                      'QLD': ['Brisbane', 'Gold Coast Seaway', 'Cairns', 'Gladstone', 'Mount Isa'],
                      'VIC': ['Melbourne', 'Phillip Island', 'Geelong', 'Ballarat', 'Wilsons Promontory'],
                      'SA': ['Adelaide', 'Whyalla', 'Coober Pedy', 'Port Augusta', 'Mount Gambier'],
                      'WA': ['Perth', 'Margaret River', 'Geraldton', 'Broome', 'Kalgoorlie']}

# This is a list of the names ov the available observation stations
met_observation_stations = {'NSW': ['Sydney - Observatory Hill', 'Sydney Olympic Park', 'Parramatta', 'Campbelltown',
                                    'Penrith', 'Albion Park', 'Newcastle University', 'Newcastle Nobbys'],
                            'QLD': ['Brisbane', 'Gold Coast Seaway', 'Cairns', 'Gladstone', 'Mount Isa'],
                            'VIC': ['Melbourne (Olympic Park)', 'Rhyll', 'Geelong Racecourse', 'Ballarat',
                                    'Wilsons Promontory'],
                            'SA': ['Adelaide (West Terrace /  ngayirdapira)', 'Whyalla', 'Coober Pedy Airport',
                                   'Port Augusta', 'Mount Gambier'],
                            'WA': ['Perth', 'Witchcliffe', 'Geraldton Airport', 'Broome', 'Kalgoorlie-Boulder']}

forecast_files = {'NSW': 'IDN11060.xml',
                  'QLD': 'IDQ11295.xml',
                  'SA': 'IDS10044.xml',
                  'VIC': 'IDV10753.xml',
                  'WA': 'IDW14199.xml'}

observation_files = {'NSW': 'IDN60920.xml',
                     'QLD': 'IDQ60920.xml',
                     'SA': 'IDS60920.xml',
                     'VIC': 'IDV60920.xml',
                     'WA': 'IDW60920.xml'}


def forecast_story(item, **kwargs):

    def _get_file(filename):
        raw = BytesIO()
        with ftp_connect({'username': app.config.get('BOM_WEATHER_FTP_USERNAME', ''),
                          'password': app.config.get('BOM_WEATHER_FTP_PASSWORD', ''),
                          'host': 'ftp.bom.gov.au',
                          'path': 'fwo'}) as ftp:
            ftp.retrbinary('RETR ' + filename, raw.write)
        return raw.getvalue()

    def _get_forecast(state):
        return _get_file(forecast_files.get(state))

    def _get_observations(state):
        return _get_file(observation_files.get(state))

    def add_value(period, dict, name, base):

        direction_map = {'N': 'north', 'NNE': 'north-northeast', 'NE': 'northeast', 'ENE': 'east-northeast',
                         'E': 'east', 'ESE': 'east-southeast', 'SE': 'southeast', 'SSE': 'south-southeast',
                         'S': 'south', 'SSW': 'south-southwest', 'SW': 'southwest', 'WSW': 'west-southwest',
                         'W': 'west', 'WNW': 'west-northwest', 'NW': 'northwest', 'NNW': 'north-northwest'}

        try:
            node = period.find('.//*[@type="{}"]'.format(name))
            if not node:
                period.get(name)
            value = node.text
            if 'temperature' in name:
                value = value.replace('.0', '')
            if 'precis' in name:
                value = value.replace('.', '')
            if 'wind_dir' == name:
                value = direction_map.get(value)
            if node is not None:
                dict['{}{}'.format(base, name).replace('-', '_')] = value
        except Exception:
            dict['{}{}'.format(base, name).replace('-', '_')] = 'N/A'

    # The place is used to determine the state the the requests will be limited to
    if 'place' in item and len(item.get('place')):
        state = item.get('place')[0].get('qcode').upper()
    else:
        return

    forecast_xml = _get_forecast(state)

    forecast_dict = dict()
    xml = et.fromstring(forecast_xml)
    s = xml.find('.forecast')
    if s is not None:
        for area in met_forecast_areas.get(state):
            location = s.find('.//area[@description="{}"]'.format(area))
            if location is not None:
                location_name = location.get('description')
                for period in location.findall('.//forecast-period'):
                    index = period.attrib.get('index')
                    base_str = '{}_{}_'.format(location_name.replace(' ', '_'), index)

                    forecast_dict['{}start'.format(base_str)] = period.attrib.get('start-time-local')
                    forecast_dict['{}weekday'.format(base_str)] = datetime.strptime(
                        period.attrib.get('start-time-local')[:10], '%Y-%m-%d').strftime('%A')
                    forecast_dict['{}end'.format(base_str)] = period.attrib.get('end-time-local')

                    add_value(period, forecast_dict, 'precis', base_str)
                    add_value(period, forecast_dict, 'air_temperature_minimum', base_str)
                    add_value(period, forecast_dict, 'air_temperature_maximum', base_str)
                    add_value(period, forecast_dict, 'probability_of_precipitation', base_str)
                    add_value(period, forecast_dict, 'precipitation_range', base_str)
                    add_value(period, forecast_dict, 'forecast_icon_code', base_str)

    current_xml = _get_observations(state)
    xml = et.fromstring(current_xml)
    s = xml.find('.observations')
    if s is not None:
        for station in met_observation_stations.get(state):
            station = s.find('.//station[@description="{}"]'.format(station))
            if station is not None:
                location_name = station.get('description')
                base_str = '{}_obs_'.format(
                    location_name.replace(' ', '_').replace('/', '_').replace('(', '_').replace(')', '_'))
                observation = station.find('.period')
                add_value(observation, forecast_dict, 'time-local', base_str)
                observation = observation.find('.level')
                add_value(observation, forecast_dict, 'air_temperature', base_str)
                add_value(observation, forecast_dict, 'apparent_temp', base_str)
                add_value(observation, forecast_dict, 'rel-humidity', base_str)
                add_value(observation, forecast_dict, 'wind_spd_kmh', base_str)
                add_value(observation, forecast_dict, 'wind_dir', base_str)

    item['body_html'] = render_template_string(item.get('body_html', ''), **forecast_dict)

    update = {'source': 'BOM'}
    update['body_html'] = item['body_html']
    get_resource_service('archive').system_update(item[config.ID_FIELD], update, item)
    item['source'] = 'BOM'

    # If the macro is being executed by a scheduled template then publish the item as well
    if 'desk' in kwargs and 'stage' in kwargs:
        get_resource_service('archive_publish').patch(id=item[config.ID_FIELD],
                                                      updates={ITEM_STATE: CONTENT_STATE.PUBLISHED,
                                                      'auto_publish': True})
        return get_resource_service('archive').find_one(req=None, _id=item[config.ID_FIELD])

    return item


name = 'bom weather forecast'
label = 'BOM Weather Forecast/Observations'
callback = forecast_story
access_type = 'frontend'
action_type = 'direct'
group = 'AM Desk'
