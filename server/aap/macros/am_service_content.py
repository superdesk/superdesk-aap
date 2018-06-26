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


def am_service_content(item, **kwargs):
    try:
        # set the category as international news
        if item.get('type') == 'text':
            item['genre'] = [{'name': 'AM Service', 'qcode': 'AM Service'}]
            if item.get('slugline') and item.get('slugline')[:3] != 'AM ':
                item['slugline'] = 'AM {}'.format(item.get('slugline'))
        return item
    except:
        logger.warning('Exception caught in macro: am_service_content')
        return item


name = 'am_service_content'
label = 'AM Service Content'
callback = am_service_content
access_type = 'backend'
action_type = 'direct'
