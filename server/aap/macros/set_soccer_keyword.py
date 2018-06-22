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


def set_soccer_keyword_process(item, **kwargs):
    """
    This macro simply appends the keyword 'RAW SOCCER' to the keywords
    :param item:
    :param kwargs:
    :return:
    """
    try:
        if (item.get('type') == 'text'):
            if (item.get('keywords')):
                item.get('keywords', []).append('RAW SOCCER')
            else:
                item['keywords'] = ['RAW SOCCER']
        return item
    except:
        logger.warning('Exception caught in macro: reuters route process')
        return item


name = 'Set Soccer Keyword'
label = 'Set Soccer Keyword'
callback = set_soccer_keyword_process
access_type = 'backend'
action_type = 'direct'
