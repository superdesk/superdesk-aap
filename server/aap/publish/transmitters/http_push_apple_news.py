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
import base64
import hmac
import requests
from datetime import datetime
from hashlib import sha256
from urllib3.fields import RequestField
from urllib3.filepost import encode_multipart_formdata
from superdesk import app
from superdesk.publish.publish_service import PublishService
from superdesk.publish import register_transmitter
from superdesk.errors import PublishHTTPPushError, PublishHTTPPushServerError, PublishHTTPPushClientError
from superdesk import get_resource_service, config
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE


errors = [PublishHTTPPushError.httpPushError().get_error_description()]
logger = logging.getLogger(__name__)


class HTTPAppleNewsPush(PublishService):
    headers = {"Accept": "application/json"}
    date_format = '%Y-%m-%dT%H:%M:%S+00:00'

    def _transmit(self, queue_item, subscriber):
        """
        @see: PublishService._transmit
        """
        self._push_item(queue_item)

    def _get_headers(self, data, destination, current_headers):
        """Get headers"""
        api_secret = self._get_api_secret(destination)
        api_key = self._get_api_key(destination)
        key = base64.b64decode(api_secret)
        hashed_value = hmac.new(key, data.get('request'), sha256)
        signature = base64.b64encode(hashed_value.digest()).decode()
        headers = {
            'authorization': 'HHMAC; key=%s; signature=%s; date=%s' % (api_key, signature, data.get('current_date'))
        }
        headers.update(current_headers)
        return headers

    def _get_item(self, queue_item):
        return get_resource_service('published').find_one(
            req=None,
            item_id=queue_item.get('item_id'),
            _current_version=queue_item.get('item_version')
        )

    def _get_original_guid(self, item):
        guid = item.get('rewrite_of', item.get('guid', item.get('item_id', None)))
        for i in range(item.get('rewrite_sequence', 1)):
            prev = get_resource_service('archive').find_one(
                req=None, _id=guid
            )
            if not prev or not prev.get('rewrite_of'):
                break
            guid = prev['rewrite_of']
        return guid

    def _push_item(self, queue_item):
        data = json.loads(queue_item['formatted_item'])
        associations = data.pop('associations', None)
        destination = queue_item.get('destination', {})
        item = self._get_item(queue_item)
        if not item:
            raise Exception('Could not find the item to publish.')

        resource_url = self._get_resource_url(destination)
        channel = self._get_channel(destination)
        current_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        method = 'POST' if item.get(ITEM_STATE) not in {CONTENT_STATE.RECALLED, CONTENT_STATE.KILLED} else 'DELETE'

        original_id = self._get_original_guid(item)
        service = get_resource_service('subscriber_transmit_references')
        subscriber_reference = service.get_subscriber_reference(
            original_id,
            queue_item.get('subscriber_id')
        )
        metadata = {}

        if not subscriber_reference:
            url = '{}/channels/{}/articles'.format(resource_url, channel)
        else:
            url = '{}/articles/{}'.format(resource_url, subscriber_reference.get('reference_id'))

        # generate body and content type for request
        content_type = 'application/json'
        body = b''
        if item.get(ITEM_STATE) not in {CONTENT_STATE.RECALLED, CONTENT_STATE.KILLED}:
            parts = []
            if subscriber_reference:
                # if the item is already published then we need revision
                metadata['data'] = {
                    'revision': subscriber_reference.get('extra').get('data').get('revision'),
                }
                metadata_payload = json.dumps(metadata)
                parts = [self._part('metadata', metadata_payload, len(metadata_payload), 'application/json')]

            payload = json.dumps(data)
            parts.append(self._part('article.json', payload, len(payload), 'application/json'))

            for association, details in (associations or {}).items():
                binary = self._get_media(association, self._get_header_image_rendition(destination), item)
                if binary:
                    parts.append(
                        self._part(association, binary.read(), binary.length, details.get('mimetype', 'image/jpeg')))

            body, content_type = encode_multipart_formdata(parts)
            canonical_request = self._get_canonical_request(method, url, current_date, content_type, body)
        else:
            canonical_request = self._get_canonical_request(method, url, current_date)

        headers = self._get_headers(
            {'request': canonical_request, 'current_date': current_date},
            destination,
            self.headers
        )

        try:
            response = None
            if item.get(ITEM_STATE) not in {CONTENT_STATE.RECALLED, CONTENT_STATE.KILLED}:
                headers['Content-Type'] = content_type
                session = requests.Session()
                req = requests.Request(method, url=url, headers=headers, data=body)
                prepared_request = req.prepare()
                response = session.send(prepared_request)
                response.raise_for_status()

                # response status_code is 204 for delete
                apple_article = json.loads(response.text)
                service.insert_update_reference(
                    original_id,
                    queue_item.get('subscriber_id'),
                    apple_article,
                    apple_article.get('data').get('id')
                )
            else:
                response = requests.delete(url, headers=headers)
                response.raise_for_status()

            logging.info('Apple News: Successfully transmitted {}.'.format(item.get('item_id')))
        except Exception as ex:
            logger.exception(ex)
            if response is not None:
                message = 'Error pushing item to apple news %s: %s' % (response.status_code, response.text)
            else:
                message = 'Failed to publish item to apple news. Queue Id: {}'.format(queue_item.get(config.ID_FIELD))
            self._raise_publish_error(response.status_code, Exception(message), destination)

    def _part(self, name, data, length, content_type):
        part = RequestField(name, data)
        part.headers['Content-Disposition'] = 'form-data; filename="%s"; size=%d' % (name, length)
        part.headers['Content-Type'] = content_type
        return part

    def _get_media(self, name, rendition_name, item):
        featuremedia = (item.get('associations') or {}).get(name)
        if not featuremedia:
            return None

        rendition = (featuremedia.get('renditions') or {}).get(rendition_name)
        if rendition:
            return app.media.get(
                rendition.get('media'),
                resource=rendition.get('resource', 'upload')
            )
        return None

    def _get_resource_url(self, destination):
        """Get the resource url"""
        return destination.get('config', {}).get('resource_url')

    def _get_canonical_request(self, method, url, date, content_type='', body=b''):
        """Get the canonical request"""
        return method.encode() + url.encode() + date.encode() + content_type.encode() + body

    def _get_channel(self, destination):
        """Get the channel"""
        return destination.get('config', {}).get('channel')

    def _get_api_key(self, destination):
        """Get the api key"""
        return destination.get('config', {}).get('api_key')

    def _get_api_secret(self, destination):
        """Get the api secret"""
        return destination.get('config', {}).get('api_secret')

    def _get_header_image_rendition(self, destination):
        return destination.get('config', {}).get('header_image_rendition') or '16-9'

    def _raise_publish_error(self, status_code, e, destination=None):
        if status_code >= 400 and status_code < 500:
            raise PublishHTTPPushClientError.httpPushError(e, destination)
        elif status_code >= 500 and status_code < 600:
            raise PublishHTTPPushServerError.httpPushError(e, destination)
        else:
            raise PublishHTTPPushError.httpPushError(e, destination)


register_transmitter('http_push_apple_news', HTTPAppleNewsPush(), errors)
