# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
import json
from superdesk.publish.transmitters import HTTPPushService
from superdesk.publish import register_transmitter
from superdesk.errors import PublishHTTPPushError
import requests
from superdesk import get_resource_service

errors = [PublishHTTPPushError.httpPushError().get_error_description()]
logger = logging.getLogger(__name__)


class HTTPAgendaPush(HTTPPushService):
    hash_header = 'x-agenda-api-key'
    headers = {"Content-type": "application/json", "Accept": "application/json"}

    def _get_headers(self, destination, current_headers):
        secret_token = self._get_secret_token(destination)
        if not secret_token:
            return current_headers
        headers = current_headers
        headers[self.hash_header] = secret_token
        return headers

    def _push_item(self, destination, data):
        # pop the ExternalIdentifier as the Superdesk planning id is to long for the Agenda database
        formatted_item = json.loads(data)
        id = formatted_item.pop('ExternalIdentifier')
        type = formatted_item.pop('Type')
        agenda_entry = json.dumps(formatted_item)

        resource_url = self._get_assets_url(destination)
        headers = self._get_headers(destination, self.headers)
        response = requests.post(resource_url, data=agenda_entry, headers=headers)

        # need to rethrow exception as a superdesk exception for now for notifiers.
        try:
            # The id from agenda is returned as part of the location header when the Event is created in Agenda
            location = response.headers.get('Location', None)
            if location:
                self._save_agenda_id(id, location, type)
            response.raise_for_status()
        except Exception as ex:
            logger.exception(ex)
            message = 'Error pushing item %s: %s' % (response.status_code, response.text)
            self._raise_publish_error(response.status_code, Exception(message), destination)

    def _save_agenda_id(self, id, location, type):
        agendaId = location.split('/')[-1]
        service = get_resource_service('events') if type == 'event' else get_resource_service('planning')
        original = service.find_one(req=None, _id=id)
        if original:
            service.system_update(id, {'unique_id': agendaId}, original)


register_transmitter('http_agenda_push', HTTPAgendaPush(), errors)
