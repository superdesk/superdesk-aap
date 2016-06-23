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
from .currency_usd_to_nzd import usd_to_nzd
from decimal import Decimal


class CurrencyTestCase(unittest.TestCase):

    def test_usd_to_nzd(self):
        text = 'This is a $ 40 note. ' \
               'This is a $41 note. ' \
               'This is a $(42) note. ' \
               'This is a $46,483 note. ' \
               'This is a $4,648,382 note. ' \
               'This is a $4,648,382.20 ' \
               '$4,648,382.2 only ' \
               'This is ($4,648,382.2) only ' \
               'This is $4,648,820.20 only ' \
               '$46,483 only ' \
               'This is $(46.00) only ' \
               'This is a  USD 52 note. ' \
               'This is a  USD53 note. ' \
               'This is a  USD(54,000) note. ' \
               'This is a  USD (55,233.00) note. ' \
               'This is a  $US 52 note. ' \
               'This is a  $US53 note. ' \
               'This is a  $US58m note. ' \
               'This is a  $US(54,000) note. ' \
               'This is a  $US (55,233.00) note. ' \
               'This is a  $US 52-million note. ' \
               'This is a  $US 52 mln note. ' \
               'This is a  $US53 b note. ' \
               'This is a  $US(540,000) million note. ' \
               'This is a  $US (55,233.00) million note. ' \
               'This is a  $US (55,233.00 billion) note. ' \

        item = {'body_html': text}
        res, diff = usd_to_nzd(item, rate=Decimal(2))
        self.assertEqual(diff['$ 40'], '$ 40 ($NZ80)')
        self.assertEqual(diff['$41'], '$41 ($NZ82)')
        self.assertEqual(diff['$(42)'], '$(42) ($NZ84)')
        self.assertEqual(diff['$46,483'], '$46,483 ($NZ92,966)')
        self.assertEqual(diff['$4,648,382'], '$4,648,382 ($NZ9.3 million)')
        self.assertEqual(diff['$4,648,382.20'], '$4,648,382.20 ($NZ9.30 million)')
        self.assertEqual(diff['USD(54,000)'], 'USD(54,000) ($NZ108,000)')
        self.assertEqual(diff['USD 52'], 'USD 52 ($NZ104)')
        self.assertEqual(diff['USD53'], 'USD53 ($NZ106)')
        self.assertEqual(diff['USD (55,233.00)'], 'USD (55,233.00) ($NZ110,466.00)')
        self.assertEqual(diff['$US(54,000)'], '$US(54,000) ($NZ108,000)')
        self.assertEqual(diff['$US 52'], '$US 52 ($NZ104)')
        self.assertEqual(diff['$US53'], '$US53 ($NZ106)')
        self.assertEqual(diff['$US58m'], '$US58m ($NZ116 m)')
        self.assertEqual(diff['$US (55,233.00)'], '$US (55,233.00) ($NZ110,466.00)')
        self.assertEqual(diff['$US 52-million'], '$US 52-million ($NZ104 million)')
        self.assertEqual(diff['$US 52 mln'], '$US 52 mln ($NZ104 mln)')
        self.assertEqual(diff['$US53 b'], '$US53 b ($NZ106 b)')
        self.assertEqual(diff['$US(540,000) million'], '$US(540,000) million ($NZ1,080 billion)')
        self.assertEqual(diff['$US (55,233.00) million'], '$US (55,233.00) million ($NZ110.47 billion)')
        self.assertEqual(diff['$US (55,233.00 billion)'], '$US (55,233.00 billion) ($NZ110.47 trillion)')
