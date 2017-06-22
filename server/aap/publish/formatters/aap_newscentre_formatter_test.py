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

from .aap_newscentre_formatter import AAPNewscentreFormatter


class AapNewscentreFormatterTest(TestCase):
    subscribers = [{"_id": "1", "name": "newscentre", "subscriber_type": SUBSCRIBER_TYPES.WIRE, "media_type": "media",
                    "is_active": True, "sequence_num_settings": {"max": 10, "min": 1},
                    "destinations": [{"name": "AAP NEWSCENTRE", "delivery_type": "email", "format": "AAP NEWSCENTRE",
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
        {'is_active': True, 'name': 'General News', 'qcode': 'A'}
    ]}, {'_id': 'geographical_restrictions', 'items': [{'name': 'New South Wales', 'qcode': 'NSW', 'is_active': True},
                                                       {'name': 'Victoria', 'qcode': 'VIC', 'is_active': True}]}]

    def setUp(self):
        self.app.data.insert('subscribers', self.subscribers)
        self.app.data.insert('vocabularies', self.vocab)
        self.app.data.insert('desks', self.desks)
        init_app(self.app)

    def testNewscentreFormatterWithNoSelector(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = AAPNewscentreFormatter()
        seq, item = f.format(self.article, subscriber)[0]
        item = json.loads(item)

        self.assertGreater(int(seq), 0)
        self.assertEqual(seq, item['sequence'])
        item.pop('sequence')
        self.assertDictEqual(item,
                             {'category': 'A', 'fullStory': 1, 'ident': '0',
                              'headline': 'VIC:This is a test headline', 'originator': 'AAP',
                              'take_key': 'take_key', 'article_text': '   By joe\r\n\r\nThe story body\r\nAAP',
                              'usn': '1', 'subject_matter': 'international law', 'news_item_type': 'News',
                              'subject_reference': '02011001', 'subject': 'crime, law and justice',
                              'subject_detail': 'international court or tribunal',
                              'selector_codes': ' ',
                              'genre': 'Current', 'keyword': 'slugline', 'author': 'joe'})

    def testNewscentreHtmlToText(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 'A'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '02011001'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'body_html': '<p>The story body line 1<br>Line 2</p>'
                         '<p>abcdefghi abcdefghi abcdefghi abcdefghi abcdefghi abcdefghi abcdefghi abcdefghi more</p>',
            'word_count': '1',
            'priority': 1
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = AAPNewscentreFormatter()
        seq, item = f.format(article, subscriber)[0]
        item = json.loads(item)

        expected = '   By joe\r\n\r\n   The story body line 1\r\nLine 2\r\n\r\n   abcdefghi ' \
                   'abcdefghi abcdefghi abcdefghi abcdefghi ' + \
                   'abcdefghi abcdefghi abcdefghi more\r\n\r\n\r\nAAP'
        self.assertEqual(item['article_text'], expected)

    def testMultipleCategories(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'name': 'Finance', 'qcode': 'F'},
                              {'name': 'Overseas Sport', 'qcode': 'S'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '04001005'}, {'qcode': '15011002'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'body_html': '<p>body</p>',
            'word_count': '1',
            'priority': 1,
            'task': {'desk': 1},
            'place': [{'qcode': 'VIC', 'name': 'VIC'}]
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = AAPNewscentreFormatter()
        docs = f.format(article, subscriber, ['Aaa', 'Bbb', 'Ccc'])
        self.assertEqual(len(docs), 2)
        for seq, doc in docs:
            doc = json.loads(doc)
            if doc['category'] == 'S':
                self.assertEqual(doc['subject_reference'], '15011002')
                self.assertEqual(doc['subject_detail'], 'four-man sled')
                self.assertEqual(doc['headline'], 'VIC:This is a test headline')
            if doc['category'] == 'F':
                self.assertEqual(doc['subject_reference'], '04001005')
                self.assertEqual(doc['subject_detail'], 'viniculture')
                self.assertEqual(doc['headline'], 'VIC:This is a test headline')
                codes = set(doc['selector_codes'].split(' '))
                expected_codes = set('AAA BBB CCC'.split(' '))
                self.assertSetEqual(codes, expected_codes)

    def testNewscentreFormatterNoSubject(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 'a'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'body_html': '<p>body</p>',
            'word_count': '1',
            'priority': 1,
            'task': {'desk': 1},
            'urgency': 1,
            'place': [{'qcode': 'VIC', 'name': 'VIC'}]
        }
        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = AAPNewscentreFormatter()
        seq, doc = f.format(article, subscriber)[0]
        doc = json.loads(doc)
        self.assertEqual(doc['subject_reference'], '00000000')
        self.assertEqual(doc['headline'], 'VIC:This is a test headline')

        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 'a'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': None,
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'body_html': '<p>body</p>',
            'word_count': '1',
            'priority': 1,
            'task': {'desk': 1},
            'urgency': 1,
            'place': None
        }

        seq, doc = f.format(article, subscriber)[0]
        doc = json.loads(doc)
        self.assertEqual(doc['subject_reference'], '00000000')
        self.assertEqual(doc['headline'], 'This is a test headline')

    def test_aap_newscentre_formatter_with_body_footer(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]
        doc = self.article.copy()
        doc['body_footer'] = '<p>call helpline 999 if you are planning to quit smoking</p>'

        f = AAPNewscentreFormatter()
        seq, item = f.format(doc, subscriber, ['Axx'])[0]
        item = json.loads(item)

        self.assertGreater(int(seq), 0)
        self.assertEqual(seq, item['sequence'])
        item.pop('sequence')
        self.maxDiff = None
        self.assertDictEqual(item,
                             {'category': 'A', 'fullStory': 1, 'ident': '0',
                              'headline': 'VIC:This is a test headline', 'originator': 'AAP',
                              'take_key': 'take_key',
                              'article_text': '   By joe\r\n\r\nThe story body\r\ncall helpline 999 if you are '
                                              'planning '
                                              'to quit smoking\r\nAAP',
                              'usn': '1',
                              'subject_matter': 'international law', 'news_item_type': 'News',
                              'subject_reference': '02011001', 'subject': 'crime, law and justice',
                              'subject_detail': 'international court or tribunal',
                              'selector_codes': 'AXX',
                              'genre': 'Current', 'keyword': 'slugline', 'author': 'joe'})

    def test_aap_newscentre_formatter_with_parent_div(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]
        article = {
            "_id": "1",
            "pubstatus": "usable",
            "format": "HTML",
            "subject": [
                {
                    "qcode": "15042000",
                    "name": "netball",
                    "parent": "15000000"
                }
            ],
            "dateline": {
                "text": "MELBOURNE, June 10 AAP -",
                "source": "AAP",
                "located": {
                    "state_code": "VIC",
                    "alt_name": "",
                    "country_code": "AU",
                    "tz": "Australia/Melbourne",
                    "dateline": "city",
                    "country": "Australia",
                    "state": "Victoria",
                    "city": "Melbourne",
                    "city_code": "Melbourne"
                }
            },
            "genre": [
                {
                    "name": "Article (news)",
                    "qcode": "Article"
                }
            ],
            "type": "text",
            "priority": 6,
            "item_id": "tag:localhost:2017:ade7bae3-bb1a-44d4-bc13-f7b863b9fbf9",
            "original_source": "Samantha Sonogan <samantha.sonogan@gmail.com>",
            "abstract": "<p>Giants Netball have defeated Melbourne Vixens by eight goals to set up a Super Netball "
                        "grand final showdown against Sunshine Coast Lightning next weekend.</p>",
            "anpa_take_key": "Wrap",
            "event_id": "tag:localhost:2017:c48df4b8-8965-4446-b085-d3ae795a3ca7",
            "family_id": "urn:newsml:localhost:2017-06-10T20:56:13.982005:6aa08c6c-5e3b-418f-bc39-cfbddb31af54",
            "place": [
                {
                    "name": "VIC",
                    "group": "Australia",
                    "world_region": "Oceania",
                    "country": "Australia",
                    "qcode": "VIC",
                    "state": "Victoria"
                }
            ],
            "byline": "Samantha Sonogan",
            "digital_item_id": "tag:localhost:2017:ade7bae3-bb1a-44d4-bc13-f7b863b9fbf9",
            "original_creator": "",
            "source": "AAP",
            "state": "published",
            "slugline": "Net Vixens",
            "sms_message": "",
            "_etag": "9ece6fa87efa28765e3e3aea1c87b4321f19c7f3",
            "language": "en",
            "unique_name": "#12151006",
            "ingest_id": "urn:newsml:localhost:2017-06-10T20:56:13.982005:6aa08c6c-5e3b-418f-bc39-cfbddb31af54",
            "anpa_category": [
                {
                    "name": "Domestic Sport",
                    "qcode": "A",
                    "subject": "15000000"
                }
            ],
            "headline": "Giants beat Vixens to reach netball GF",
            "profile": "58b788bd069b7f6953927e9d",
            "queue_state": "queued",
            "body_html": "<div class=\"\"><p>Giants Netball have won through to the inaugural Super Netball grand "
                         "final with a clinical 65-57 victory over Melbourne Vixens at Hisense Arena on Saturday "
                         "night.</p><p>The eight-goal win secures the Giants a grand final berth against Sunshine "
                         "Coast Lightning at Brisbane Entertainment Centre next Saturday. </p><p>It wasn’t to be for "
                         "the Vixens who completed the regular season as minor premiers but lost both of their finals "
                         "matches.</p><p>Kristina Brice began the season on the Giants bench but showed she has the "
                         "skill and composure of a strike shooter with a match-high 42 goals, from 44 attempts at 95 "
                         "per cent accuracy.</p></div>",
            "operation": "publish",
            "sign_off": "TK",
            "ingest_provider_sequence": "5569",
            "rewritten_by": "urn:newsml:localhost:2017-06-10T21:41:14.783739:68340e20-13c2-4116-aefb-201a7d097117"
        }

        f = AAPNewscentreFormatter()
        seq, item = f.format(article, subscriber, ['Axx'])[0]
        item = json.loads(item)
        self.assertTrue(
            item['article_text'].startswith('   By Samantha Sonogan\r\n\r\n   MELBOURNE, June 10 AAP - Giants Netball'))
