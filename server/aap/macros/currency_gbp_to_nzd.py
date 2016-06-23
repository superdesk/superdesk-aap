# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import os
from . import aap_currency_base as currency_base
from decimal import Decimal

GBP_TO_NZD = Decimal('2.06')  # backup


def get_rate():
    """Get GBP to NZD rate."""
    try:
        return currency_base.get_rate('GBP', 'NZD')
    except:
        return GBP_TO_NZD


def gbp_to_nzd(item, **kwargs):
    """Convert NZD to GBP."""

    rate = kwargs.get('rate') or get_rate()
    if os.environ.get('BEHAVE_TESTING'):
        rate = GBP_TO_NZD

    regex = r'([£]|(GBP)|(STG))\s*\-?\s*\(?(((\d{1,3}((\,\d{3})*|\d*))?' \
            r'(\.\d{1,4})?)|((\d{1,3}((\,\d{3})*|\d*))(\.\d{0,4})?))\)?' \
            + currency_base.SUFFIX_REGEX

    return currency_base.do_conversion(item, rate, '$NZ', regex, match_index=0, value_index=4, suffix_index=17)


name = 'gbp_to_nzd'
label = 'Currency GBP to NZD'
callback = gbp_to_nzd
access_type = 'frontend'
action_type = 'interactive'
