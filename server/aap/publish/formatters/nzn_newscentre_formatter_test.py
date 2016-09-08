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
from superdesk.publish.subscribers import SUBSCRIBER_TYPES
from superdesk.tests import TestCase

from .nzn_newscentre_formatter import NznNewscentreFormatter


class NznNewscentreFormatterTest(TestCase):
    subscribers = [{"_id": "1", "name": "newscentre", "subscriber_type": SUBSCRIBER_TYPES.WIRE, "media_type": "media",
                    "is_active": True, "sequence_num_settings": {"max": 10, "min": 1},
                    "destinations": [{"name": "NZN NEWSCENTRE", "delivery_type": "email", "format": "NZN NEWSCENTRE",
                                      "config": {"recipients": "test@sourcefabric.org"}
                                      }]
                    }]

    desks = [{'_id': 1, 'name': 'National'},
             {'_id': 2, 'name': 'Sports'},
             {'_id': 3, 'name': 'Finance'}]

    article = {
        'source': 'AAP',
        'anpa_category': [{'qcode': 'a'}],
        'headline': 'This is a test headline',
        'byline': 'joe',
        'slugline': 'slugline',
        'subject': [{'qcode': '02011001'}],
        'anpa_take_key': 'take_key',
        'unique_id': '1',
        'format': 'preserved',
        'type': 'text',
        'body_html': '<p>The story body</p>',
        'word_count': '1',
        'priority': 1,
        'place': [{'qcode': 'VIC', 'name': 'VIC'}],
        'genre': []
    }

    vocab = [{'_id': 'categories', 'items': [
        {'is_active': True, 'name': 'Overseas Sport', 'qcode': 'S', 'subject': '15000000'},
        {'is_active': True, 'name': 'Finance', 'qcode': 'F', 'subject': '04000000'},
        {'is_active': True, 'name': 'General News', 'qcode': 'A'},
        {'is_active': True, 'name': 'New Zealand News', 'qcode': 'N'}
    ]}, {'_id': 'geographical_restrictions', 'items': [{'name': 'New South Wales', 'qcode': 'NSW', 'is_active': True},
                                                       {'name': 'Victoria', 'qcode': 'VIC', 'is_active': True}]}]

    def setUp(self):
        self.app.data.insert('subscribers', self.subscribers)
        self.app.data.insert('vocabularies', self.vocab)
        self.app.data.insert('desks', self.desks)
        init_app(self.app)

    def testNewscentreNZN(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = NznNewscentreFormatter()
        seq, item = f.format(self.article, subscriber)[0]
        item = json.loads(item)

        self.assertGreater(int(seq), 0)
        self.assertEqual(seq, item['sequence'])
        item.pop('sequence')
        self.assertDictEqual(item,
                             {'category': 'N', 'fullStory': 1, 'ident': '0',
                              'headline': 'VIC:This is a test headline', 'originator': 'NZN',
                              'take_key': 'take_key', 'article_text': 'The story body\r\nNZN', 'usn': '1',
                              'subject_matter': 'international law', 'news_item_type': 'News',
                              'subject_reference': '02011001', 'subject': 'crime, law and justice',
                              'subject_detail': 'international court or tribunal',
                              'selector_codes': ' ',
                              'genre': 'Current', 'keyword': 'slugline', 'author': 'joe'})
