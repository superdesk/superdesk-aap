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
from datetime import datetime
import json
from io import StringIO
from superdesk.utc import utcnow, utc
from flask import render_template_string
from flask import current_app as app

logger = logging.getLogger(__name__)


def expand_melbourne_public_transport(item, **kwargs):
    train_story = StringIO()
    tram_story = StringIO()
    bus_story = StringIO()

    def get_story(mode, story):
        for mechanism in data.get('disruptions').get('metro_' + mode):
            if mechanism.get('disruption_status') == 'Current':
                now = utcnow()
                from_date = datetime.strptime(mechanism.get('from_date'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=utc)
                to_date = datetime.strptime(mechanism.get('to_date'), '%Y-%m-%dT%H:%M:%SZ').replace(
                    tzinfo=utc) if mechanism.get(
                    'to_date') else now
                diff = abs((from_date - now).days)
                # only include disrutptions that are current and started in the last couple of days
                if from_date <= now <= to_date and diff <= 2:
                    story.write('<p>{}'.format(mechanism.get('title')))
                    if mechanism.get('title') != mechanism.get('description'):
                        story.write(' {}'.format(mechanism.get('description')))
                    story.write('</p>')

        incidents_map[mode + '_alerts'] = story.getvalue()
        story.close()

    incidents_map = dict()
    response = requests.get('http://timetableapi.ptv.vic.gov.au/v3/disruptions?devid={}&'
                            'signature={}'.format(app.config.get('VICTORIAN_TRANSPORT_DEVICE_ID', ''),
                                                  app.config.get('VICTORIAN_TRANSPORT_SIGNATURE', '')))
    response.raise_for_status()
    data = json.loads(response.content.decode('utf-8'))

    get_story('train', train_story)
    get_story('tram', tram_story)
    get_story('bus', bus_story)

    item['body_html'] = render_template_string(item.get('body_html', ''), **incidents_map)
    return item


name = 'Melbourne Public Transport Alerts'
label = 'Melbourne Public Transport Alerts'
callback = expand_melbourne_public_transport
access_type = 'frontend'
action_type = 'direct'
group = 'AM Desk'
