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

from apps.publish import init_app
from superdesk.tests import TestCase

from .aap_sms_formatter import AAPSMSFormatter


class AapSMSFormatterTest(TestCase):
    subscribers = [{"_id": "1", "name": "Test", "can_send_takes_packages": False, "media_type": "media",
                    "is_active": True, "sequence_num_settings": {"max": 10, "min": 1},
                    "destinations": [{"name": "AAP SMS", "delivery_type": "ODBC", "format": "AAP SMS",
                                      "config": {"connection_string": "DRIVER=BLAH", "stored_procedure": "Insert"}
                                      }]
                    }]

    article1 = {
        'priority': 1,
        'anpa_category': [{'qcode': 'a'}],
        'abstract': 'This is a test headline',
        'type': 'text',
        'body_html': 'The story body',
        'body_footer': 'call helpline 999 if you are planning to quit smoking'
    }

    article2 = {
        'priority': 1,
        'anpa_category': [{'qcode': 'a'}],
        'abstract': 'This is a test headline',
        'sms_message': 'This is the sms message',
        'type': 'text',
        'body_html': 'The story body',
        'body_footer': 'call helpline 999 if you are planning to quit smoking'
    }

    article3 = {
        'priority': 1,
        'anpa_category': [{'qcode': 'a'}],
        'abstract': 'This is a test headline',
        'sms_message': 'dont send again',
        'type': 'text',
        'body_html': 'The story body',
        'body_footer': 'call helpline 999 if you are planning to quit smoking'
    }

    article4 = {
        'priority': 1,
        'anpa_category': [{'qcode': 'a'}],
        'abstract': 'This is a test headline',
        'sms_message': '<p>not marked up string</p>',
        'type': 'text',
        'body_html': 'The story body',
        'body_footer': 'call helpline 999 if you are planning to quit smoking'
    }

    published = [{"_id": 1, "state": "published", "sms_message": "dont send again", "flags": {"marked_for_sms": True},
                  "queue_state": "queued"}]

    def setUp(self):
        self.app.data.insert('subscribers', self.subscribers)
        self.app.data.insert('published', self.published)
        init_app(self.app)
        self.app.config['TEST_SMS_OUTPUT'] = False

    def test_sms_can_format(self):
        f = AAPSMSFormatter()
        self.assertFalse(f.can_format("AAP SMS", self.article1))
        self.assertFalse(f.can_format("AAP SMS", self.article2))
        self.article2['flags'] = {'marked_for_sms': True}
        self.assertTrue(f.can_format("AAP SMS", self.article2))

    def test_cant_send_again(self):
        f = AAPSMSFormatter()
        self.assertFalse(f.can_format("AAP SMS", self.article3))

    def test_sms_formatter(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = AAPSMSFormatter()
        seq, item = f.format(self.article1, subscriber)[0]
        item = json.loads(item)

        self.assertGreater(int(seq), 0)
        self.assertDictEqual(item, {'Category': 'A', 'Priority': 'f', 'Sequence': item['Sequence'], 'ident': '0',
                                    'Headline': 'This is a test headline',
                                    'StoryText':
                                        'The story bodycall helpline 999 if you are planning to quit smoking'})

    def test_test_sms_formatter(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]
        self.app.config['TEST_SMS_OUTPUT'] = True

        f = AAPSMSFormatter()
        seq, item = f.format(self.article1, subscriber)[0]
        item = json.loads(item)

        self.assertGreater(int(seq), 0)
        self.assertDictEqual(item, {'Category': '1', 'Priority': 'f', 'Sequence': item['Sequence'], 'ident': '0',
                                    'Headline': 'This is a test headline',
                                    'StoryText':
                                        'The story bodycall helpline 999 if you are planning to quit smoking'})

    def test_sms_formatter_with_sms_message(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = AAPSMSFormatter()
        seq, item = f.format(self.article2, subscriber)[0]
        item = json.loads(item)

        self.assertGreater(int(seq), 0)
        self.assertDictEqual(item, {'Category': 'A', 'Priority': 'f', 'Sequence': item['Sequence'], 'ident': '0',
                                    'Headline': 'This is the sms message',
                                    'StoryText':
                                        'The story bodycall helpline 999 if you are planning to quit smoking'})

    def test_html_message(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = AAPSMSFormatter()
        seq, item = f.format(self.article4, subscriber)[0]
        item = json.loads(item)
        self.assertEqual(item['Headline'], 'not marked up string')
