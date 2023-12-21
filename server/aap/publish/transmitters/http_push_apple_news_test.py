# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import json
import hmac
import base64
from httmock import all_requests, HTTMock
from unittest.mock import patch, Mock, MagicMock
from superdesk.tests import TestCase
from datetime import datetime
from .http_push_apple_news import HTTPAppleNewsPush
from superdesk.errors import PublishHTTPPushClientError
from hashlib import sha256


class MockedResourceService:
    """Mocked get_resource_service for http push to apple news"""

    def __init__(self, find_one, get_subscriber_reference, insert_update_reference):
        self.find_one = find_one
        self.get_subscriber_reference = get_subscriber_reference
        self.insert_update_reference = insert_update_reference


class HttpAppleNewsPushTestCase(TestCase):
    def setUp(self):
        self.http_push = HTTPAppleNewsPush()

    def get_queue_item(self):
        return {
            'destination': {
                'delivery_type': 'http_push_apple_news',
                'config': {
                    'api_secret': 'apisecret123apisecret123apisecret123',
                    'file_extension': 'json',
                    'api_key': 'apikey1234',
                    'header_image_rendition': '16-9',
                    'resource_url': 'https://news-api.apple.com',
                    'channel': 'channel1234'
                },
                'format': 'AAP Apple News',
                'name': 'Apple News'
            },
            'item_version': 5,
            'item_id': '1',
            'formatted_item': '{"test": "1"}',
            'subscriber_id': 'foo bar'
        }

    @all_requests
    def new_item_response(self, url, request):
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.url, 'https://news-api.apple.com/channels/channel1234/articles')
        self.assertIn('multipart/form-data', request.headers.get('Content-Type'))
        self.assertEqual('application/json', request.headers.get('accept'))
        return {
            'status_code': 200,
            'content': json.dumps({"data": {"id": "foo"}}).encode('UTF-8')
        }

    @all_requests
    def existing_item_response(self, url, request):
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.url, 'https://news-api.apple.com/articles/foo')
        self.assertIn('multipart/form-data', request.headers.get('Content-Type'))
        self.assertEqual('application/json', request.headers.get('accept'))
        return {
            'status_code': 200,
            'content': json.dumps({"data": {"id": "foo"}}).encode('UTF-8')
        }

    @all_requests
    def delete_item_response(self, url, request):
        self.assertEqual(request.method, 'DELETE')
        self.assertEqual(request.url, 'https://news-api.apple.com/articles/foo')
        self.assertEqual('application/json', request.headers.get('accept'))
        return {
            'status_code': 204
        }

    @all_requests
    def fail_item_response(self, url, request):
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.url, 'https://news-api.apple.com/channels/channel1234/articles')
        self.assertIn('multipart/form-data', request.headers.get('Content-Type'))
        self.assertEqual('application/json', request.headers.get('accept'))
        return {
            'status_code': 400,
            'content': 'Failed to process request'.encode('UTF-8'),
        }

    def test_transmit_new_item(self):
        queue_item = self.get_queue_item()
        find_one = Mock(return_value={'item_id': '1', 'state': 'published'})
        get_subscriber_reference = Mock(return_value=None)
        insert_update_reference = Mock()
        mocked_service = MagicMock()
        mocked_service.return_value = MockedResourceService(
            find_one=find_one,
            get_subscriber_reference=get_subscriber_reference,
            insert_update_reference=insert_update_reference
        )
        with patch('aap.publish.transmitters.http_push_apple_news.get_resource_service', mocked_service):
            with HTTMock(self.new_item_response):
                self.http_push._push_item(queue_item)
                find_one.assert_called()
                find_one.assert_called_with(req=None, _id='1')
                get_subscriber_reference.assert_called_once()
                get_subscriber_reference.assert_called_with('1', 'foo bar')

    def test_transmit_existing_item(self):
        queue_item = self.get_queue_item()
        find_one = Mock(return_value={'item_id': '1', 'state': 'published'})
        get_subscriber_reference = Mock(return_value={
            'item_id': '1',
            'subscriber_id': 'foo bar',
            'reference_id': 'foo',
            'extra': {
                'data': {
                    'revision': 'test'
                }
            }
        })
        insert_update_reference = Mock()
        mocked_service = MagicMock()
        mocked_service.return_value = MockedResourceService(
            find_one=find_one,
            get_subscriber_reference=get_subscriber_reference,
            insert_update_reference=insert_update_reference
        )
        with patch('aap.publish.transmitters.http_push_apple_news.get_resource_service', mocked_service):
            with HTTMock(self.existing_item_response):
                self.http_push._push_item(queue_item)
                find_one.assert_called()
                find_one.assert_called_with(req=None,
                                            _id='1')
                get_subscriber_reference.assert_called_once()
                get_subscriber_reference.assert_called_with('1', 'foo bar')

    def test_transmit_delete_item(self):
        queue_item = self.get_queue_item()
        find_one = Mock(return_value={'item_id': '1', 'state': 'killed'})
        get_subscriber_reference = Mock(return_value={
            'item_id': '1',
            'subscriber_id': 'foo bar',
            'reference_id': 'foo',
            'extra': {
                'data': {
                    'revision': 'test'
                }
            }
        })
        insert_update_reference = Mock()
        mocked_service = MagicMock()
        mocked_service.return_value = MockedResourceService(
            find_one=find_one,
            get_subscriber_reference=get_subscriber_reference,
            insert_update_reference=insert_update_reference
        )
        with patch('aap.publish.transmitters.http_push_apple_news.get_resource_service', mocked_service):
            with HTTMock(self.delete_item_response):
                self.http_push._push_item(queue_item)
                find_one.assert_called()
                find_one.assert_called_with(req=None, _id='1')
                get_subscriber_reference.assert_called_once()
                get_subscriber_reference.assert_called_with('1', 'foo bar')

    def test_get_headers(self):
        queue_item = self.get_queue_item()
        destination = queue_item.get('destination', {})
        current_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        resource_url = self.http_push._get_resource_url(destination)
        channel = self.http_push._get_channel(destination)
        url = '{}/channels/{}/articles'.format(resource_url, channel)
        canonical_request = self.http_push._get_canonical_request('POST', url, current_date)

        headers = self.http_push._get_headers(
            {'request': canonical_request, 'current_date': current_date},
            destination,
            {'accept': 'application/json'}
        )
        self.assertEqual(url, 'https://news-api.apple.com/channels/channel1234/articles')
        self.assertEqual(channel, 'channel1234')
        self.assertEqual(headers.get('accept'), 'application/json')

        api_secret = self.http_push._get_api_secret(destination)
        api_key = self.http_push._get_api_key(destination)
        key = base64.b64decode(api_secret)
        hashed_value = hmac.new(key, canonical_request, sha256)
        signature = base64.b64encode(hashed_value.digest()).decode()
        self.assertIn('HHMAC;', headers.get('authorization'))
        self.assertIn(signature, headers.get('authorization'))
        self.assertIn(api_key, headers.get('authorization'))
        self.assertIn(current_date, headers.get('authorization'))

    def test_transmit_fail(self):
        queue_item = self.get_queue_item()
        find_one = Mock(return_value={'item_id': '1', 'state': 'published'})
        get_subscriber_reference = Mock(return_value=None)
        insert_update_reference = Mock()
        mocked_service = MagicMock()
        mocked_service.return_value = MockedResourceService(
            find_one=find_one,
            get_subscriber_reference=get_subscriber_reference,
            insert_update_reference=insert_update_reference
        )
        with patch('aap.publish.transmitters.http_push_apple_news.get_resource_service', mocked_service):
            with HTTMock(self.fail_item_response):
                with self.assertRaises(PublishHTTPPushClientError) as context:
                    self.http_push._push_item(queue_item)

                self.assertTrue('HTTP push publish client error' in str(context.exception))
                self.assertTrue('Failed to process request' in str(context.exception.system_exception))
                self.assertEqual(context.exception.status_code, 400)
