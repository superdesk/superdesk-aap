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
from .currency_jpy_to_aud import yen_to_aud
from decimal import Decimal


class CurrencyTestCase(unittest.TestCase):

    def test_jpy_to_aud(self):
        text = 'This is a ¥ 40 note. ' \
               'This is a ¥41 note. ' \
               'This is a ¥(42) note. ' \
               'This is a ¥46,483 note. ' \
               'This is a ¥4,648,382 note. ' \
               'This is a ¥4,648,382.20 ' \
               '¥4,648,382.2 only ' \
               'This is (¥4,648,382.2) only ' \
               'This is ¥4,648,820.20 only ' \
               '¥46,483 only ' \
               'This is ¥(46.00) only ' \
               'This is a  JPY 52 note. ' \
               'This is a  JPY53 note. ' \
               'This is a  JPY(54,000) note. ' \
               'This is a  JPY (55,233.00) note. ' \
               'This is a  100-JPY note. ' \
               'This is a  JPY 52-million note. ' \
               'This is a  JPY 52 mln note. ' \
               'This is a  JPY53 b note. ' \
               'This is a  JPY(540,000) million note. ' \
               'This is a  JPY (55,233.00) million note. ' \
               'This is a  JPY (55,233.00 billion) note. ' \

        item = {'body_html': text}
        res, diff = yen_to_aud(item, rate=Decimal(2))
        self.assertEqual(diff['¥ 40'], '¥ 40 ($A80)')
        self.assertEqual(diff['¥41'], '¥41 ($A82)')
        self.assertEqual(diff['¥(42)'], '¥(42) ($A84)')
        self.assertEqual(diff['¥46,483'], '¥46,483 ($A92,966)')
        self.assertEqual(diff['¥4,648,382'], '¥4,648,382 ($A9.3 million)')
        self.assertEqual(diff['¥4,648,382.20'], '¥4,648,382.20 ($A9.30 million)')
        self.assertEqual(diff['JPY(54,000)'], 'JPY(54,000) ($A108,000)')
        self.assertEqual(diff['JPY 52'], 'JPY 52 ($A104)')
        self.assertEqual(diff['JPY53'], 'JPY53 ($A106)')
        self.assertEqual(diff['JPY (55,233.00)'], 'JPY (55,233.00) ($A110,466.00)')
        self.assertEqual(diff['JPY 52-million'], 'JPY 52-million ($A104 million)')
        self.assertEqual(diff['JPY 52 mln'], 'JPY 52 mln ($A104 mln)')
        self.assertEqual(diff['JPY53 b'], 'JPY53 b ($A106 b)')
        self.assertEqual(diff['JPY(540,000) million'], 'JPY(540,000) million ($A1,080 billion)')
        self.assertEqual(diff['JPY (55,233.00) million'], 'JPY (55,233.00) million ($A110.47 billion)')
        self.assertEqual(diff['JPY (55,233.00 billion)'], 'JPY (55,233.00 billion) ($A110.47 trillion)')
