# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.io.feeding_services.http_service import HTTPFeedingService
from superdesk.io.registry import register_feeding_service
from superdesk.errors import IngestApiError
import requests
import json
from datetime import datetime
from superdesk import get_resource_service
import logging
from superdesk.utc import local_to_utc
from eve.utils import config

logger = logging.getLogger(__name__)


class IntelematicsIncidentHTTPFeedingService(HTTPFeedingService):

    label = 'Intelematics Incident API Feed'
    NAME = 'intelematics_incident_api_feed'

    fields = [
        {
            'id': 'api_url', 'type': 'text', 'label': 'API URL',
            'placeholder': 'API URL', 'required': True
        },
        {
            'id': 'username', 'type': 'text', 'label': 'Username',
            'placeholder': 'Username', 'required': False
        },
        {
            'id': 'password', 'type': 'password', 'label': 'Password',
            'placeholder': 'Password', 'required': False
        }
    ]

    def _update(self, provider, update):

        def convert_date(epoch):
            dt = local_to_utc(config.DEFAULT_TIMEZONE, datetime.fromtimestamp(int(str(epoch)[:10])))
            return dt

        username = provider.get('config', {}).get('username')
        password = provider.get('config', {}).get('password')
        url = provider.get('config', {}).get('api_url')

        try:
            response = requests.get(url, auth=(username, password))
            response.raise_for_status()
        except Exception as ex:
            raise IngestApiError.apiGeneralError(ex, self.provider)

        data = json.loads(response.content.decode('UTF-8'))

        service = get_resource_service('traffic_incidents')
        incidents = []
        for feature in data.get('features', []):
            props = feature.get('properties', {})
            incident = {
                'guid': int(props.get('id')),
                'start_date': convert_date(props.get('startDate')),
                'end_date': convert_date(props.get('endDate')),
                'incident_type': props.get('type'),
                'incident_description': props.get('description'),
                'city': props.get('city'),
                'state': props.get('state'),
                'from_street_name': props.get('fromStreetName'),
                'from_crossStreet_ame': props.get('fromCrossStreetName'),
                'to_street_name': props.get('toStreetName'),
                'to_cross_street_name': props.get('toCrossStreetName'),
                'geometry': feature.get('geometry')
            }
            incident.get('geometry').pop('crs')
            incidents.append(incident)
        service.delete(lookup={})
        service.post(incidents)


register_feeding_service(IntelematicsIncidentHTTPFeedingService)
