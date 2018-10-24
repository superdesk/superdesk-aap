# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from . import aap_currency_base as currency_base
from copy import deepcopy


def get_rate():
    """Get CHF to AUD rate."""
    try:
        return currency_base.get_rate('CHF', 'AUD')
    except:
        raise LookupError('Failed to retrieve currency conversion rate')


def chf_to_aud(item, **kwargs):
    """Convert CHF to AUD."""

    rate = kwargs.get('rate') or get_rate()

    symbol_first_regex = r'((Fr)|(CHF))\s*\-?\s*\(?(((\d{1,}((\,\d{3})*|\d*))?' \
                         r'(\.\d{1,4})?)|((\d{1,}((\,\d{3})*|\d*))(\.\d{0,4})?))\)?' \
                         + currency_base.SUFFIX_REGEX

    symbol_last_regex = r'\(?(((\d{1,}((\,\d{3})*|\d*))?(\.\d{1,4})?)((\d{1,}((\,\d{3})*|\d*))(\.\d{0,4})?))' \
                        + currency_base.SECONDARY_SUFFIX_REGEX \
                        + r'\s?((CHF)|([f|F]ranks?)|(Fr))'

    symbol_first_result = currency_base.do_conversion(deepcopy(item),
                                                      rate,
                                                      '$A',
                                                      symbol_first_regex,
                                                      match_index=0,
                                                      value_index=4,
                                                      suffix_index=17)

    symbol_last_result = currency_base.do_conversion(deepcopy(item),
                                                     rate,
                                                     '$A',
                                                     symbol_last_regex,
                                                     match_index=0,
                                                     value_index=1,
                                                     suffix_index=13)

    symbol_first_result[1].update(symbol_last_result[1])

    return symbol_first_result


name = 'chf_to_aud'
label = 'Currency CHF to AUD'
callback = chf_to_aud
access_type = 'frontend'
action_type = 'interactive'
group = 'currency'
