# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.publish.subscribers import SUBSCRIBER_TYPES
from test_factory import SuperdeskTestCase
from apps.publish import init_app
from .nzn_ipnews_formatter import NznIpNewsFormatter
import json


class NznIpNewsFormatterTest(SuperdeskTestCase):
    subscribers = [{"_id": "1", "name": "ipnews", "subscriber_type": SUBSCRIBER_TYPES.WIRE, "media_type": "media",
                    "is_active": True, "sequence_num_settings": {"max": 10, "min": 1},
                    "destinations": [{"name": "NZN IPNEWS", "delivery_type": "email", "format": "NZN IPNEWS",
                                      "config": {"recipients": "test@sourcefabric.org"}
                                      }]
                    }]

    desks = [{'_id': 1, 'name': 'New Zealand'},
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
        'body_html': 'The story body',
        'word_count': '1',
        'priority': 1,
        'genre': []
    }

    pkg = [{'_id': 'package',
            'type': 'composite',
            'package_type': 'takes',
            'last_take': '3'}]

    vocab = [{'_id': 'categories', 'items': [
        {'is_active': True, 'name': 'Overseas Sport', 'qcode': 'S', 'subject': '15000000'},
        {'is_active': True, 'name': 'Finance', 'qcode': 'F', 'subject': '04000000'},
        {'is_active': True, 'name': 'Domestic Sport', 'qcode': 'T'},
        {'is_active': True, 'name': 'New Zealand News', 'qcode': 'N'},
        {'is_active': True, 'name': 'International News', 'qcode': 'I'}
    ]}, {'_id': 'geographical_restrictions', 'items': [{'name': 'New South Wales', 'qcode': 'NSW', 'is_active': True},
                                                       {'name': 'Victoria', 'qcode': 'VIC', 'is_active': True}]}]

    def setUp(self):
        super().setUp()
        self.app.data.insert('subscribers', self.subscribers)
        self.app.data.insert('vocabularies', self.vocab)
        self.app.data.insert('desks', self.desks)
        self.app.data.insert('archive', self.pkg)
        init_app(self.app)

    def testCategoryMapper(self):
        f = NznIpNewsFormatter()
        mapped_cats = f._get_category_list([{'qcode': 'A'}])
        self.assertEqual(mapped_cats[0]['qcode'], 'N')
        mapped_cats = f._get_category_list([{'qcode': 'A'}, {'qcode': 'E'}])
        self.assertEqual(mapped_cats[0]['qcode'], 'N')
        self.assertTrue(len(mapped_cats) == 1)
        mapped_cats = f._get_category_list([{'qcode': 'S'}])
        self.assertEqual(mapped_cats[0]['qcode'], 'S')
        mapped_cats = f._get_category_list([{'qcode': 'T'}])
        self.assertEqual(mapped_cats[0]['qcode'], 'T')

    def testIPNewsFormatterAAPtoNZN(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = NznIpNewsFormatter()
        seq, item = f.format(self.article, subscriber)[0]
        item = json.loads(item)

        self.assertGreater(int(seq), 0)
        self.assertEqual(seq, item['sequence'])
        item.pop('sequence')
        self.maxDiff = None
        self.assertDictEqual(item,
                             {'category': 'n', 'texttab': 't', 'fullStory': 1, 'ident': '0',
                              'headline': 'This is a test headline', 'service_level': 'a', 'originator': 'NZN',
                              'take_key': 'take_key', 'article_text': 'The story body\r\nNZN', 'priority': 'f',
                              'usn': '1',
                              'subject_matter': 'international law', 'news_item_type': 'News',
                              'subject_reference': '02011001', 'subject': 'crime, law and justice',
                              'wordcount': '1', 'subject_detail': 'international court or tribunal',
                              'selector_codes': ' ',
                              'genre': 'Current', 'keyword': 'slugline', 'author': 'joe'})
