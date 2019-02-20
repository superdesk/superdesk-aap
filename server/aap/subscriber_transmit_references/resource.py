
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
from superdesk.resource import Resource


logger = logging.getLogger(__name__)


class SubscriberTransmitReferenceResource(Resource):
    schema = {
        # superdesk id of the item
        'item_id': {
            'type': 'string'
        },
        'subscriber_id': Resource.rel('subscribers'),
        # reference_id points to the unique id in the subscriber system
        'reference_id': {
            'type': 'string'
        },
        'extra': {'type': 'dict'}
    }
    internal_resource = True
    mongo_indexes = {
        'item_id_1': [('item_id', 1)],
        'subscriber_id_1': [('subscriber_id', 1)],
        'reference_id_1': [('reference_id', 1)]
    }
    item_methods = []
    resource_methods = []
