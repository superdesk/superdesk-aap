# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from unittests import AAPTestCase
from unittest.mock import patch
from aap.publish.transmitters.socket import SocketPublishService
from aap.errors import PublishSocketError


class mysocket():
    def __init__(self, a, b):
        pass

    def connect(self, address):
        return True

    def close(self):
        pass

    def sendall(self, msg):
        if msg != b'I was here':
            raise PublishSocketError.socketSendError(Exception('Bad Message'), None)


class myBadConnectingSocket(mysocket):
    def connect(self, address):
        raise Exception('connection failed')


class myBadSendSocket(mysocket):
    def sendall(self, msg):
        raise Exception('sendall failed')


class SocketPushPublishTestCase(AAPTestCase):
    def setUp(self):
        self.app.config['ERROR_NOTIFICATIONS'] = False

    @patch('socket.socket', mysocket)
    def test_transmit(self, *mock):
        service = SocketPublishService()

        item = {"destination": {
            "name": "L6 Ticker",
            "format": "aap ticker",
            "delivery_type": "socket",
            "config": {
                "port": "9999",
                "address": "127.0.0.1"
            }
        }, 'encoded_item': b'I was here'}
        with self.app.app_context():
            service._transmit(item, None)

    @patch('socket.socket', myBadConnectingSocket)
    def test_transmit_connect_fail(self, *mock):
        service = SocketPublishService()

        item = {"destination": {
            "name": "L6 Ticker",
            "format": "aap ticker",
            "delivery_type": "socket",
            "config": {
                "port": "9999",
                "address": "127.0.0.1"
            }
        }, 'encoded_item': b'I was here'}

        with self.assertRaises(PublishSocketError):
            with self.app.app_context():
                service._transmit(item, None)

    @patch('socket.socket', myBadSendSocket)
    def test_transmit_send_fail(self, *mock):
        service = SocketPublishService()

        item = {"destination": {
            "name": "L6 Ticker",
            "format": "aap ticker",
            "delivery_type": "socket",
            "config": {
                "port": "9999",
                "address": "127.0.0.1"
            }
        }, 'encoded_item': b'I was here'}

        with self.assertRaises(PublishSocketError):
            with self.app.app_context():
                service._transmit(item, None)
