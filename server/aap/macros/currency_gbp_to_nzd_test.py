# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import unittest
from .currency_gbp_to_nzd import gbp_to_nzd
from decimal import Decimal


class CurrencyTestCase(unittest.TestCase):

    def test_gbp_to_nzd(self):
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
               'This is a  4,648,382.20 GBP note. ' \
               'This is a  52 mln GBP note. ' \
               'This is a  53 b GBP note. ' \
               'This is a  52-million GBP note. ' \
               'This is a  200-GBP note. ' \
               'This is a  (55,233.00) GBP note. ' \
               'This is a  52 mln pounds note. ' \
               'This is a £ 4000 note.' \

        item = {'body_html': text}
        res, diff = gbp_to_nzd(item, rate=Decimal(2))
        self.assertEqual(diff['£ 40'], '£ 40 ($NZ80)')
        self.assertEqual(diff['£41'], '£41 ($NZ82)')
        self.assertEqual(diff['£(42)'], '£(42) ($NZ84)')
        self.assertEqual(diff['£46,483'], '£46,483 ($NZ92,966)')
        self.assertEqual(diff['£4,648,382'], '£4,648,382 ($NZ9.3 million)')
        self.assertEqual(diff['£4,648,382.20'], '£4,648,382.20 ($NZ9.30 million)')
        self.assertEqual(diff['GBP(54,000)'], 'GBP(54,000) ($NZ108,000)')
        self.assertEqual(diff['STG 52'], 'STG 52 ($NZ104)')
        self.assertEqual(diff['STG53'], 'STG53 ($NZ106)')
        self.assertEqual(diff['STG (55,233.00)'], 'STG (55,233.00) ($NZ110,466.00)')
        self.assertEqual(diff['GBP 52-million'], 'GBP 52-million ($NZ104 million)')
        self.assertEqual(diff['GBP 52 mln'], 'GBP 52 mln ($NZ104 mln)')
        self.assertEqual(diff['GBP53 b'], 'GBP53 b ($NZ106 b)')
        self.assertEqual(diff['GBP(540,000) million'], 'GBP(540,000) million ($NZ1,080 billion)')
        self.assertEqual(diff['GBP (55,233.00) million'], 'GBP (55,233.00) million ($NZ110.47 billion)')
        self.assertEqual(diff['GBP (55,233.00 billion)'], 'GBP (55,233.00 billion) ($NZ110.47 trillion)')

        self.assertEqual(diff['1 million GBP'], '1 million GBP ($NZ2.0 million)')
        self.assertEqual(diff['4,648,382.20 GBP'], '4,648,382.20 GBP ($NZ9.30 million)')
        self.assertEqual(diff['52 mln GBP'], '52 mln GBP ($NZ104 mln)')
        self.assertEqual(diff['53 b GBP'], '53 b GBP ($NZ106 b)')
        self.assertEqual(diff['52-million GBP'], '52-million GBP ($NZ104 million)')
        self.assertEqual(diff['200-GBP'], '200-GBP ($NZ400)')
        self.assertEqual(diff['(55,233.00) GBP'], '(55,233.00) GBP ($NZ110,466.00)')
        self.assertEqual(diff['52 mln pounds'], '52 mln pounds ($NZ104 mln)')
        self.assertEqual(diff['£ 4000'], '£ 4000 ($NZ8,000)')
