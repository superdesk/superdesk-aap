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
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
import requests
from requests import HTTPError
from datetime import datetime
import json
from io import StringIO, BytesIO
from flask import render_template_string
from flask import current_app as app
from zipfile import ZipFile
import csv
import io
import os
import glob
import re
from apps.prepopulate.app_initialize import get_filepath
from pathlib import Path
from superdesk.utils import config
from superdesk import get_resource_service
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE


logger = logging.getLogger(__name__)


def expand_sydney_public_transport(item, **kwargs):
    """
    Retrieve public transport alerts for Sydney public transport
    :param item:
    :param kwargs:
    :return:
    """

    trips = dict()
    routes = dict()
    stops = dict()
    times = dict()

    def get_reference_data():
        """Get the schedule data for Sydney trains so that routes and departure times can be identified

        :return:
        """

        # Get the path where the reference data is stored
        path = get_filepath('sydney_trains')

        # Request to get the current response headers
        response = requests.head('https://api.transport.nsw.gov.au/v1/gtfs/schedule/sydneytrains',
                                 headers={'Authorization':
                                          'apikey {}'.format(app.config.get('SYDNEY_TRANSPORT_API_KEY', '')),
                                          'Accept': 'application/octet-stream'})
        response.raise_for_status()

        # Get the name of the currently available file
        fname = re.findall("filename=(.+)", response.headers["Content-Disposition"])[0]

        # Get the path to the file new file
        zpath = Path(str(path) + '/' + fname)

        # If the current file exists we are up to date
        up_to_date = zpath.exists()

        # Need to retrieve the current file
        if not up_to_date:
            response = requests.get('https://api.transport.nsw.gov.au/v1/gtfs/schedule/sydneytrains',
                                    headers={'Authorization':
                                             'apikey {}'.format(app.config.get('SYDNEY_TRANSPORT_API_KEY', '')),
                                             'Accept': 'application/octet-stream'})
            response.raise_for_status()

            # Remove the old version of the file
            for f in glob.glob(str(path) + '/*.zip'):
                os.remove(f)

            # extract the contents from the new one
            zipfile = ZipFile(BytesIO(response.content))
            zipfile.extractall(str(path))

            with open(str(path) + '/' + fname, 'wb') as f:
                f.write(response.content)
                f.close()

        agency_file = zipfile.open('agency.txt') if not up_to_date else open(str(path) + '/agency.txt', 'rb')
        file = io.TextIOWrapper(agency_file, encoding='utf-8')
        agency_list = []
        for row in csv.DictReader(file):
            agency_list.append(row)
        agency_file.close()

        trips_file = zipfile.open('trips.txt') if not up_to_date else open(str(path) + '/trips.txt', 'rb')
        file = io.TextIOWrapper(trips_file, encoding='utf-8')
        for row in csv.DictReader(file):
            trips[row.get('trip_id')] = row
        trips_file.close()

        routes_file = zipfile.open('routes.txt') if not up_to_date else open(str(path) + '/routes.txt', 'rb')
        file = io.TextIOWrapper(routes_file, encoding='utf-8')
        for row in csv.DictReader(file):
            routes[row.get('route_id')] = row
        routes_file.close()

        stops_file = zipfile.open('stops.txt') if not up_to_date else open(str(path) + '/stops.txt', 'rb')
        file = io.TextIOWrapper(stops_file, encoding='utf-8')
        for row in csv.DictReader(file):
            stops[row.get('stop_id')] = row
        stops_file.close()

        if not up_to_date:
            stop_time_file = zipfile.open('stop_times.txt') if not up_to_date \
                else open(str(path) + '/stop_times.txt', 'rb')
            file = io.TextIOWrapper(stop_time_file, encoding='utf-8')
            stop_times = csv.DictReader(file)
            for row in stop_times:
                # save only the first stop
                if times.get(row.get('trip_id')):
                    if times.get(row.get('trip_id')).get('stop_sequence') < row.get('stop_sequence'):
                        times[row.get('trip_id')] = {'stop_sequence': row.get('stop_sequence'),
                                                     'departure_time': row.get('departure_time')}
                else:
                    times[row.get('trip_id')] = {'stop_sequence': row.get('stop_sequence'),
                                                 'departure_time': row.get('departure_time')}
            with open(str(path) + '/filtered_stop_times.json', 'w') as times_out:
                json.dump(times, times_out)
            times_out.close()
            stop_time_file.close()
        else:
            times_out = open(str(path) + '/filtered_stop_times.json', 'r')
            times.update(json.load(times_out))

    def convert_date(epoch):
        """Convert the passed epoch to a datetime

        :param epoch:
        :return:
        """
        dt = datetime.fromtimestamp(int(str(epoch)))
        return dt

    bus_story = StringIO()
    train_story = StringIO()
    ferry_story = StringIO()

    # This feed contains alerts across multiple agencies
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('https://api.nextthere.com/au_sydney/tools/GTFSRSydneyAlerts')
    response.raise_for_status()
    feed.ParseFromString(response.content)
    alerts = protobuf_to_dict(feed)
    for entity in alerts.get('entity'):
        if 'alert' in entity:
            alert = entity.get('alert')
            active = False
            time_count = 0
            recent_start = False
            for period in alert.get('active_period'):
                if convert_date(period.get('start')) <= datetime.now() <= convert_date(period.get('end')):
                    active = True
                    time_count += 1
                diff = datetime.now() - convert_date(period.get('start'))
                if diff.days == 0:
                    recent_start = True
            if active and time_count == 1 and recent_start and alert.get('informed_entity')[0].get('agency_id') \
                    not in ('711', '710', 'SF', 'SydneyTrains', 'NSWTrains'):
                bus_story.write(
                    '<p><b>{}</b></p>'.format(
                        alert.get('header_text').get('translation')[0].get('text')).replace('\n', '</br>'))
                bus_story.write(
                    '<p>{}</p><hr>'.format(
                        alert.get('description_text').get('translation')[0].get('text')).replace('\n', '</br>'))

            if active and time_count == 1 and recent_start and \
                    alert.get('informed_entity')[0].get('agency_id') == 'SydneyTrains':
                train_story.write('<p><b>{}</b></p>'.format(
                    alert.get('header_text').get('translation')[0].get('text')).replace('\n', '</br>'))
                train_story.write('<p>{}</p><hr>'.format(
                    alert.get('description_text').get('translation')[0].get('text')).replace('\n', '</br>'))

            if active and time_count == 1 and recent_start and alert.get('informed_entity')[0].get('agency_id') == 'SF':
                ferry_story.write('<p><b>{}</b></p>'.format(
                    alert.get('header_text').get('translation')[0].get('text')).replace('\n', '</br>'))
                ferry_story.write('<p>{}</p><hr>'.format(
                    alert.get('description_text').get('translation')[0].get('text')).replace('\n', '</br>'))

    incidents_map = {'bus_alerts': bus_story.getvalue()}
    bus_story.close()

    try:
        get_reference_data()

        response = requests.get('https://api.transport.nsw.gov.au/v1/gtfs/alerts/sydneytrains',
                                headers={'Authorization':
                                         'apikey {}'.format(app.config.get('SYDNEY_TRANSPORT_API_KEY', '')),
                                         'Accept': 'application/x-google-protobuf'})
        response.raise_for_status()

        feed.ParseFromString(response.content)
        alerts = protobuf_to_dict(feed)
        for entity in alerts.get('entity'):
            if 'alert' in entity:
                alert = entity.get('alert')
                ignore = False
                if alert.get('header_text').get('translation')[0].get('text').startswith('Lift Availability'):
                    continue
                for inf in alert.get('informed_entity'):
                    if inf.get('agency_id') != 'SydneyTrains':
                        ignore = True
                    if 'stop_id' in inf:
                        train_story.write('<p><b>{}</b></p>'.format(stops.get(inf.get('stop_id')).get('stop_name')))
                    if 'trip' in inf:
                        train_story.write('<p><b>{:5.5} : {}</b></p>'.format(
                            times.get(inf.get('trip').get('trip_id'), {}).get('departure_time'),
                            routes.get(trips.get(inf.get('trip').get('trip_id')).get('route_id')).get(
                                'route_long_name')))
                    break
                if not ignore:
                    train_story.write('<p>{} {}</p><hr>'.format(
                        alert.get('header_text').get('translation')[0].get('text'),
                        alert.get('description_text').get('translation')[0].get('text')))
    except HTTPError as ex:
        logger.warning('Exception retrieving gtfs')

    incidents_map['train_alerts'] = train_story.getvalue()
    train_story.close()

    incidents_map['ferry_alerts'] = ferry_story.getvalue()
    ferry_story.close()

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


name = 'Sydney Public Transport Alerts'
label = 'Sydney Public Transport Alerts'
callback = expand_sydney_public_transport
access_type = 'frontend'
action_type = 'direct'
group = 'AM Desk'
