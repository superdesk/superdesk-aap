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
from .fuel import get_areas

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

        incidents = service.get_from_mongo(req=req, lookup=incident_query)
        if incidents.count():
            incidents_html += '<p><b>{}</b></p>'.format(area['properties']['area'])
            for i in incidents:
                incidents_html += '<p>{}</p>'.format(i.get('incident_description'))

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

    return item


name = 'Traffic Information'
label = 'Traffic Information'
callback = traffic_story
access_type = 'frontend'
action_type = 'direct'
