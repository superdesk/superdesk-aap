# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from mock import patch
from copy import deepcopy
from superdesk.tests import TestCase
from .broadcast_auto_publish import broadcast_auto_publish


class BroadcastAutoPublishTestCase(TestCase):

    article = {
        'guid': 'aapimage-1', '_id': '1', 'type': 'text',
        'keywords': ['Student', 'Crime', 'Police', 'Missing'],
        'body_html': '',
        'state': 'published',
        'flags': {
            'marked_for_legal': False
        },
        'genre': [{'qcode': 'foo', 'name': 'bar'}]
    }

    def get_item(self):
        item = deepcopy(self.article)
        body_lines = []
        for count in range(1, 1005):
            body_lines.append('<p>line-#{}#</p>'.format(count))
        item['body_html'] = ''.join(body_lines)
        return item

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_state_published(self, internal_dest):
        item = self.get_item()
        broadcast_auto_publish(item)
        self.assertNotIn('line-#1001#', item['body_html'])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_state_corrected(self, internal_dest):
        item = self.get_item()
        item['state'] = 'corrected'

        broadcast_auto_publish(item)
        self.assertNotIn('line-#1001#', item['body_html'])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_state_killed(self, internal_dest):
        item = self.get_item()
        item['state'] = 'killed'

        broadcast_auto_publish(item)
        self.assertIn('line-#1004#', item['body_html'])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_state_recalled(self, internal_dest):
        item = self.get_item()
        item['state'] = 'killed'

        broadcast_auto_publish(item)
        self.assertIn('line-#1004#', item['body_html'])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_legal(self, internal_dest):
        item = self.get_item()
        item['flags']['marked_for_legal'] = True
        broadcast_auto_publish(item)
        self.assertIn('line-#1004#', item['body_html'])
        self.assertEqual([{'name': 'Broadcast Script', 'qcode': 'Broadcast Script'}], item['genre'])
        internal_dest.assert_called_with(item)

    @patch('aap.macros.broadcast_auto_publish.internal_destination_auto_publish')
    def test_broadcast_copy_not_text_item(self, internal_dest):
        item = self.get_item()
        item['type'] = 'picture'
        broadcast_auto_publish(item)
        self.assertIn('line-#1004#', item['body_html'])
        self.assertEqual([{'qcode': 'foo', 'name': 'bar'}], item['genre'])
        self.assertFalse(internal_dest.called)
