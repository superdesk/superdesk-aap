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
from .currency_euro_to_aud import euro_to_aud
from decimal import Decimal


class CurrencyTestCase(unittest.TestCase):

    def test_gbp_to_aud(self):
        text = 'This is a € 40 note. ' \
               'This is a €41 note. ' \
               'This is a €(42) note. ' \
               'This is a €46,483 note. ' \
               'This is a €4,648,382 note. ' \
               'This is a €4,648,382.20 ' \
               '€4,648,382.2 only ' \
               'This is (€4,648,382.2) only ' \
               'This is €4,648,820.20 only ' \
               '€46,483 only ' \
               'This is €(46.00) only ' \
               'This is a  EUR 52 note. ' \
               'This is a  EUR53 note. ' \
               'This is a  EUR(54,000) note. ' \
               'This is a  EUR (55,233.00) note. ' \
               'This is a  EUR 52-million note. ' \
               'This is a  EUR 52 mln note. ' \
               'This is a  EUR53 b note. ' \
               'This is a  EUR(540,000) million note. ' \
               'This is a  EUR (55,233.00) million note. ' \
               'This is a  EUR (55,233.00 billion) note. ' \
               'This is a  52 Euro note. ' \
               'This is a  52 million euro note. ' \
               'This is a  54,000 EUR note. ' \
               'This is a  54,000 € note. ' \

        item = {'body_html': text}
        res, diff = euro_to_aud(item, rate=Decimal(2))
        self.assertEqual(diff['€ 40'], '€ 40 ($A80)')
        self.assertEqual(diff['€41'], '€41 ($A82)')
        self.assertEqual(diff['€(42)'], '€(42) ($A84)')
        self.assertEqual(diff['€46,483'], '€46,483 ($A92,966)')
        self.assertEqual(diff['€4,648,382'], '€4,648,382 ($A9.3 million)')
        self.assertEqual(diff['€4,648,382.20'], '€4,648,382.20 ($A9.30 million)')
        self.assertEqual(diff['EUR(54,000)'], 'EUR(54,000) ($A108,000)')
        self.assertEqual(diff['EUR 52'], 'EUR 52 ($A104)')
        self.assertEqual(diff['EUR53'], 'EUR53 ($A106)')
        self.assertEqual(diff['EUR (55,233.00)'], 'EUR (55,233.00) ($A110,466.00)')
        self.assertEqual(diff['EUR 52-million'], 'EUR 52-million ($A104 million)')
        self.assertEqual(diff['EUR 52 mln'], 'EUR 52 mln ($A104 mln)')
        self.assertEqual(diff['EUR53 b'], 'EUR53 b ($A106 b)')
        self.assertEqual(diff['EUR(540,000) million'], 'EUR(540,000) million ($A1,080 billion)')
        self.assertEqual(diff['EUR (55,233.00) million'], 'EUR (55,233.00) million ($A110.47 billion)')
        self.assertEqual(diff['EUR (55,233.00 billion)'], 'EUR (55,233.00 billion) ($A110.47 trillion)')

        self.assertEqual(diff['52 Euro'], '52 Euro ($A104)')
        self.assertEqual(diff['52 million euro'], '52 million euro ($A104 million)')
        self.assertEqual(diff['54,000 EUR'], '54,000 EUR ($A108,000)')
        self.assertEqual(diff['54,000 €'], '54,000 € ($A108,000)')
