# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from unittest import mock

from .reuters_newsml_1_2_formatter import ReutersNewsML12Formatter
from lxml import etree
from superdesk.publish import init_app
from superdesk.publish.formatters import Formatter
from superdesk.tests import TestCase
import datetime
import os


@mock.patch('superdesk.publish.subscribers.SubscribersService.generate_sequence_number', lambda self, subscriber: 1)
class ReutersNitfFormatterTest(TestCase):
    article = {
        'guid': 'tag:aap.com.au:20150613:12345',
        '_current_version': 1,
        'anpa_category': [{'qcode': 'f', 'name': 'Finance'}],
        'source': 'NZN',
        'headline': 'This is a test headline',
        'byline': 'joe',
        'slugline': 'slugline',
        'subject': [{'qcode': '02011001', 'name': 'international court or tribunal'},
                    {'qcode': '02011002', 'name': 'extradition'}, {'qcode': '4016006'}],
        'anpa_take_key': 'take_key',
        'unique_id': '1234',
        'body_html': '<p>Dental materials maker and marketer SDI<br> has boosted its shares after '
                     'reporting a lift in'
                     ' sales, with improvements across Europe, Brazil and North America.</p>'
                     '<p>SDI&nbsp;<span style=\"background-color: transparent;\">'
                     'reported a 7.8 per cent lift in unaudited'
                     ' sales to $74 million for the year to June 30, 2016 on Monday, up from $68.7 million a year '
                     'earlier.</span></p><p>The company said it expected to report a post-tax profit of '
                     'between $7.2 million '
                     'and $7.8 million when it releases its full-year results on August 29.</p><p>Shares in SDI gained '
                     '6.5 cents - a 12.2 per cent increase - to close at 59.5 cents on Monday.</p>',
        'type': 'text',
        'word_count': '1',
        'priority': '1',
        '_id': 'urn:localhost.abc',
        'state': 'published',
        'urgency': 2,
        'pubstatus': 'usable',
        'dateline': {
            'source': 'AAP',
            'text': 'Los Angeles, Aug 11 AAP -',
            'located': {
                'alt_name': '',
                'state': 'California',
                'city_code': 'Los Angeles',
                'city': 'Los Angeles',
                'dateline': 'city',
                'country_code': 'US',
                'country': 'USA',
                'tz': 'America/Los_Angeles',
                'state_code': 'CA'
            }
        },
        'creditline': 'sample creditline',
        'keywords': ['traffic'],
        'abstract': 'sample abstract',
        'place': [{'qcode': 'Australia', 'name': 'Australia',
                   'state': '', 'country': 'Australia',
                   'world_region': 'Oceania'}],
        'company_codes': [{'name': 'YANCOAL AUSTRALIA LIMITED', 'qcode': 'YAL', 'security_exchange': 'ASX'}],
        'sign_off': 'AM',
        'body_footer': '<p>call helpline 999 if you are planning to quit smoking</p>'
    }

    vocab = [{'_id': 'reuters_iptc_n2000_map', 'items': [{"is_active": True, "name": "BOMB", "qcode": "16005002"}]}]

    def setUp(self):
        self.app.data.insert('vocabularies', self.vocab)
        self.formatter = ReutersNewsML12Formatter()
        self.base_formatter = Formatter()
        init_app(self.app)
        self.app.config['INIT_DATA_PATH'] = os.path.abspath(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../data'))

    def test_company_codes(self):
        now = datetime.datetime(2015, 6, 13, 11, 45, 19, 0)
        self.article['firstcreated'] = now
        self.article['versioncreated'] = now
        seq, doc = self.formatter.format(self.article, {'name': 'Test Subscriber'})[0]
        utf8_parser = etree.XMLParser(encoding='utf-8')
        newsml = etree.fromstring(doc.encode('utf-8'), parser=utf8_parser)
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/Role').
                         get('FormalName'), 'Main')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/NewsComponent/Role').
                         get('FormalName'), 'MainText')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/NewsComponent/NewsLines/HeadLine').
                         text, 'This is a test headline')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/NewsComponent/NewsLines/ByLine').
                         text, 'joe')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/NewsComponent/NewsLines/DateLine').
                         text, 'Los Angeles, Aug 11 AAP -')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/NewsComponent/NewsLines/CreditLine').
                         text, 'Australian Associated Press')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/TopicSet/Topic[@Duid="T0004"]/FormalName').
                         text, 'YAL.AX')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/TopicSet/Topic[@Duid="T0003"]/FormalName').
                         text, 'CORA')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/NewsComponent/ContentItem/DataContent/'
                                     '{http://www.w3.org/1999/xhtml}html/{http://www.w3.org/1999/xhtml}head/'
                                     '{http://www.w3.org/1999/xhtml}title').
                         text, None)

    def test_preformated(self):
        now = datetime.datetime(2015, 6, 13, 11, 45, 19, 0)
        self.article['firstcreated'] = now
        self.article['versioncreated'] = now
        item = self.article.copy()
        item.update({
            'body_html': '<pre>Test line 1\rTest line 2</pre>',
            'format': 'preserved'})

        seq, doc = self.formatter.format(item, {'name': 'Test Subscriber'})[0]
        utf8_parser = etree.XMLParser(encoding='utf-8')
        newsml = etree.fromstring(doc.encode('utf-8'), parser=utf8_parser)
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/NewsComponent/ContentItem/DataContent/'
                                     '{http://www.w3.org/1999/xhtml}html/{http://www.w3.org/1999/xhtml}body/'
                                     '{http://www.w3.org/1999/xhtml}pre').text, 'Test line 1\nTest line 2')

    def test_subjects(self):
        article = {
            "_id": "tag:localhost:2017:e3b9176f-c20f-49cb-a145-6130ac6496e4",
            "original_creator": "",
            "guid": "tag:localhost:2017:e3b9176f-c20f-49cb-a145-6130ac6496e4",
            "format": "HTML",
            "unique_name": "#32234594",
            "slugline": "Contraband",
            "keywords": [],
            "ingest_id":
                "urn:newsml:localhost:2017-12-11T11:04:40.538092:9a7db65e-f623-47bf-ba49-37d5dee3a04f",
            "genre": [
                {
                    "qcode": "Article",
                    "name": "Article (news)"
                }
            ],
            "_current_version": 2,
            "byline": "",
            "place": [],
            "state": "published",
            "pubstatus": "usable",
            "subject": [
                {
                    "qcode": "16005002",
                    "name": "bombings"
                },
                {
                    "qcode": "02003000",
                    "name": "police"
                },
                {
                    "qcode": "02000000",
                    "name": "crime, law and justice"
                }
            ],
            "source": "TEST",
            "profile": "58b788bd069b7f6953927e9d",
            "anpa_take_key": "",
            "priority": 6,
            "abstract": "",
            "family_id": "urn:newsml:localhost:2017-12-11T11:04:40.538092:9a7db65e-f623-47bf-ba49-"
                         "37d5dee3a04f",
            "headline": "NSW prison guard caught smuggling tobacco",
            "_etag": "3d856e0463ce349bb6a09f854eb4271585169744",
            "anpa_category": [
                {
                    "qcode": "a",
                    "name": "Australian General News"
                }
            ],
            "word_count": 79,
            "event_id": "tag:localhost:2017:81ef03fe-afaf-4670-8175-bbeb22c7a172",
            "body_html": "<p>Hannah Higgins</p><p>SYDNEY, Dec 11 AAP - A prison guard is facing corruption"
                         " charges after she was caught allegedly smuggling tobacco to a prisoner in "
                         "western Sydney's Parklea jail.</p><p>The 40-year-old woman was nabbed at a prison"
                         " in Parklea after she allegedly supplied the drug to an inmate in exchange for "
                         "cash on Sunday morning, police say.</p><p>She has since been dismissed and is "
                         "due to appear in Blacktown Local Court on January 29.</p><p>AAP hh/jca/wf</p>",
            "unique_id": 32234594,
            "urgency": 5,
            "operation": "publish",
            "ingest_provider": "55c2b5349cb25900254c9f6f",
            "ingest_provider_sequence": "0211",
            "type": "text",
            "language": "en",
        }
        now = datetime.datetime(2015, 6, 13, 11, 45, 19, 0)
        article['firstcreated'] = now
        article['versioncreated'] = now

        seq, doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        utf8_parser = etree.XMLParser(encoding='utf-8')
        newsml = etree.fromstring(doc.encode('utf-8'), parser=utf8_parser)
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/TopicSet/Topic[@Duid="T0003"]/FormalName').
                         text, 'BOMB')
