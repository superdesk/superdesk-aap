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
import requests
import json
from io import StringIO
from flask import render_template_string
from superdesk.utils import config
from superdesk import get_resource_service
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE
from flask import current_app as app


logger = logging.getLogger(__name__)


def expand_brisbane_traffic(item, **kwargs):
    metro = StringIO()
    regional = StringIO()

    response = requests.get('https://api.qldtraffic.qld.gov.au/v1/events?apikey={}'.format(
        app.config.get('QLD_TRAFFIC_API_KEY', '')))

    data = json.loads(response.content.decode('UTF-8'))
    for feature in data.get('features'):
        if feature.get('properties').get('event_type') in (
                'Crash', 'Hazard', 'Congestion', 'Flooding'):
            properties = feature.get('properties')
            road = properties.get('road_summary')
            impact = properties.get('impact')
            incident = '<p>{}: {}, {} {} {} {}</p>'.format(feature.get('properties').get('event_type'),
                                                           feature.get('properties').get('event_subtype'),
                                                           road.get('road_name'), road.get('locality'),
                                                           impact.get('direction'),
                                                           properties.get('description') if properties.get(
                                                               'description') else '')
            if 'Metropolitan' in feature.get('properties').get('road_summary').get('district'):
                metro.write(incident)
            elif 'NSW' not in feature.get('properties').get('road_summary').get('district'):
                regional.write(incident)

    incidents_map = {'alerts_metro': metro.getvalue(), 'alerts_regional': regional.getvalue()}
    metro.close()
    regional.close()
    item['body_html'] = render_template_string(item.get('body_html', ''), **incidents_map)

    # If the macro is being executed by a scheduled template then publish the item as well
    if 'desk' in kwargs and 'stage' in kwargs:
        update = {'body_html': item.get('body_html', '')}
        get_resource_service('archive').system_update(item[config.ID_FIELD], update, item)

        get_resource_service('archive_publish').patch(id=item[config.ID_FIELD],
                                                      updates={ITEM_STATE: CONTENT_STATE.PUBLISHED,
                                                      'auto_publish': True})
        return get_resource_service('archive').find_one(req=None, _id=item[config.ID_FIELD])

    return item


name = 'Brisbane Traffic'
label = 'Brisbane Traffic'
callback = expand_brisbane_traffic
access_type = 'frontend'
action_type = 'direct'
group = 'AM Desk'
