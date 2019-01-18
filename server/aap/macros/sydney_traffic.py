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
from flask import current_app as app
from superdesk.utils import config
from superdesk import get_resource_service
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE

logger = logging.getLogger(__name__)


def expand_sydney_traffic_congestion(item, **kwargs):
    metro = StringIO()
    north = StringIO()
    south = StringIO()
    west = StringIO()
    regional = StringIO()

    response = requests.get('https://api.transport.nsw.gov.au/v1/live/hazards/incident/all', headers={
        'Authorization': 'apikey {}'.format(app.config.get('SYDNEY_TRANSPORT_API_KEY', '')),
        'Accept': 'application/vnd.ttds-traveltime+json', 'User-Agent': 'AAP/1.0'})
    data = json.loads(response.content.decode('UTF-8'))
    for feature in data.get('features', []):
        ended = feature.get('properties').get('ended')
        if feature.get('properties').get('incidentKind') == 'Planned':
            continue
        for road in feature.get('properties', {}).get('roads', []):
            if not ended:
                msg = '<p>{}, {} {} {} {}{}</p>'.format(feature.get('properties').get('mainCategory'),
                                                        road.get('suburb'),
                                                        road.get('mainStreet'),
                                                        road.get('locationQualifier') if road.get(
                                                            'crossStreet') else '', road.get('crossStreet'),
                                                        ', ' + road.get('impactedLanes')[0].get(
                                                            'affectedDirection') if len(
                                                            road.get('impactedLanes')) else '')
                if road.get('region', '') == 'SYD_MET':
                    metro.write(msg)
                elif road.get('region', '') == 'SYD_NORTH':
                    north.write(msg)
                elif road.get('region', '') == 'SYD_SOUTH':
                    south.write(msg)
                elif road.get('region', '') == 'SYD_WEST':
                    west.write(msg)
                else:
                    regional.write(msg)

    incidents_map = {'alerts_metro': metro.getvalue(), 'alerts_north': north.getvalue(), 'alerts_west': west.getvalue(),
                     'alerts_south': south.getvalue(), 'alerts_regional': regional.getvalue()}

    metro.close()
    south.close()
    north.close()
    west.close()
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


name = 'Sydney Traffic Congestion'
label = 'Sydney Traffic Congestion'
callback = expand_sydney_traffic_congestion
access_type = 'frontend'
action_type = 'direct'
group = 'AM Desk'
