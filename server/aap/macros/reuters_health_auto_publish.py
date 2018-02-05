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

logger = logging.getLogger(__name__)


def reuters_health_auto_publish(item, **kwargs):
    try:
        if (item.get('source', '').upper() == 'REUTERS' or item.get('source', '').upper() == 'RAW') and \
                item.get('state').upper() == 'INGESTED':
            remove_place_with_no_qcode(item)
            reuters_derive_dateline(item)

            # set the category as international news
            item['anpa_category'] = [{'name': 'International News', 'qcode': 'i'}]

            # anything starting with health topic is first subject.
            if item.get('subject'):
                item['subject'] = sorted(item.get('subject'),
                                         key=lambda s: 0 if s.get('qcode').startswith('07') else 1)

        return item
    except:
        logger.warning('Exception caught in macro: reuters route process')
        return item


name = 'reuters_health_auto_publish'
label = 'reuters_health_auto_publish'
callback = reuters_health_auto_publish
access_type = 'backend'
action_type = 'direct'
