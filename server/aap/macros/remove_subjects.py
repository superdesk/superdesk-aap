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


def remove_subjects(item, **kwargs):
    try:
        item['subject'] = []
        return item
    except:
        logger.warn('Exception caught in macro: remove_subjects')
        return item


name = 'Remove IPTC subjects from item'
callback = remove_subjects
access_type = 'backend'
action_type = 'direct'
