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


logger = logging.getLogger(__name__)


def ap_wire_aapx_route(item, **kwargs):
    try:
        if not item.get('keywords'):
            item['keywords'] = []

        # add marketplace keyword
        item['keywords'].append('marketplace')

        return item
    except:
        logger.warning('Exception caught in macro: market_place_route_process')
        return item


name = 'AP wire AAPX route'
label = 'AP wire AAPX route'
callback = ap_wire_aapx_route
access_type = 'backend'
action_type = 'direct'
