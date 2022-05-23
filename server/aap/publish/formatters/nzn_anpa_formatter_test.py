# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from datetime import datetime

import io
from apps.publish import init_app
from superdesk.publish.subscribers import SUBSCRIBER_TYPES
from superdesk.tests import TestCase

from .nzn_anpa_formatter import NZNAnpaFormatter


class NZNANPAFormatterTest(TestCase):
    subscribers = [{"_id": "1", "name": "notes", "subscriber_type": SUBSCRIBER_TYPES.WIRE, "media_type": "media",
                    "is_active": True, "sequence_num_settings": {"max": 10, "min": 1},
                    "destinations": [{"name": "ANPA", "delivery_type": "email", "format": "ANPA",
                                      "config": {"recipients": "test@sourcefabric.org"}
                                      }]
                    }]

    article = {
        'source': 'AAP',
        '_updated': datetime.strptime('2015-05-29 05:46', '%Y-%m-%d %H:%M'),
        'anpa_category': [{'qcode': 'a'}],
        'headline': 'This is a test headline',
        'slugline': 'slugline',
        'subject': [{'qcode': '02011001'}],
        'anpa_take_key': 'take_key',
        'urgency': 5,
        'unique_id': '1',
        'body_html': '<p>The story body</p>',
        'type': 'text',
        'word_count': '1',
        'priority': 1,
        'task': {'desk': 1},
        'body_footer': '<p>call helpline 999 if you are planning<br>to quit smoking</p>'
    }

    desks = [{'_id': 1, 'name': 'National'},
             {'_id': 2, 'name': 'Sports'},
             {'_id': 3, 'name': 'Finance'}]

    vocab = [{'_id': 'categories', 'items': [
        {'is_active': True, 'name': 'Overseas Sport', 'qcode': 'S', 'subject': '15000000'},
        {'is_active': True, 'name': 'Finance', 'qcode': 'F', 'subject': '04000000'},
        {'is_active': True, 'name': 'General News', 'qcode': 'A'},
        {'is_active': True, 'name': 'New Zealand News', 'qcode': 'N'}]}]

    def setUp(self):
        self.app.data.insert('subscribers', self.subscribers)
        self.app.data.insert('desks', self.desks)
        self.app.data.insert('vocabularies', self.vocab)
        init_app(self.app)

    def testNZNANPAFormatter(self):
        subscriber = self.app.data.find('subscribers', None, None)[0][0]

        f = NZNAnpaFormatter()
        resp = f.format(self.article.copy(), subscriber, ['axx'])[0]
        seq = resp['published_seq_num']
        item = resp['encoded_item']

        self.assertGreater(int(seq), 0)

        lines = io.StringIO(item.decode())

        line = lines.readline()
        self.assertTrue('axx' in line[1:])

        line = lines.readline()
        self.assertEqual(line[:3], '')  # Skip the sequence

        line = lines.readline()
        self.assertEqual(line[0:20], 'f n bc-slugline   ')  # skip the date

        line = lines.readline()
        self.assertEqual(line.strip(), 'This is a test headline')

        line = lines.readline()
        self.assertEqual(line.strip(), 'slugline take_key')

        line = lines.readline()
        self.assertEqual(line.strip(), 'The story body')

        line = lines.readline()
        self.assertEqual(line.strip(), 'call helpline 999 if you are planning')

        line = lines.readline()
        self.assertEqual(line.strip(), 'to quit smoking')

        lines.readline()
        line = lines.readline()
        self.assertEqual(line.strip(), 'NZN')
