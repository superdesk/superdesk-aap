# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from unittest import mock
from superdesk.tests import TestCase
from .kvh_newsml_1_2_formatter import KVHNewsML12Formatter
from lxml import etree
import datetime
from superdesk.publish import init_app


@mock.patch('superdesk.publish.subscribers.SubscribersService.generate_sequence_number', lambda self, subscriber: 1)
class KVHNewsML12FormatterTest(TestCase):
    article = {
        '_id': 'urn:localhost.abc',
        'guid': 'urn:localhost.abc',
        'source': 'AAP',
        'anpa_category': [{'qcode': 'a', 'name': 'Australian General News'}],
        'headline': 'This is a test headline',
        'byline': 'joe',
        'slugline': 'slugline',
        'subject': [{'qcode': '02011001'}, {'qcode': '02011002'}],
        'anpa_take_key': 'take_key',
        'unique_id': '1',
        'body_html': '<p>The story body&nbsp;more to the story</p>',
        'type': 'text',
        'word_count': '1',
        'priority': 1,
        '_current_version': 5,
        'state': 'published',
        'urgency': 2,
        'pubstatus': 'usable',
        'dateline': {
            'source': 'AAP',
            'text': 'sample dateline',
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
        'keywords': ['traffic'],
        'abstract': 'sample abstract',
        'place': [
            {'qcode': 'NSW', 'name': 'NSW', 'state': 'New South Wales',
             'country': 'Australia', 'world_region': 'Oceania'}
        ],
        'ednote': 'this is test',
        'body_footer': '<p>call helpline 999 if you are planning to quit smoking</p>',
        'company_codes': [{'name': 'YANCOAL AUSTRALIA LIMITED', 'qcode': 'YAL', 'security_exchange': 'ASX'}]
    }

    vocab = [{'_id': 'rightsinfo', 'items': [{'name': 'AAP',
                                              'copyrightHolder': 'copy right holder',
                                              'copyrightNotice': 'copy right notice',
                                              'usageTerms': 'terms'},
                                             {'name': 'default',
                                              'copyrightHolder': 'default copy right holder',
                                              'copyrightNotice': 'default copy right notice',
                                              'usageTerms': 'default terms'}]}]

    now = datetime.datetime(2019, 7, 13, 11, 45, 19, 0)

    def setUp(self):
        self.article['state'] = 'published'
        self._setup_dates([self.article])
        self.newsml = etree.Element("NewsML")
        self.formatter = KVHNewsML12Formatter()
        self.formatter.now = self.now
        self.formatter.string_now = self.now.strftime('%Y%m%dT%H%M%S+0000')
        with self.app.app_context():
            init_app(self.app)
            self.app.data.insert('vocabularies', self.vocab)

    def _setup_dates(self, item_list):
        for item in item_list:
            item['firstcreated'] = self.now
            item['versioncreated'] = self.now

    def test_format_news_component(self):
        self.formatter._format_news_component(self.article, self.newsml)
        self.assertEqual(self.newsml.find('NewsComponent/NewsComponent/Role').
                         get('FormalName'), 'Main')
        self.assertEqual(self.newsml.find('NewsComponent/NewsComponent/NewsLines/HeadLine').
                         text, 'This is a test headline')
        self.assertEqual(self.newsml.find('NewsComponent/NewsComponent/NewsLines/ByLine').
                         text, 'joe')
        self.assertEqual(self.newsml.find('NewsComponent/NewsComponent/NewsLines/DateLine').
                         text, 'sample dateline')
        self.assertEqual(self.newsml.find('NewsComponent/NewsComponent/NewsLines/CreditLine').
                         text, 'AAP')
        self.assertEqual(self.newsml.find('NewsComponent/NewsComponent/NewsLines/KeywordLine').
                         text, 'slugline')
        self.assertEqual(
            self.newsml.findall(
                'NewsComponent/NewsComponent/DescriptiveMetadata/SubjectCode/Subject')[0].get('FormalName'), '02011001')
        self.assertEqual(
            self.newsml.findall(
                'NewsComponent/NewsComponent/DescriptiveMetadata/SubjectCode/Subject')[1].get('FormalName'), '02011002')
        self.assertEqual(self.newsml.find('NewsComponent/NewsComponent/DescriptiveMetadata/Property'
                                          '/[@FormalName="Category"]').get('Value'), 'a')
        self.assertEqual(self.newsml.find('NewsComponent/NewsComponent/DescriptiveMetadata/Property'
                                          '/[@FormalName="TakeKey"]').get('Value'), 'take_key')
        self.assertEqual(
            self.newsml.findall(
                'NewsComponent/NewsComponent/NewsComponent/ContentItem/DataContent')[0].text, 'sample abstract')
        self.assertEqual(self.newsml.findall(
            'NewsComponent/NewsComponent/NewsComponent/ContentItem/DataContent/nitf/body/body.content/p')[0].text,
            'The story body\xa0more to the story')
        self.assertEqual(
            self.newsml.findall(
                'NewsComponent/NewsComponent/NewsComponent/ContentItem/DataContent/nitf/body/body.content/p')[1].text,
            'call helpline 999 if you are planning to quit smoking')
        self.assertEqual(self.newsml.find('.//NewsLines/NewsLine/NewsLineText').text, 'this is test')

        company_info = self.newsml.find('NewsComponent/NewsComponent/Metadata/Property[@FormalName="Ticker Symbol"]')
        self.assertEqual(company_info.attrib['Value'], 'YAL')

        company_info = self.newsml.find('NewsComponent/NewsComponent/Metadata/Property[@FormalName="Exchange"]')
        self.assertEqual(company_info.attrib['Value'], 'ASX')
