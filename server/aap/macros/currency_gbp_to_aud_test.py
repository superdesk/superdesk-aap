# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from .currency_test_base import CurrencyTestClass
from .currency_gbp_to_aud import gbp_to_aud


class CurrencyTestCase(CurrencyTestClass):

    def test_gbp_to_aud(self):
        text = 'This is a £ 40 note. ' \
               'This is a £41 note. ' \
               'This is a £(42) note. ' \
               'This is a £46,483 note. ' \
               'This is a £4,648,382 note. ' \
               'This is a £4,648,382.20 ' \
               '£4,648,382.2 only ' \
               'This is (£4,648,382.2) only ' \
               'This is £4,648,820.20 only ' \
               '£46,483 only ' \
               'This is £(46.00) only ' \
               'This is a  GBP 52 note. ' \
               'This is a  GBP53 note. ' \
               'This is a  GBP(54,000) note. ' \
               'This is a  GBP (55,233.00) note. ' \
               'This is a  STG 52 note. ' \
               'This is a  STG53 note. ' \
               'This is a  STG(54,000) note. ' \
               'This is a  STG (55,233.00) note. ' \
               'This is a  GBP 52-million note. ' \
               'This is a  GBP 52 mln note. ' \
               'This is a  GBP53 b note. ' \
               'This is a  GBP(540,000) million note. ' \
               'This is a  GBP (55,233.00) million note. ' \
               'This is a  GBP (55,233.00 billion) note. ' \
               'This is a  1 million GBP note. ' \
               'This is a  4,648,382.20 pounds note. ' \
               'This is a  52 mln GBP note. ' \
               'This is a  53 b GBP note. ' \
               'This is a  52-million GBP note. ' \
               'This is a  200-GBP note. ' \
               'This is a  (55,233.00) GBP note. ' \
               'This is a  52 mln pounds note. ' \
               'This is a £ 40000 note. ' \

        item = {'body_html': text}
        res, diff = gbp_to_aud(item)
        self.assertEqual(diff['£ 40'], '£ 40 ($A80)')
        self.assertEqual(diff['£41'], '£41 ($A82)')
        self.assertEqual(diff['£(42)'], '£(42) ($A84)')
        self.assertEqual(diff['£46,483'], '£46,483 ($A92,966)')
        self.assertEqual(diff['£4,648,382'], '£4,648,382 ($A9.3 million)')
        self.assertEqual(diff['£4,648,382.20'], '£4,648,382.20 ($A9.30 million)')
        self.assertEqual(diff['GBP(54,000)'], 'GBP(54,000) ($A108,000)')
        self.assertEqual(diff['STG 52'], 'STG 52 ($A104)')
        self.assertEqual(diff['STG53'], 'STG53 ($A106)')
        self.assertEqual(diff['STG (55,233.00)'], 'STG (55,233.00) ($A110,466.00)')
        self.assertEqual(diff['GBP 52-million'], 'GBP 52-million ($A104 million)')
        self.assertEqual(diff['GBP 52 mln'], 'GBP 52 mln ($A104 mln)')
        self.assertEqual(diff['GBP53 b'], 'GBP53 b ($A106 b)')
        self.assertEqual(diff['GBP(540,000) million'], 'GBP(540,000) million ($A1,080 billion)')
        self.assertEqual(diff['GBP (55,233.00) million'], 'GBP (55,233.00) million ($A110.47 billion)')
        self.assertEqual(diff['GBP (55,233.00 billion)'], 'GBP (55,233.00 billion) ($A110.47 trillion)')
        self.assertEqual(diff['1 million GBP'], '1 million GBP ($A2.0 million)')
        self.assertEqual(diff['4,648,382.20 pounds'], '4,648,382.20 pounds ($A9.30 million)')
        self.assertEqual(diff['52 mln GBP'], '52 mln GBP ($A104 mln)')
        self.assertEqual(diff['53 b GBP'], '53 b GBP ($A106 b)')
        self.assertEqual(diff['52-million GBP'], '52-million GBP ($A104 million)')
        self.assertEqual(diff['200-GBP'], '200-GBP ($A400)')
        self.assertEqual(diff['(55,233.00) GBP'], '(55,233.00) GBP ($A110,466.00)')
        self.assertEqual(diff['52 mln pounds'], '52 mln pounds ($A104 mln)')
        self.assertEqual(diff['£ 40000'], '£ 40000 ($A80,000)')
