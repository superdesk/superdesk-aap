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
from .aap_currency_base import update_suffix
from decimal import Decimal


class CurrencyBaseTestCase(unittest.TestCase):

    def test_update_suffix(self):
        value, suffix, precision = update_suffix(Decimal(250), None)
        self.assertTupleEqual((value, suffix), (Decimal(250), None))
        value, suffix, precision = update_suffix(Decimal(2500), None)
        self.assertTupleEqual((value, suffix), (Decimal(2500), None))
        value, suffix, precision = update_suffix(Decimal(25000), None)
        self.assertTupleEqual((value, suffix), (Decimal(25000), None))
        value, suffix, precision = update_suffix(Decimal(250000), None)
        self.assertTupleEqual((value, suffix), (Decimal(250000), None))

        value, suffix, precision = update_suffix(Decimal(1200000), None)
        value = Decimal(1200000) / Decimal(1000000)
        self.assertTupleEqual((value, suffix), (value, 'million'))

        value, suffix, precision = update_suffix(Decimal(250), 'million')
        self.assertTupleEqual((value, suffix), (Decimal(250), 'million'))
        value, suffix, precision = update_suffix(Decimal(2500), 'million')
        self.assertTupleEqual((value, suffix), (Decimal(2.5), 'billion'))
        value, suffix, precision = update_suffix(Decimal(25000), 'million')
        self.assertTupleEqual((value, suffix), (Decimal(25), 'billion'))
        value, suffix, precision = update_suffix(Decimal(250000), 'million')
        self.assertTupleEqual((value, suffix), (Decimal(250), 'billion'))

        value, suffix, precision = update_suffix(Decimal(250), 'billion')
        self.assertTupleEqual((value, suffix), (Decimal(250), 'billion'))
        value, suffix, precision = update_suffix(Decimal(3500), 'billion')
        value = Decimal(3500) / Decimal(1000)
        self.assertTupleEqual((value, suffix), (value, 'trillion'))
