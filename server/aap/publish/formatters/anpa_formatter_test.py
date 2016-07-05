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
from .anpa_formatter import AAPAnpaFormatter
from .aap_formatter_common import map_priority
from datetime import datetime
import io


class ANPAFormatterTest(SuperdeskTestCase):
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

    def setUp(self):
        super().setUp()
        self.app.data.insert('subscribers', self.subscribers)
        self.app.data.insert('desks', self.desks)
        init_app(self.app)

    def testANPAFormatter(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]

        f = AAPAnpaFormatter()
        seq, item = f.format(self.article.copy(), subscriber, ['axx'])[0]

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
        seq, item = f.format(self.article.copy(), subscriber)[0]

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
        byline_article['byline'] = 'Joe Blogs'

        f = AAPAnpaFormatter()
        seq, item = f.format(byline_article, subscriber)[0]

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

    def testMultipleCategoryFormatter(self):
        subscriber = self.app.data.find('subscribers', None, None)[0]
        multi_article = dict(self.article.copy())
        multi_article.pop('anpa_category')
        multi_article['anpa_category'] = [{'qcode': 'a'}, {'qcode': 'b'}]
        f = AAPAnpaFormatter()
        docs = f.format(multi_article, subscriber, ['Axy', 'Bkl'])
        self.assertEqual(len(docs), 2)
        cat = 'a'
        for seq, doc in docs:
            lines = io.StringIO(doc.decode())
            line = lines.readline()
            line = lines.readline()
            line = lines.readline()
            self.assertEqual(line[2:3], cat)  # skip the date
            cat = 'b'

    def test_process_headline_empty_sequence_short_headline(self):
        f = AAPAnpaFormatter()
        article = {'headline': '1234567890' * 5}
        anpa = []
        f._process_headline(anpa, article, 'a')
        self.assertEqual(anpa[0], b'12345678901234567890123456789012345678901234567890')

    def test_process_headline_empty_sequence_long_headline(self):
        f = AAPAnpaFormatter()
        article = {'headline': '1234567890' * 7}
        anpa = []
        f._process_headline(anpa, article, 'a')
        self.assertEqual(anpa[0], b'1234567890123456789012345678901234567890123456789012345678901234')

    def test_process_headline_with_sequence_short_headline(self):
        f = AAPAnpaFormatter()
        article = {'headline': '1234567890=7', 'sequence': 7}
        anpa = []
        f._process_headline(anpa, article, 'a')
        self.assertEqual(anpa[0], b'1234567890=7')

    def test_process_headline_with_sequence_long_headline(self):
        f = AAPAnpaFormatter()
        article1 = {'headline': '1234567890' * 7 + '=7', 'sequence': 7}
        anpa = []
        f._process_headline(anpa, article1, 'a')
        self.assertEqual(anpa[0], b'12345678901234567890123456789012345678901234567890123456789012=7')
        article2 = {'headline': '1234567890' * 7 + '=7', 'sequence': 17}
        anpa = []
        f._process_headline(anpa, article2, 'a')
        self.assertEqual(anpa[0], b'1234567890123456789012345678901234567890123456789012345678901=17')

    def test_process_headline_locator_inject(self):
        f = AAPAnpaFormatter()
        article3 = {'headline': '1234567890' * 3, 'place': [{'qcode': 'VIC', 'name': 'VIC'}]}
        anpa = []
        f._process_headline(anpa, article3, 'a')
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
        seq, out = f.format(item, subscriber)[0]

    def test_dateline_injection(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item.update({'dateline': {'text': 'SYDNEY, June 27 AAP -'}})
        seq, out = f.format(item, subscriber)[0]
        lines = io.StringIO(out.decode())
        self.assertTrue(lines.getvalue().find('SYDNEY, June 27 AAP - The story body') > 0)

    def test_ednote_injection(self):
        f = AAPAnpaFormatter()
        subscriber = self.app.data.find('subscribers', None, None)[0]
        item = self.article.copy()
        item.update({'ednote': 'Note this'})
        seq, out = f.format(item, subscriber)[0]
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
        seq, out = f.format(item, subscriber)[0]
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
        seq, out = f.format(item, subscriber)[0]
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
        seq, out = f.format(item, subscriber)[0]
        lines = io.StringIO(out.decode())
        self.assertTrue(lines.getvalue().split('\n')[4].find('   Dental materials maker and marketer SDI') == 0)
        self.assertTrue(lines.getvalue().split('\n')[5].find(' has boosted its shares after reporting') == 0)
