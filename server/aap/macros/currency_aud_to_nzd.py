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

AUD_TO_NZD = Decimal('1.04')  # backup


def get_rate():
    """Get AUD to NZD rate."""
    try:
        return currency_base.get_rate('AUD', 'NZD')
    except:
        return AUD_TO_NZD


def aud_to_nzd(item, **kwargs):
    """Convert AUD to NZD."""

    rate = kwargs.get('rate') or get_rate()
    if os.environ.get('BEHAVE_TESTING'):
        rate = AUD_TO_NZD

    regex = r'((AUD)|(\$A)|(\$AU)|(\$))\s*\-?\s*\(?(((\d{1,3}((\,\d{3})*|\d*))?' \
            r'(\.\d{1,4})?)|((\d{1,3}((\,\d{3})*|\d*))(\.\d{0,4})?))\)?' \
            + currency_base.SUFFIX_REGEX

    return currency_base.do_conversion(item, rate, '$NZ', regex, match_index=0, value_index=6, suffix_index=17)


name = 'aud_to_nzd'
label = 'Currency AUD to NZD'
callback = aud_to_nzd
access_type = 'frontend'
action_type = 'interactive'
