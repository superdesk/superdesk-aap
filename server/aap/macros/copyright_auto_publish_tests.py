# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from datetime import datetime
from superdesk.tests import TestCase
from .copyright_auto_publish import auto_publish


class CopyrightAutoPublishTestCase(TestCase):

    desks = [
        {
            "desk_type": "production",
            "name": "Politic Desk",
            "members": [],
            "desk_metadata": {},
            "description": "Test",
            "source": "AAP",
            "content_profiles": {},
            "content_expiry": 1440
        }
    ]

    articles = [
        {
            'guid': '123', '_id': '123',
            'type': 'text',
            'body_html': '<p>Copyright {{year}} AAP.</p>',
            'headline': 'Copyright',
            'abstract': 'abstract',
            'state': 'in_progress',
            '_current_version': 1,
            'unique_id': 1,
            'unique_name': '#1',
            'versioncreated': datetime(year=2018, month=8, day=1, hour=12, minute=12, second=0, microsecond=0)
        },
        {
            'guid': '456', '_id': '456',
            'type': 'text',
            'body_html': '<p>Copyright AAP.</p>',
            'headline': 'Copyright',
            'abstract': 'abstract',
            'state': 'in_progress',
            '_current_version': 1,
            'unique_id': 2,
            'unique_name': '#2',
            'versioncreated': datetime(year=2018, month=8, day=1, hour=12, minute=12, second=0, microsecond=0)
        }
    ]

    validators = [
        {
            'schema': {},
            'type': 'text',
            'act': 'publish',
            '_id': 'publish_text'
        },
        {
            '_id': 'publish_composite',
            'act': 'publish',
            'type': 'composite',
            'schema': {}
        }
    ]

    def setUp(self):
        self.app.data.insert('desks', self.desks)
        for article in self.articles:
            article['task'] = {
                'desk': self.desks[0].get('_id'),
                'stage': self.desks[0].get('incoming_stage')
            }
        self.app.data.insert('archive', self.articles)
        self.app.data.insert('validators', self.validators)

    def test_copyright_publish(self):
        item = auto_publish(self.articles[0])
        self.assertEqual(item.get('state'), 'published')
        self.assertEqual(item.get('headline'), 'Copyright')
        self.assertEqual(item.get('body_html'), '<p>Copyright 2018 AAP.</p>')

        item = auto_publish(self.articles[1])
        self.assertEqual(item.get('state'), 'published')
        self.assertEqual(item.get('headline'), 'Copyright')
        self.assertEqual(item.get('body_html'), '<p>Copyright AAP.</p>')
