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
from superdesk import get_resource_service
from eve.utils import ParsedRequest
import re
from flask import render_template_string
from datetime import timedelta
from superdesk.utc import utcnow
from copy import deepcopy
from .intelematics_fuel import get_areas
from superdesk.utils import config
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE

logger = logging.getLogger(__name__)


def traffic_story(item, **kwargs):

    # The place is used to determine the state the the requests will be limited to
    if 'place' in item and len(item.get('place')):
        state = item.get('place')[0].get('qcode').upper()
    else:
        return

    # Current time in UTC to restrict the query to incidents that are currently active
    today = utcnow()
    # Also include incidents that started in the last 24 hours
    yesterday = today - timedelta(hours=24)
    service = get_resource_service('traffic_incidents')
    req = ParsedRequest()
    areas = get_areas().get('features')
    incidents_map = dict()
    incidents_html = ''
    roadworks_html = ''

    # Scan the areas in the state.
    for area in [a for a in areas if a.get('properties', {}).get('state', '').upper() == state]:
        base_query = {'$and': [{'state': state},
                               {'end_date': {'$gt': today}},
                               {'start_date': {'$lt': today, '$gt': yesterday}},
                               {'incident_type': {'$ne': 'This message is for test purposes only , please ignore'}},
                               {'geometry': {
                                   '$geoIntersects': {
                                       '$geometry': {
                                           'type': 'Polygon',
                                           'coordinates': area.get('geometry').get('coordinates')
                                       }
                                   }
                               }}
                               ]}
        incident_query = deepcopy(base_query)
        # Append clauses that will exclude road works
        incident_query['$and'] += [{'incident_type': {'$ne': 'Roadworks'}},
                                   {'incident_description': {
                                       '$not': re.compile('.*{}.*'.format('Maintenance work'), re.IGNORECASE)}},
                                   {'incident_description': {
                                       '$not': re.compile('.*{}.*'.format('Roadworks'), re.IGNORECASE)}}]

        # Attempt to remove the reporting of apparently permanently closed roads in Brisbane and Perth
        if state == 'WA':
            incident_query['$and'].append({'incident_description': {'$ne': 'Closed on Brearley Avenue Eastbound in '
                                                                           'Perth between Great Eastern '
                                                                           'Highway and Second Street.'}})
            incident_query['$and'].append({'incident_description': {'$ne': 'Closed on Brearley Avenue Westbound in '
                                                                           'Perth between Second Street and Great '
                                                                           'Eastern Highway.'}})
        if state == 'QLD':
            incident_query['$and'].append({'incident_description': {'$ne': 'Entry slip road closed on Sandgate Road '
                                                                    'Northbound in Brisbane between Holroyd '
                                                                    'Street and Gateway Motorway.'}})
            incident_query['$and'].append({'incident_description': {'$ne': 'Closed on William Street '
                                                                           'Northbound in Brisbane '
                                                                    'between Margaret Street and Elizabeth Street.'}})
            incident_query['$and'].append({'incident_description': {'$ne': 'Closed on William Street South '
                                                                           'Bound in Brisbane '
                                                                    'between Elizabeth Street and Margaret Street.'}})

        incidents = service.get_from_mongo(req=req, lookup=incident_query)
        if incidents.count():
            incidents_html += '<p><b>{}</b></p>'.format(area['properties']['area'])
            for i in incidents:
                message = i.get('incident_description').replace('lorr(y/ies)', 'truck')
                message = message.replace('Accident(s)', 'Accident')
                incidents_html += '<p>{}</p>'.format(message)

        roadworks_query = deepcopy(base_query)
        # Append a clause that restrict to roadworks only
        roadworks_query['$and'].append({'$or': [
            {'incident_type': 'Roadworks'},
            {'incident_description': re.compile('.*{}.*'.format('Maintenance work'), re.IGNORECASE)},
            {'incident_description': re.compile('.*{}.*'.format('Roadworks'), re.IGNORECASE)}
        ]})

        roadworks = service.get_from_mongo(req=req, lookup=roadworks_query)
        if roadworks.count():
            roadworks_html += '<p><b>{}</b></p>'.format(area['properties']['area'])
            for i in roadworks:
                roadworks_html += '<p>{}</p>'.format(i.get('incident_description'))

    incidents_map['incidents'] = 'No incidents at this time.' if incidents_html == '' else incidents_html
    incidents_map['roadworks'] = 'No roadworks at this time.' if roadworks_html == '' else roadworks_html

    item['body_html'] = render_template_string(item.get('body_html', ''), **incidents_map)
    update = {'source': 'Intelematics'}
    ingest_provider = get_resource_service('ingest_providers').find_one(req=None, source='Intelematics')
    if ingest_provider:
        update['ingest_provider'] = ingest_provider.get(config.ID_FIELD)
    update['body_html'] = item['body_html']
    get_resource_service('archive').system_update(item[config.ID_FIELD], update, item)
    item['source'] = 'Intelematics'

    # If the macro is being executed by a scheduled template then publish the item as well
    if 'desk' in kwargs and 'stage' in kwargs:
        get_resource_service('archive_publish').patch(id=item[config.ID_FIELD],
                                                      updates={ITEM_STATE: CONTENT_STATE.PUBLISHED,
                                                      'auto_publish': True})
        return get_resource_service('archive').find_one(req=None, _id=item[config.ID_FIELD])

    return item


name = 'Traffic Information'
label = 'Traffic Information'
callback = traffic_story
access_type = 'frontend'
action_type = 'direct'
