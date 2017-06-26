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
from copy import deepcopy

CNY_TO_AUD = Decimal('0.21')  # backup


def get_rate():
    """Get CNY to AUD rate."""
    try:
        return currency_base.get_rate('CNY', 'AUD')
    except:
        return CNY_TO_AUD


def yuan_to_aud(item, **kwargs):
    """Convert CNY to AUD."""

    rate = kwargs.get('rate') or get_rate()
    if os.environ.get('BEHAVE_TESTING'):
        rate = CNY_TO_AUD

    symbol_first_regex = r'([¥]|(CNY)|(RMB)|(CN¥))\s*\-?\s*\(?(((\d{1,}((\,\d{3})*|\d*))?' \
                         r'(\.\d{1,4})?)|((\d{1,}((\,\d{3})*|\d*))(\.\d{0,4})?))\)?' \
                         + currency_base.SUFFIX_REGEX

    symbol_last_regex = r'\(?(((\d{1,}((\,\d{3})*|\d*))?(\.\d{1,4})?)((\d{1,}((\,\d{3})*|\d*))(\.\d{0,4})?))' \
                        + currency_base.SECONDARY_SUFFIX_REGEX \
                        + '\s?([¥]|(CNY)|(RMB)|(CN¥)|([y|Y]en)|([r|R]enminbi))'

    symbol_first_result = currency_base.do_conversion(deepcopy(item),
                                                      rate,
                                                      '$A',
                                                      symbol_first_regex,
                                                      match_index=0,
                                                      value_index=5,
                                                      suffix_index=18)

    symbol_last_result = currency_base.do_conversion(deepcopy(item),
                                                     rate,
                                                     '$A',
                                                     symbol_last_regex,
                                                     match_index=0,
                                                     value_index=1,
                                                     suffix_index=13)

    symbol_first_result[1].update(symbol_last_result[1])

    return symbol_first_result


name = 'yuan_to_aud'
label = 'Currency CNY to AUD'
callback = yuan_to_aud
access_type = 'frontend'
action_type = 'interactive'
group = 'currency'
