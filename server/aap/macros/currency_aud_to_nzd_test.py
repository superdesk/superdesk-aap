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
from .currency_aud_to_nzd import aud_to_nzd
from decimal import Decimal


class CurrencyTestCase(unittest.TestCase):

    def test_aud_to_nzd(self):
        text = 'This is a $A 40 note. ' \
               'This is a $A41 note. ' \
               'This is a $A(42) note. ' \
               'This is a $A46,483 note. ' \
               'This is a $A4,648,382 note. ' \
               'This is a $A4,648,382.20 ' \
               '$A4,648,382.2 only ' \
               'This is ($A4,648,382.2) only ' \
               'This is $A4,648,820.20 only ' \
               '$A46,483 only ' \
               'This is $A(46.00) only ' \
               'This is a  AUD 52 note. ' \
               'This is a  AUD53 note. ' \
               'This is a  AUD(54,000) note. ' \
               'This is a  AUD (55,233.00) note. ' \
               'This is a  AUD 52-million note. ' \
               'This is a  AUD 52 mln note. ' \
               'This is a  AUD53 b note. ' \
               'This is a  AUD(540,000) million note. ' \
               'This is a  AUD (55,233.00) million note. ' \
               'This is a  AUD (55,233.00 billion) note. ' \

        item = {'body_html': text}
        res, diff = aud_to_nzd(item, rate=Decimal(2))
        self.assertEqual(diff['AUD 52 mln'], 'AUD 52 mln ($NZ104  mln)')
        self.assertEqual(diff['AUD(540,000) million'], 'AUD(540,000) million ($NZ1,080,000  million)')
        self.assertEqual(diff['$A41'], '$A41 ($NZ82)')
        self.assertEqual(diff['$A46,483'], '$A46,483 ($NZ92,966)')
        self.assertEqual(diff['$A(46.00)'], '$A(46.00) ($NZ92.00)')
        self.assertEqual(diff['$A4,648,382'], '$A4,648,382 ($NZ9.3 million)')
        self.assertEqual(diff['AUD53'], 'AUD53 ($NZ106)')
        self.assertEqual(diff['AUD 52'], 'AUD 52 ($NZ104)')
        self.assertEqual(diff['AUD53 b'], 'AUD53 b ($NZ106  b)')
        self.assertEqual(diff['AUD(54,000)'], 'AUD(54,000) ($NZ108,000)')
        self.assertEqual(diff['$A(42)'], '$A(42) ($NZ84)')
        self.assertEqual(diff['AUD (55,233.00)'], 'AUD (55,233.00) ($NZ110,466.00)')
        self.assertEqual(diff['$A 40'], '$A 40 ($NZ80)')
        self.assertEqual(diff['$A4,648,382.2'], '$A4,648,382.2 ($NZ9.3 million)')
        self.assertEqual(diff['AUD (55,233.00) million'], 'AUD (55,233.00) million ($NZ110,466.00  million)')
        self.assertEqual(diff['AUD (55,233.00 billion)'], 'AUD (55,233.00 billion) ($NZ110,466.00  billion)')
        self.assertEqual(diff['$A4,648,820.20'], '$A4,648,820.20 ($NZ9.30 million)')
        self.assertEqual(diff['$A4,648,382.20'], '$A4,648,382.20 ($NZ9.30 million)')
        self.assertEqual(diff['AUD 52-million'], 'AUD 52-million ($NZ104 -million)')
