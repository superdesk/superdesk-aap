
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
        superdesk.Option('--end_message', '-e', dest='end_message', required=True),
        superdesk.Option('--batch_size', '-b', dest='batch_size', required=True),
        superdesk.Option('--sleep_duration', '-sd', dest='sleep_duration', required=True)
    ]

    def run(self, message_count, test_message, start_message, end_message, batch_size, sleep_duration):
        print('Starting to send messages')
        print('Batch size: {}'.format(batch_size))
        print('Sleep duration: {}'.format(sleep_duration))

        b_size = int(batch_size)
        s_duration = float(sleep_duration)

        push_notification('{} at {}'.format(start_message, time.strftime("%H:%M:%S", time.localtime())))

        for i in range(1, int(message_count) + 1):
            push_notification('{}:{} at {}'.format(test_message, i, time.strftime("%H:%M:%S", time.localtime())))
            if i % b_size == 0:
                time.sleep(s_duration)

        push_notification('{} at {}'.format(end_message, time.strftime("%H:%M:%S", time.localtime())))

        print('Finished sending messages')


superdesk.command('app:socket_load_test', SocketLoadTestCommand())
