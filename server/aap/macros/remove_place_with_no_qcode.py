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


def remove_place_with_no_qcode(item, **kwargs):
    try:
        if 'place' in item:
            for p in item.get('place')[:]:
                if 'qcode' not in p:
                    item.get('place').remove(p)
        return item
    except:
        logger.warn('Exception caught in macro: remove_place_with_no_qcode')
        return item


name = 'Remove the place from an item if it has no qcode'
callback = remove_place_with_no_qcode
access_type = 'backend'
action_type = 'direct'
