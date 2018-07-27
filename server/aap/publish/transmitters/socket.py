# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.publish import register_transmitter
from superdesk.publish.publish_service import PublishService
from aap.errors import PublishSocketError
import socket
import logging

logger = logging.getLogger(__name__)
errors = [PublishSocketError.socketConnectionError().get_error_description(),
          PublishSocketError.socketSendError().get_error_description()]


class SocketPublishService(PublishService):
    """Socket publish service

    The service will establish a socket connection to the configured address on the configured port. It will write the
    Item to the stream then disconnect.
    """

    def _transmit(self, queue_item, subscriber):
        destination = queue_item.get('destination', {})
        config = destination.get('config', {})
        address = config.get('address')
        port = int(config.get('port'))

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port on the server given by the caller
        server_address = (address, port)
        try:
            sock.connect(server_address)
        except Exception as ex:
            sock.close()
            raise PublishSocketError.socketConnectionError(exception=ex, destination=destination)

        # try to send the complete item
        try:
            sock.sendall(queue_item['encoded_item'])
        except Exception as ex:
            raise PublishSocketError.socketSendError(exception=ex, destination=destination)
        finally:
            sock.close()


register_transmitter('socket', SocketPublishService(), errors)
