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
from superdesk.metadata.item import FORMAT, FORMATS
from superdesk.tests import TestCase

from .aap_formatter_common import map_priority
from .anpa_formatter import AAPAnpaFormatter


class ANPAFormatterTest(TestCase):
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
        {'is_active': True, 'name': 'bogus', 'qcode': 'b'}]}]

    def setUp(self):
        self.app.data.insert('subscribers', self.subscribers)
        self.app.data.insert('desks', self.desks)
        self.app.data.insert('vocabularies', self.vocab)
        init_app(self.app)

    def testANPAFormatter(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = AAPAnpaFormatter()
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
        self.assertEqual(line[0:20], 'f a bc-slugline   ')  # skip the date

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
        self.assertEqual(line.strip(), 'AAP')

    def testANPAWithNoSelectorsFormatter(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]
        subscriber['name'] = 'not notes'

        f = AAPAnpaFormatter()
        resp = f.format(self.article.copy(), subscriber)[0]
        seq = resp['published_seq_num']
        item = resp['encoded_item']

        self.assertGreater(int(seq), 0)

        lines = io.StringIO(item.decode())

        line = lines.readline()
        self.assertEqual(line[:3], '')  # Skip the sequence

        line = lines.readline()
        self.assertEqual(line[0:20], 'f a bc-slugline   ')  # skip the date

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
        self.assertEqual(line.strip(), 'AAP')

    def testANPAWithBylineFormatter(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]
        subscriber['name'] = 'not notes'
        byline_article = dict(self.article.copy())
        byline_article['byline'] = '<p>Joe Blogs</p>'

        f = AAPAnpaFormatter()
        resp = f.format(byline_article, subscriber)[0]
        seq = resp['published_seq_num']
        item = resp['encoded_item']

        self.assertGreater(int(seq), 0)

        lines = io.StringIO(item.decode())

        line = lines.readline()
        self.assertEqual(line[:3], '')  # Skip the sequence

        line = lines.readline()
        self.assertEqual(line[0:20], 'f a bc-slugline   ')  # skip the date

        line = lines.readline()
        self.assertEqual(line.strip(), 'This is a test headline')

        line = lines.readline()
        self.assertEqual(line.strip(), 'slugline take_key')

        line = lines.readline()
        self.assertEqual(line.strip(), 'Joe Blogs')

        line = lines.readline()
        self.assertEqual(line.strip(), 'The story body')

        line = lines.readline()
        self.assertEqual(line.strip(), 'call helpline 999 if you are planning')

        line = lines.readline()
        self.assertEqual(line.strip(), 'to quit smoking')

        lines.readline()
        line = lines.readline()
        self.assertEqual(line.strip(), 'AAP')

    def testServiceLevelFormatter(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]
        subscriber['name'] = 'not notes'
        service_level_article = dict(self.article.copy())
        service_level_article['genre'] = [{'qcode': 'Results (sport)'}]
        service_level_article['anpa_category'] = [{'qcode': 'S'}]
        f = AAPAnpaFormatter()
        resp = f.format(service_level_article, subscriber)[0]
        seq = resp['published_seq_num']
        item = resp['encoded_item']

        self.assertGreater(int(seq), 0)

        lines = io.StringIO(item.decode())

        line = lines.readline()
        self.assertEqual(line[:3], '')  # Skip the sequence

        line = lines.readline()
        self.assertEqual(line[0:20], 'f s bc-slugline   ')  # skip the date

    def testMultipleCategoryFormatter(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]
        multi_article = dict(self.article.copy())
        multi_article.pop('anpa_category')
        multi_article['anpa_category'] = [{'qcode': 'a'}, {'qcode': 'b'}]
        f = AAPAnpaFormatter()
        docs = f.format(multi_article, subscriber, ['Axy', 'Bkl'])
        docs = f.format(multi_article, subscriber, ['Axy', 'Bkl'])

        self.assertEqual(len(docs), 2)
        cat = 'a'
        for doc in docs:
            item = doc['encoded_item']
            lines = io.StringIO(item.decode())
            line = lines.readline()
            line = lines.readline()
            line = lines.readline()
            self.assertEqual(line[2:3], cat)  # skip the date
            cat = 'b'

    def test_process_headline_empty_sequence_short_headline(self):
        f = AAPAnpaFormatter()
        article = {'headline': '1234567890' * 5}
        anpa = []
        f._process_headline(anpa, article, b'a')
        self.assertEqual(anpa[0], b'12345678901234567890123456789012345678901234567890')

    def test_headline_with_markup(self):
        f = AAPAnpaFormatter()
        article = {'headline': '<p>headline</p>'}
        anpa = []
        f._process_headline(anpa, article, b'a')
        self.assertEqual(anpa[0], b'headline')

    def test_process_headline_empty_sequence_long_headline(self):
        f = AAPAnpaFormatter()
        article = {'headline': '1234567890' * 7}
        anpa = []
        f._process_headline(anpa, article, b'a')
        self.assertEqual(anpa[0], b'1234567890123456789012345678901234567890123456789012345678901234')

    def test_process_headline_with_sequence_short_headline(self):
        f = AAPAnpaFormatter()
        article = {'headline': '1234567890=7', 'sequence': 7}
        anpa = []
        f._process_headline(anpa, article, b'a')
        self.assertEqual(anpa[0], b'1234567890=7')

    def test_process_headline_with_sequence_long_headline(self):
        f = AAPAnpaFormatter()
        article1 = {'headline': '1234567890' * 7 + '=7', 'sequence': 7}
        anpa = []
        f._process_headline(anpa, article1, b'a')
        self.assertEqual(anpa[0], b'12345678901234567890123456789012345678901234567890123456789012=7')
        article2 = {'headline': '1234567890' * 7 + '=7', 'sequence': 17}
        anpa = []
        f._process_headline(anpa, article2, b'a')
        self.assertEqual(anpa[0], b'1234567890123456789012345678901234567890123456789012345678901=17')

    def test_process_headline_locator_inject(self):
        f = AAPAnpaFormatter()
        article3 = {'headline': '1234567890' * 3, 'place': [{'qcode': 'VIC', 'name': 'VIC'}]}
        anpa = []
        f._process_headline(anpa, article3, b'a')
        self.assertEqual(anpa[0], b'VIC:123456789012345678901234567890')

    def test_map_priority(self):
        self.assertEqual('f', map_priority(1))
        self.assertEqual('u', map_priority(2))
        self.assertEqual('b', map_priority(3))
        self.assertEqual('r', map_priority(4))
        self.assertEqual('r', map_priority(5))
        self.assertEqual('r', map_priority(6))
        self.assertEqual('r', map_priority(None))
        self.assertEqual('r', map_priority(7))
        self.assertEqual('r', map_priority(''))

    def test_dateline_with_empty_text(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item.update({'dateline': {'text': None}})
        resp = f.format(item, subscriber)[0]
        self.assertTrue('The story body' in resp['encoded_item'].decode('ascii'))

    def test_dateline_injection(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item.update({'dateline': {'text': 'SYDNEY, June 27 AAP -'}})
        resp = f.format(item, subscriber)[0]
        out = resp['encoded_item']
        lines = io.StringIO(out.decode())
        self.assertTrue(lines.getvalue().find('SYDNEY, June 27 AAP - The story body') > 0)

    def test_ednote_injection(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item.update({'ednote': 'Note this'})
        resp = f.format(item, subscriber)[0]
        out = resp['encoded_item']
        lines = io.StringIO(out.decode())
        self.assertTrue(lines.getvalue().find('Note this') > 0)

    def test_div_body(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item.update({
            'body_html': '<div>Kathmandu Holdings has lodged a claim in the New Zealand High'
                         ' Court for the recovery of costs associated with last year\'s takeover bid from Briscoe'
                         ' Group.</div><div>Kathmandu Holdings has lodged a claim in the New Zealand High Court for '
                         'the recovery of costs associated with last year\'s takeover bid from Briscoe Group.'
                         '</div><div><br></div><div>Kathmandu incurred costs in relation to the takeover bid. '
                         'After an initial request for payment on November 20, 2015 and subsequent correspondence, '
                         'Briscoe made a payment of $637,711.65 on May 25, 2016 without prejudice to its position on '
                         'what sum Kathmandu is entitled to recover.</div><div><br></div><div>Kathmandu considers the '
                         'full amount claimed is recoverable and has issued legal proceedings for the balance of monies'
                         ' owed.</div>'})
        resp = f.format(item, subscriber)[0]
        out = resp['encoded_item']
        lines = io.StringIO(out.decode())
        self.assertTrue(lines.getvalue().split('\n')[6].find('   Kathmandu incurred costs in relation') == 0)

    def test_span_body(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item.update({
            'body_html': '<p>Dental materials maker and marketer SDI has boosted its shares after reporting a lift in'
            ' sales, with improvements across Europe, Brazil and North America.</p>'
            '<p>SDI&nbsp;<span style=\"background-color: transparent;\">reported a 7.8 per cent lift in unaudited'
            ' sales to $74 million for the year to June 30, 2016 on Monday, up from $68.7 million a year '
            'earlier.</span></p><p>The company said it expected to report a post-tax profit of between $7.2 million '
            'and $7.8 million when it releases its full-year results on August 29.</p><p>Shares in SDI gained '
            '6.5 cents - a 12.2 per cent increase - to close at 59.5 cents on Monday.</p>'})
        resp = f.format(item, subscriber)[0]
        out = resp['encoded_item']
        lines = io.StringIO(out.decode())
        self.assertTrue(lines.getvalue().split('\n')[5].find('   SDI reported a 7.8 per cent lift in unaudited') == 0)

    def test_br_body(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item.update({
            'body_html': '<p>Dental materials maker and marketer SDI<br> has boosted its shares after '
            'reporting a lift in'
            ' sales, with improvements across Europe, Brazil and North America.</p>'
            '<p>SDI&nbsp;<span style=\"background-color: transparent;\">reported a 7.8 per cent lift in unaudited'
            ' sales to $74 million for the year to June 30, 2016 on Monday, up from $68.7 million a year '
            'earlier.</span></p><p>The company said it expected to report a post-tax profit of between $7.2 million '
            'and $7.8 million when it releases its full-year results on August 29.</p><p>Shares in SDI gained '
            '6.5 cents - a 12.2 per cent increase - to close at 59.5 cents on Monday.</p>'})
        resp = f.format(item, subscriber)[0]
        out = resp['encoded_item']

        lines = io.StringIO(out.decode())
        self.assertTrue(lines.getvalue().split('\n')[4].find('   Dental materials maker and marketer SDI') == 0)
        self.assertTrue(lines.getvalue().split('\n')[5].find(' has boosted its shares after reporting') == 0)

    def test_none_body(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item.update({
            'anpa_take_key': None, 'byline': None, 'abstract': None})
        resp = f.format(item, subscriber)[0]
        self.assertTrue('encoded_item' in resp)

    def test_EM_html(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item['body_html'] = '<p>stuff\x19\r\nmore stuff<\p>'
        resp = f.format(item, subscriber)[0]
        self.assertTrue('stuff\r\nmore stuff' in resp['encoded_item'].decode('ascii'))

    def test_EM_preserved(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item[FORMAT] = FORMATS.PRESERVED
        item['body_html'] = 'stuff\x19\r\nmore stuff'
        resp = f.format(item, subscriber)[0]
        self.assertTrue('stuff\r\nmore stuff' in resp['encoded_item'].decode('ascii'))
