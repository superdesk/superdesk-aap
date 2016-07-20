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
from superdesk.services import BaseService

logger = logging.getLogger(__name__)


class ConsistencyRecordResource(Resource):
    schema = {
        'started_at': {
            'type': 'datetime'
        },
        'completed_at': {
            'type': 'datetime'
        },
        'resource_name': {
            'type': 'string'
        },
        'mongo': {
            'type': 'integer'
        },
        'elastic': {
            'type': 'integer'
        },
        'identical': {
            'type': 'integer'
        },
        'mongo_only': {
            'type': 'integer'
        },
        'mongo_only_ids': {
            'type': 'list',
            'nullable': True
        },
        'elastic_only': {
            'type': 'integer'
        },
        'elastic_only_ids': {
            'type': 'list',
            'nullable': True
        },
        'inconsistent': {
            'type': 'integer'
        },
        'inconsistent_only_ids': {
            'type': 'list',
            'nullable': True
        },
        'differences': {
            'type': 'list',
            'nullable': True
        },
    }
    datasource = {'default_sort': [('_created', -1)]}


class ConsistencyRecordService(BaseService):
    pass
