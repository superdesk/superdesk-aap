
# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from superdesk.notification import push_notification
import superdesk
import time


class SocketLoadTestCommand(superdesk.Command):

    option_list = [
        superdesk.Option('--message_count', '-m', dest='message_count', required=True),
        superdesk.Option('--test_message', '-t', dest='test_message', required=True),
        superdesk.Option('--start_message', '-s', dest='start_message', required=True),
        superdesk.Option('--end_message', '-e', dest='end_message', required=True)
    ]

    def run(self, message_count, test_message, start_message, end_message):
        print('Starting to send messages')

        push_notification('{} at {}'.format(start_message, time.strftime("%H:%M:%S", time.localtime())))

        for i in range(0, int(message_count)):
            push_notification('{}:{} at {}'.format(test_message, i, time.strftime("%H:%M:%S", time.localtime())))
            if i % 250 == 0:
                time.sleep(1)

        push_notification('{} at {}'.format(end_message, time.strftime("%H:%M:%S", time.localtime())))

        print('Finished sending messages')


superdesk.command('app:socket_load_test', SocketLoadTestCommand())
