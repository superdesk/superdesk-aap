# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from .currency_nzd_to_aud import nzd_to_aud
from .currency_test_base_test import CurrencyTestClass


class CurrencyTestCase(CurrencyTestClass):

    def test_nzd_to_aud(self):
        self.resp = {'success': True, 'rates': {"AUD": 2.0, "NZD": 1.0}}
        text = 'This is a NZ$ 40 note. ' \
               'This is a NZ$41 note. ' \
               'This is a NZ$(42) note. ' \
               'This is a NZ$46,483 note. ' \
               'This is a NZ$4,648,382 note. ' \
               'This is a NZ$4,648,382.20 ' \
               'NZ$4,648,382.2 only ' \
               'This is (NZ$4,648,382.2) only ' \
               'This is NZ$4,648,820.20 only ' \
               'NZ$46,483 only ' \
               'This is NZ$(46.00) only ' \
               'This is a  NZD 52 note. ' \
               'This is a  NZD53 note. ' \
               'This is a  NZD(54,000) note. ' \
               'This is a  NZD (55,233.00) note. ' \
               'This is a  NZD 52-million note. ' \
               'This is a  NZD 52 mln note. ' \
               'This is a  NZD53 b note. ' \
               'This is a  NZD(540,000) million note. ' \
               'This is a  NZD (55,233.00) million note. ' \
               'This is a  NZD (55,233.00 billion) note. ' \
               'This is a NZ$ 4000 note. ' \
               'This is a $NZ 500 note. ' \

        item = {'body_html': text}
        self.clearCache()
        res, diff = nzd_to_aud(item)
        self.clearCache()
        self.assertEqual(diff['NZ$ 40'], 'NZ$ 40 ($A80)')
        self.assertEqual(diff['NZ$41'], 'NZ$41 ($A82)')
        self.assertEqual(diff['NZ$(42)'], 'NZ$(42) ($A84)')
        self.assertEqual(diff['NZ$46,483'], 'NZ$46,483 ($A92,966)')
        self.assertEqual(diff['NZ$4,648,382'], 'NZ$4,648,382 ($A9.3 million)')
        self.assertEqual(diff['NZ$4,648,382.20'], 'NZ$4,648,382.20 ($A9.30 million)')
        self.assertEqual(diff['NZD(54,000)'], 'NZD(54,000) ($A108,000)')
        self.assertEqual(diff['NZD 52'], 'NZD 52 ($A104)')
        self.assertEqual(diff['NZD53'], 'NZD53 ($A106)')
        self.assertEqual(diff['NZD (55,233.00)'], 'NZD (55,233.00) ($A110,466.00)')
        self.assertEqual(diff['NZD 52-million'], 'NZD 52-million ($A104 million)')
        self.assertEqual(diff['NZD 52 mln'], 'NZD 52 mln ($A104 mln)')
        self.assertEqual(diff['NZD53 b'], 'NZD53 b ($A106 b)')
        self.assertEqual(diff['NZD(540,000) million'], 'NZD(540,000) million ($A1,080 billion)')
        self.assertEqual(diff['NZD (55,233.00) million'], 'NZD (55,233.00) million ($A110.47 billion)')
        self.assertEqual(diff['NZD (55,233.00 billion)'], 'NZD (55,233.00 billion) ($A110.47 trillion)')
        self.assertEqual(diff['NZ$ 4000'], 'NZ$ 4000 ($A8,000)')
        self.assertEqual(diff['$NZ 500'], '$NZ 500 ($A1,000)')
        self.assertEqual(res['body_html'], item['body_html'])
