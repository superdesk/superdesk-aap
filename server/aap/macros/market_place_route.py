# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
from .remove_place_with_no_qcode import remove_place_with_no_qcode
from .reuters_derive_dateline import reuters_derive_dateline
from aap.utils import remove_dateline


logger = logging.getLogger(__name__)


def market_place_route(item, **kwargs):
    try:
        if item.get('source', '').upper() == 'REUTERS' or item.get('source', '').upper() == 'RAW':
            remove_place_with_no_qcode(item)
            reuters_derive_dateline(item)

        if not item.get('keywords'):
            item['keywords'] = []

        # add marketplace keyword
        item['keywords'].append('marketplace')

        remove_dateline(item)
        return item
    except:
        logger.warning('Exception caught in macro: market_place_route_process')
        return item


name = 'market_place_route'
label = 'market_place_route'
callback = market_place_route
access_type = 'backend'
action_type = 'direct'
