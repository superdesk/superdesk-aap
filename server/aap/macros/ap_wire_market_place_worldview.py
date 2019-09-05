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
from superdesk import get_resource_service
from bson import ObjectId
from flask import current_app as app
from superdesk.utils import config
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE

logger = logging.getLogger(__name__)


def ap_wire_aapx_worldview_route(item, **kwargs):
    """
    This macro will look for a configured list of subscribers and set the target subscribers in the item to that list.
    It will also set the keywords for marketplace and worldview. If the macro is not being run interactively it will
    publish the item.
    :param item:
    :param kwargs:
    :return:
    """
    # Using the system configured subscriber list set the targeted publish list for the item
    service = get_resource_service('subscribers')
    subscribers = service.get_from_mongo(req=None, lookup={
        '_id': {'$in': [ObjectId(s) for s in app.config.get('WORLDVIEW_TARGET_SUBSCRIBERS').split(',')]}})
    if subscribers.count() > 0:
        item['target_subscribers'] = [{'_id': str(s.get('_id')), 'name': s.get('name')} for s in subscribers]
    else:
        logger.warn('No AAPX worldview subscribers found')

    try:
        if not item.get('keywords'):
            item['keywords'] = []

        # add marketplace keyword
        if 'marketplace' not in item.get('keywords', []):
            item['keywords'].append('marketplace')
        # add the worldview keyword if not already present
        if 'worldview' not in item.get('keywords', []):
            item['keywords'].append('worldview')

        # If a desk and stage in the kwargs then it's being run as a stage macro, so publish it as well.
        if 'desk' in kwargs and 'stage' in kwargs:
            update = {'keywords': item.get('keywords')}
            if item.get('target_subscribers'):
                update['target_subscribers'] = item['target_subscribers']
            get_resource_service('archive').system_update(item[config.ID_FIELD], update, item)

            get_resource_service('archive_publish').patch(id=item[config.ID_FIELD],
                                                          updates={ITEM_STATE: CONTENT_STATE.PUBLISHED,
                                                                   'auto_publish': True})
            return get_resource_service('archive').find_one(req=None, _id=item[config.ID_FIELD])

        return item
    except:
        logger.warning('Exception caught in macro: market_place_worldview_route_process')
        return item


name = 'AP wire AAPX Worldview'
label = 'AP wire AAPX Worldview'
callback = ap_wire_aapx_worldview_route
access_type = 'frontend'
action_type = 'direct'
