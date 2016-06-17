
# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
import superdesk
import websockets
import asyncio
import time


class SocketListenerCommand(superdesk.Command):

    option_list = [
        superdesk.Option('--address', '-a', dest='address', required=True),
        superdesk.Option('--filter', '-f', dest='filter', required=True),
        superdesk.Option('--start_message', '-s', dest='start_message', required=True),
        superdesk.Option('--end_message', '-e', dest='end_message', required=True)
    ]

    def run(self, address, filter, start_message, end_message):
        print('Listening...')
        asyncio.get_event_loop().run_until_complete(self.listen(address, filter, start_message, end_message))
        print('Stopped listening.')

    @asyncio.coroutine
    def listen(self, address, filter, start_message, end_message):
        websocket = yield from websockets.connect(address)
        start = 0
        end = 0
        try:
            while True:
                message = yield from websocket.recv()
                if start_message and start_message in message:
                    start = time.time()
                    print("< {} at {}".format('Started', time.strftime("%H:%M:%S", time.localtime())))

                if filter and filter in message:
                    print("< {} at {}".format(message, time.strftime("%H:%M:%S", time.localtime())))

                if end_message and end_message in message:
                    end = time.time()
                    print("< {} at {}".format('Stopped', time.strftime("%H:%M:%S", time.localtime())))
                    print("< Total time in seconds: %02d" % (end - start))
                    break

        finally:
            yield from websocket.close()


superdesk.command('app:socket_listener', SocketListenerCommand())
