# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from .currency_usd_to_nzd import usd_to_nzd
from .currency_test_base import CurrencyTestClass


class CurrencyTestCase(CurrencyTestClass):

    def test_usd_to_nzd(self):
        self.resp = {'success': True, 'rates': {"NZD": 2.0, "USD": 1.0}}
        self.clearCache()
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
               'This is a  1 million dollars note. ' \
               'This is a  4,648,382.20 USD note. ' \
               'This is a  52 mln $US note. ' \
               'This is a  53 b dollars note. ' \
               'This is a  52-million dollars note. ' \
               'This is a  200-USD note. ' \
               'This is a  (55,233.00) USD note. ' \
               'This is a  $US3434 note. ' \
               'This is a  $US3,434 note. ' \
               'This is a  3434 USD note. ' \
               'This is a  3434 dollars. ' \

        item = {'body_html': text}
        res, diff = usd_to_nzd(item)
        self.clearCache()

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

        self.assertEqual(diff['1 million dollars'], '1 million dollars ($NZ2.0 million)')
        self.assertEqual(diff['4,648,382.20 USD'], '4,648,382.20 USD ($NZ9.30 million)')
        self.assertEqual(diff['52 mln $US'], '52 mln $US ($NZ104 mln)')
        self.assertEqual(diff['53 b dollars'], '53 b dollars ($NZ106 b)')
        self.assertEqual(diff['52-million dollars'], '52-million dollars ($NZ104 million)')
        self.assertEqual(diff['200-USD'], '200-USD ($NZ400)')
        self.assertEqual(diff['(55,233.00) USD'], '(55,233.00) USD ($NZ110,466.00)')
        self.assertEqual(diff['$US3434'], '$US3434 ($NZ6,868)')
        self.assertEqual(diff['$US3,434'], '$US3,434 ($NZ6,868)')
        self.assertEqual(diff['$US3,434'], '$US3,434 ($NZ6,868)')
        self.assertEqual(diff['3434 USD'], '3434 USD ($NZ6,868)')
        self.assertEqual(diff['3434 dollars'], '3434 dollars ($NZ6,868)')
