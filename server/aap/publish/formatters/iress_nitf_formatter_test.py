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
from datetime import datetime
import xml.etree.ElementTree as etree
from superdesk.publish import init_app
from superdesk.publish.formatters import Formatter
from superdesk.tests import TestCase
from .iress_nitf_formatter import IRESSNITFFormatter


@mock.patch('superdesk.publish.subscribers.SubscribersService.generate_sequence_number', lambda self, subscriber: 1)
class IRESSNITFFormatterTest(TestCase):
    line_ender = b'\x19\x0D\x0A'.decode()
    line_feed = 'ZZZZYYYY\n'
    line_prefix = '   '

    def setUp(self):
        self.formatter = IRESSNITFFormatter()
        self.base_formatter = Formatter()
        init_app(self.app)
        self.setUpData()

    def setUpData(self):
        copyrights = [{
            "_id": "rightsinfo",
            "items": [
                {
                    "usageTerms": "Usage terms goes here.",
                    "copyrightHolder": "Australian Associated Press",
                    "is_active": True,
                    "copyrightNotice": "Notice goes here.",
                    "name": "AAP"
                },
                {
                    "usageTerms": "Usage terms goes here.",
                    "copyrightHolder": "Australian Associated Press",
                    "is_active": True,
                    "copyrightNotice": "Notice goes here.",
                    "name": "default"
                },
                {
                    "usageTerms": "Usage terms goes here.",
                    "copyrightHolder": "Foo bar",
                    "is_active": True,
                    "copyrightNotice": "Notice goes here.",
                    "name": "SUP"
                }
            ],
            "type": "manageable",
            "_etag": "init",
            "display_name": "Copyrights",
        }]
        self.app.data.insert('vocabularies', copyrights)

    def test_append_legal(self):
        article = {
            'slugline': 'Obama Republican Healthc',
            'flags': {'marked_for_legal': True}
        }

        slugline = self.base_formatter.append_legal(article)
        self.assertEqual(slugline, 'Legal: Obama Republican Healthc')
        slugline = self.base_formatter.append_legal(article, truncate=True)
        self.assertEqual(slugline, 'Legal: Obama Republican ')

    def test_append_legal_when_not_legal(self):
        article = {
            'slugline': 'Obama Republican Healthc',
            'flags': {'marked_for_legal': False}
        }

        slugline = self.base_formatter.append_legal(article)
        self.assertEqual(slugline, 'Obama Republican Healthc')

    def test_formatter(self):
        article = {
            'headline': 'test headline',
            'body_html': '<p>test body</p><p>test body</p>',
            'slugline': 'keyword',
            'anpa_take_key': 'take-key',
            'anpa_category': [{'qcode': 'f', 'name': 'Finance'}],
            'original_source': 'EMAIL',
            'type': 'text',
            'priority': '9',
            'source': 'SUP',
            '_id': 'urn:localhost.abc',
            'guid': 'urn:localhost.abc',
            'urgency': 2,
            'word_count': 99,
            'unique_id': 11,
            'place': [{'qcode': 'FED'}],
            'sign_off': 'me',
            'versioncreated': datetime(2018, 6, 13, 11, 45, 19, 0),
            'byline': 'Bar Foo'
        }

        doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        item = doc['formatted_item'].replace(self.line_ender, self.line_feed)
        nitf_xml = etree.fromstring(item)
        self.assertEqual(nitf_xml.find('head/title').text, 'FED:test headline')
        self.assertEqual(nitf_xml.find('body/body.content/pre').text,
                         '   Bar FooZZZZYYYY\n   test bodyZZZZYYYY\n   test bodyZZZZYYYY\n   SUP meZZZZYYYY\n')
        self.assertEqual(nitf_xml.find('head/docdata/urgency').get('ed-urg'), '2')
        self.assertEqual(nitf_xml.find('head/meta[@name="anpa-sequence"]').get('content'),
                         str(doc['published_seq_num']).zfill(4))
        self.assertEqual(nitf_xml.find('head/meta[@name="anpa-keyword"]').get('content'), 'keyword')
        self.assertEqual(nitf_xml.find('head/meta[@name="anpa-takekey"]').get('content'), 'take-key')
        self.assertEqual(nitf_xml.find('head/meta[@name="anpa-category"]').get('content'), 'f')
        self.assertEqual(nitf_xml.find('head/meta[@name="anpa-wordcount"]').get('content'), '0099')
        self.assertEqual(nitf_xml.find('body/body.head/hedline/hl1').text, 'FED:test headline')
        self.assertEqual(nitf_xml.find('head/docdata/doc.copyright').get('year'), '2018')
        self.assertEqual(nitf_xml.find('head/docdata/doc.copyright').get('holder'), 'Foo bar')
        self.assertEqual(nitf_xml.find('head/docdata/doc-id').get('id-string'), 'AAP.20180613.11')
        self.assertEqual(nitf_xml.find('head/docdata/date.issue').get('norm'),
                         article.get('versioncreated').strftime('%Y%m%dT%H%M%S'))
        self.assertEqual(nitf_xml.find('head/docdata/date.release').get('norm'),
                         article.get('versioncreated').strftime('%Y%m%dT%H%M%S'))
        self.assertEqual(len(nitf_xml.findall('body/body.end')), 0)

    def test_company_codes(self):
        article = {
            'guid': 'tag:aap.com.au:20150613:12345',
            '_current_version': 1,
            'anpa_category': [{'qcode': 'f', 'name': 'Finance'}],
            'source': 'AAP',
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '02011001', 'name': 'international court or tribunal'},
                        {'qcode': '02011002', 'name': 'extradition'}],
            'anpa_take_key': 'take_key',
            'unique_id': 1,
            'body_html': 'The story body',
            'type': 'text',
            'word_count': '1',
            'priority': '1',
            '_id': 'urn:localhost.abc',
            'state': 'published',
            'urgency': 2,
            'pubstatus': 'usable',
            'versioncreated': datetime(2018, 6, 13, 11, 45, 19, 0),
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
            'company_codes': [
                {'name': 'YANCOAL AUSTRALIA LIMITED', 'qcode': 'YAL', 'security_exchange': 'ASX'},
                {'name': 'BHP Billiton Limited', 'qcode': 'BHP', 'security_exchange': 'ASX'}
            ]
        }

        doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        item = doc['formatted_item'].replace(self.line_ender, self.line_feed)
        nitf_xml = etree.fromstring(item)
        self.assertEqual(nitf_xml.find('head/meta[@name="asx-codes"]').get('content'), "YAL BHP")

    def testDivContent(self):
        article = {
            '_id': '3',
            'source': 'AAP',
            'anpa_category': [{'qcode': 'a'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '02011001'}],
            'anpa_take_key': 'take_key',
            'unique_id': 1,
            'type': 'text',
            'versioncreated': datetime(2018, 6, 13, 11, 45, 19, 0),
            'body_html': '<div>Kathmandu Holdings has lodged a claim in the New Zealand High'
                         'Court for the recovery of costs associated with last years takeover bid from Briscoe'
                         'Group.</div><div>Kathmandu Holdings has lodged a claim in the New Zealand High Court for '
                         'the recovery of costs associated with last years takeover bid from Briscoe Group.'
                         '</div><div><br></div><div><br></div><div>Kathmandu incurred costs in relation to the takeover'
                         'After an initial request for payment on November 20, 2015 and subsequent correspondence, '
                         'Briscoe made a payment of $637,711.65 on May 25, 2016 without prejudice to its position on '
                         'what sum Kathmandu is entitled to recover.</div><div><br></div><div>Kathmandu considers the '
                         'full amount claimed is recoverable and has issued legal proceedings for the balance of monies'
                         ' owed.</div>',
            'word_count': '1',
            'priority': 1
        }
        doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        item = doc['formatted_item'].replace(self.line_ender, self.line_feed)
        nitf_xml = etree.fromstring(item)
        self.assertTrue(nitf_xml.find('body/body.content/pre').text.
                        startswith('   joeZZZZYYYY\n   Kathmandu Holdings'))
        self.assertTrue(nitf_xml.find('body/body.content/pre').text.split('\n'), 7)

    def testLFContent(self):
        article = {
            '_id': '3',
            'source': 'AAP',
            'anpa_category': [{'qcode': 'a'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '02011001'}],
            'anpa_take_key': 'take_key',
            'unique_id': 1,
            'versioncreated': datetime(2018, 6, 13, 11, 45, 19, 0),
            'type': 'text',
            'body_html': '<p><span style=\"background-color: transparent;\">The Australian dollar has tumbled'
                         ' after&nbsp;</span>Standard &amp; Poor\'s warned the country\'s triple-A credit rating '
                         'is at risk.<br></p><p>   At 1200 AEST on Thursday, the currency was trading at 74.98 US '
                         'cents, up from\n\n 74.41\n\n cents on Wednesday, but down from a high of 75.38 on Thursday '
                         'morning.</p><p>S&amp;P downgraded its outlook on Australia\'s credit rating from stable '
                         'to negative, due to the prospect of ongoing budget deficits without substantial reforms '
                         'being passed by parliament.</p><p>Westpac chief currency strategist&nbsp;Robert Rennie '
                         'said the uncertain election outcome is likely to result in a longer run of budget'
                         'deficits.</p><p>\"It was clearly a risk and the market has been living in its shadow since'
                         'Monday morning,\" he said.</p><p>\"Gridlock or the inability to improve the fiscal situation '
                         'over the forecast period is something I think a ratings agency ought to take into '
                         'account.\"</p><p><span style=\"background-color: transparent;\">The currency had a sudden '
                         'plunge to 74.67 US cents on the announcement from S&amp;P, before recovering some of that '
                         'ground.</span></p><p><span style=\"background-color: transparent;\">Mr Rennie tipped the '
                         'Australian dollar will slip further on Thursday.</span></p><p><span style=\"background-color:'
                         'transparent;\">\"We should make fresh lows, we should be pushing down though 74 US cents '
                         'and possibly lower,\" he said.</span></p><p><span style=\"background-color: '
                         'transparent;\">KEY MOVEMENTS:</span></p><p><span style=\"background-color: transparent;\">One'
                         'Australian dollar buys:</span><br></p><p>   * 74.98 US cents, from\n\n 74.41\n\ncents on '
                         'Wednesday</p><p>   * 75.63 Japanese yen, from \n\n75.15\n\n yen</p><p>   * 67.64 euro cents, '
                         'from \n\n67.24\n\n euro cents</p><p>   * 105.01 New Zealand cents, from \n\n104.85\n\n NZ '
                         'cents</p><p>   * 57.96 British pence, from \n\n57.53\n\n pence</p><p>   Government bond '
                         'yields:</p><p>   * CGS 5.25pct March 2019, 1.510pct, from \n\n1.513pct</p><p>   * CGS 4.25pct'
                         'April 2026, 1.868pct, from \n\n1.862pct</p><p>   Sydney Futures Exchange prices:</p><p>   *'
                         'September 2016 10-year bond futures contract, was at 98.125\n\n (1.875\n\n per cent), '
                         'unchanged from Wednesday</p><p>   * September 2016 3-year bond futures contract, at 98.570 '
                         '(1.430 per cent), up from \n\n98.550\n\n (1.450\n\n per cent)</p><p>   (*Currency closes '
                         'taken at 1700 AEST previous local session, bond market closes taken at 1630 AEST previous '
                         'local session)</p><p>   Source: IRESS</p>',
            'word_count': '1',
            'priority': 1
        }
        doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        item = doc['formatted_item'].replace(self.line_ender, self.line_feed)
        nitf_xml = etree.fromstring(item)
        self.assertTrue('from 74.41' in nitf_xml.find('body/body.content/pre').text)

    def testStraySpaceContent(self):
        article = {
            '_id': '3',
            'source': 'AAP',
            'anpa_category': [{'qcode': 'a'}],
            'headline': 'This is a test headline',
            'slugline': 'slugline',
            'subject': [{'qcode': '02011001'}],
            'anpa_take_key': 'take_key',
            'unique_id': 1,
            'type': 'text',
            'versioncreated': datetime(2018, 6, 13, 11, 45, 19, 0),
            'body_html': '<p><span style=\"background-color: transparent;\">\"</span>'
                         '<span style=\"background-color: transparent;\">However</span></p>'
                         '<p>\"<span style=\"background-color: transparent;\">The proposed</p>',
            'word_count': '1',
            'priority': 1
        }
        doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        item = doc['formatted_item'].replace(self.line_ender, self.line_feed)
        nitf_xml = etree.fromstring(item)
        self.assertEqual(nitf_xml.find('body/body.content/pre').text,
                         '\"However   \"The proposedZZZZYYYY\n   AAPZZZZYYYY\n')

    def testSpacesContent(self):
        article = {
            '_id': '3',
            'source': 'AAP',
            'anpa_category': [{'qcode': 'a'}],
            'headline': 'This is a test headline',
            'slugline': 'slugline',
            'subject': [{'qcode': '02011001'}],
            'anpa_take_key': 'take_key',
            'unique_id': 1,
            'type': 'text',
            'versioncreated': datetime(2018, 6, 13, 11, 45, 19, 0),
            'body_html': '<p>a b  c   d&nbsp;e&nbsp;&nbsp;f\xA0g</p>',
            'word_count': '1',
            'priority': 1
        }
        doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        item = doc['formatted_item'].replace(self.line_ender, self.line_feed)
        nitf_xml = etree.fromstring(item)
        self.assertEqual(nitf_xml.find('body/body.content/pre').text, '   a b c d e  f gZZZZYYYY\n   AAPZZZZYYYY\n')

    def testControlCharsContent(self):
        article = {
            '_id': '3',
            'source': 'AAP',
            'anpa_category': [{'qcode': 'a'}],
            'headline': 'This is a test headline',
            'slugline': 'slugline',
            'subject': [{'qcode': '02011001'}],
            'anpa_take_key': 'take_key',
            'unique_id': 1,
            'versioncreated': datetime(2018, 6, 13, 11, 45, 19, 0),
            'type': 'text',
            'body_html': '<p><span style=\"background-color: transparent;\">\u0018\u0012\f \u000b\u0012\b</span>'
                         '<span style=\"background-color: transparent;\">\u0005\f\u0006\b \u0006\f\u0019&nbsp;</span>'
                         '</p>',
            'word_count': '1',
            'priority': 1
        }
        doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        item = doc['formatted_item'].replace(self.line_ender, self.line_feed)
        nitf_xml = etree.fromstring(item)
        self.assertEqual(nitf_xml.find('body/body.content/pre').text, '      AAPZZZZYYYY\n')

    def testNullTakeKeyContent(self):
        article = {
            '_id': '3',
            'source': 'AAP',
            'anpa_category': [{'qcode': 'a'}],
            'headline': 'This is a test headline',
            'byline': None,
            'versioncreated': datetime(2018, 6, 13, 11, 45, 19, 0),
            'slugline': 'slugline',
            'subject': [{'qcode': '02011001'}],
            'anpa_take_key': None,
            'unique_id': 1,
            'type': 'text',
            'body_html': '<p>no body</p>',
            'word_count': '1',
            'priority': 1,
            'abstract': None
        }
        doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        item = doc['formatted_item'].replace(self.line_ender, self.line_feed)
        nitf_xml = etree.fromstring(item)
        self.assertIsNone(nitf_xml.find('head/meta[@name="anpa-takekey"]'))

    def testLocator(self):
        article = {
            '_id': '4853',
            'slugline': 'Gangs',
            'byline': '',
            'anpa_category': [
                {
                    'name': 'Australian General News',
                    'qcode': 'a'
                }
            ],
            'versioncreated': datetime(2018, 6, 13, 11, 45, 19, 0),
            'genre': [
                {
                    'name': 'Article (news)',
                    'qcode': 'Article'
                }
            ],
            'priority': 6,
            'unique_id': 33423059,
            'format': 'HTML',
            'guid': '4853',
            'headline': 'Drop gang campaign, bishop tells Vic Libs',
            'source': 'TEST',
            'subject': [
                {
                    'name': 'crime, law and justice',
                    'qcode': '02000000'
                }
            ],
            'flags': {
                'marked_for_sms': False,
                'marked_for_not_publication': False,
                'marked_archived_only': False,
                'marked_for_legal': False
            },
            'anpa_take_key': None,
            'pubstatus': 'usable',
            'schedule_settings': {
                'time_zone': None,
                'utc_embargo': None,
                'utc_publish_schedule': None
            },
            'urgency': 5,
            'word_count': 83,
            'type': 'text',
            'place': [
                {
                    'name': 'VIC',
                    'qcode': 'VIC',
                    'world_region': 'Oceania',
                    'state': 'Victoria',
                    'country': 'Australia',
                    'group': 'Australia'
                }
            ],
            'state': 'corrected',
            'body_html': '<p>A Melbourne-based Anglican bishop is calling on the Liberal party</P',
            '_current_version': 3,
            'sign_off': 'MG',
            'ednote': 'In the story \'Gangs\' sent at: 16/07/2018 15:26\r\n\r\nThis is a corrected repeat.',
            'sms_message': ''
        }

        doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        item = doc['formatted_item'].replace(self.line_ender, self.line_feed)
        nitf_xml = etree.fromstring(item)
        self.assertEqual(nitf_xml.find('head/title').text, 'VIC:Drop gang campaign, bishop tells Vic Libs')
        self.assertEqual(nitf_xml.find('body/body.head/hedline/hl1').text,
                         'VIC:Drop gang campaign, bishop tells Vic Libs')

        article['anpa_category'] = [{'name': 'Domestic Sports', 'qcode': 't'}]
        article['subject'] = [{'name': 'Cricket', 'qcode': '15017000'}]
        doc = self.formatter.format(article, {'name': 'Test Subscriber'})[0]
        item = doc['formatted_item'].replace(self.line_ender, self.line_feed)
        nitf_xml = etree.fromstring(item)
        self.assertEqual(nitf_xml.find('head/title').text, 'CRIK:Drop gang campaign, bishop tells Vic Libs')
        self.assertEqual(nitf_xml.find('body/body.head/hedline/hl1').text,
                         'CRIK:Drop gang campaign, bishop tells Vic Libs')
