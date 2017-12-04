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
    vocab = [{'_id': 'rightsinfo', 'items': [{'name': 'AAP',
                                              'copyrightHolder': 'copy right holder',
                                              'copyrightNotice': 'copy right notice',
                                              'usageTerms': 'terms'},
                                             {'name': 'NZN',
                                              'copyrightHolder': 'New Zealand Associated Press',
                                              'copyrightNotice': 'NZ copy right notice',
                                              'usageTerms': 'terms'},
                                             {'name': 'default',
                                              'copyrightHolder': 'default copy right holder',
                                              'copyrightNotice': 'default copy right notice',
                                              'usageTerms': 'default terms'}]}]

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

    def setUp(self):
        self.formatter = ReutersNewsML12Formatter()
        self.base_formatter = Formatter()
        init_app(self.app)
        self.app.data.insert('vocabularies', self.vocab)
        self.app.config['INIT_DATA_PATH'] = os.path.abspath(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../data'))

    def test_company_codes(self):
        now = datetime.datetime(2015, 6, 13, 11, 45, 19, 0)
        self.article['firstcreated'] = now
        self.article['versioncreated'] = now
        seq, doc = self.formatter.format(self.article, {'name': 'Test Subscriber'})[0]
        newsml = etree.fromstring(doc)
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
                         text, 'New Zealand Associated Press')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/TopicSet/Topic[@Duid="T0004"]/FormalName').
                         text, 'YAL.AX')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/TopicSet/Topic[@Duid="T0003"]/FormalName').
                         text, 'CORA')
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/NewsComponent/ContentItem/DataContent/'
                                     '{http://www.w3.org/1999/xhtml}html/{http://www.w3.org/1999/xhtml}head/'
                                     '{http://www.w3.org/1999/xhtml}title').
                         text, 'This is a test headline')

    def test_preformated(self):
        now = datetime.datetime(2015, 6, 13, 11, 45, 19, 0)
        self.article['firstcreated'] = now
        self.article['versioncreated'] = now
        item = self.article.copy()
        item.update({
            'body_html': '<pre>Test line 1\rTest line 2</pre>',
            'format': 'preserved'})

        seq, doc = self.formatter.format(item, {'name': 'Test Subscriber'})[0]
        newsml = etree.fromstring(doc)
        self.assertEqual(newsml.find('./NewsItem/NewsComponent/NewsComponent/ContentItem/DataContent/'
                                     '{http://www.w3.org/1999/xhtml}html/{http://www.w3.org/1999/xhtml}body/'
                                     '{http://www.w3.org/1999/xhtml}pre').text, 'Test line 1\nTest line 2')
