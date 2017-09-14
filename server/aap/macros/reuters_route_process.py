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
from .remove_subjects import remove_subjects

logger = logging.getLogger(__name__)


def reuters_route_process(item, **kwargs):
    try:
        if (item.get('source', '').upper() == 'REUTERS' or item.get('source', '').upper() == 'RAW') and \
                item.get('state').upper() == 'INGESTED':
            remove_subjects(item)
            remove_place_with_no_qcode(item)
            reuters_derive_dateline(item)

            # set the category as international news
            item['anpa_category'] = [{'name': 'International News', 'qcode': 'i'}]

        return item
    except:
        logger.warning('Exception caught in macro: reuters route process')
        return item


name = 'reuters_route_process'
label = 'reuters_route_process'
callback = reuters_route_process
access_type = 'backend'
action_type = 'direct'
