# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from .currency_chf_to_aud import chf_to_aud
from .currency_test_base import CurrencyTestClass


class CurrencyTestCase(CurrencyTestClass):

    def test_chf_to_aud(self):
        text = 'This is a Fr 40 note. ' \
               'This is a Fr41 note. ' \
               'This is a Fr(42) note. ' \
               'This is a Fr46,483 note. ' \
               'This is a Fr4,648,382 note. ' \
               'This is a Fr4,648,382.20 ' \
               'This is a  CHF 52 note. ' \
               'This is a  CHF53 note. ' \
               'This is a  CHF(54,000) note. ' \
               'This is a  CHF (55,233.00) note. ' \
               'This is a  CHF 52-million note. ' \
               'This is a  CHF 52 mln note. ' \
               'This is a  CHF53 b note. ' \
               'This is a  CHF(540,000) million note. ' \
               'This is a  CHF (55,233.00) million note. ' \
               'This is a  CHF (55,233.00 billion) note. ' \
               'This is a 40 Franks note. ' \
               'This is a 4,648,382 Fr note. ' \
               'This is a 52 million CHF note. ' \
               'This is a Fr 4000 note. ' \

        item = {'body_html': text}
        res, diff = chf_to_aud(item)
        self.assertEqual(diff['Fr 40'], 'Fr 40 ($A80)')
        self.assertEqual(diff['Fr41'], 'Fr41 ($A82)')
        self.assertEqual(diff['Fr(42)'], 'Fr(42) ($A84)')
        self.assertEqual(diff['Fr46,483'], 'Fr46,483 ($A92,966)')
        self.assertEqual(diff['Fr4,648,382'], 'Fr4,648,382 ($A9.3 million)')
        self.assertEqual(diff['Fr4,648,382.20'], 'Fr4,648,382.20 ($A9.30 million)')
        self.assertEqual(diff['CHF(54,000)'], 'CHF(54,000) ($A108,000)')
        self.assertEqual(diff['CHF 52'], 'CHF 52 ($A104)')
        self.assertEqual(diff['CHF53'], 'CHF53 ($A106)')
        self.assertEqual(diff['CHF (55,233.00)'], 'CHF (55,233.00) ($A110,466.00)')
        self.assertEqual(diff['CHF 52-million'], 'CHF 52-million ($A104 million)')
        self.assertEqual(diff['CHF 52 mln'], 'CHF 52 mln ($A104 mln)')
        self.assertEqual(diff['CHF53 b'], 'CHF53 b ($A106 b)')
        self.assertEqual(diff['CHF(540,000) million'], 'CHF(540,000) million ($A1,080 billion)')
        self.assertEqual(diff['CHF (55,233.00) million'], 'CHF (55,233.00) million ($A110.47 billion)')
        self.assertEqual(diff['CHF (55,233.00 billion)'], 'CHF (55,233.00 billion) ($A110.47 trillion)')

        self.assertEqual(diff['40 Franks'], '40 Franks ($A80)')
        self.assertEqual(diff['4,648,382 Fr'], '4,648,382 Fr ($A9.3 million)')
        self.assertEqual(diff['52 million CHF'], '52 million CHF ($A104 million)')
        self.assertEqual(diff['Fr 4000'], 'Fr 4000 ($A8,000)')
