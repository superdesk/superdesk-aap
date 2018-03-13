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


def get_rate():
    """Get NZD to AUD rate."""
    try:
        return currency_base.get_rate('NZD', 'AUD')
    except:
        raise LookupError('Failed to retrieve currency conversion rate')


def nzd_to_aud(item, **kwargs):
    """Convert NZD to GBP."""

    rate = get_rate()

    regex = r'((NZD)|(NZ\$))\s*\-?\s*\(?(((\d{1,}((\,\d{3})*|\d*))?' \
            r'(\.\d{1,4})?)|((\d{1,}((\,\d{3})*|\d*))(\.\d{0,4})?))\)?' \
            + currency_base.SUFFIX_REGEX

    return currency_base.do_conversion(item, rate, '$A', regex, match_index=0, value_index=4, suffix_index=17)


name = 'nzd_to_aud'
label = 'Currency NZD to AUD'
callback = nzd_to_aud
access_type = 'frontend'
action_type = 'interactive'
group = 'currency'
