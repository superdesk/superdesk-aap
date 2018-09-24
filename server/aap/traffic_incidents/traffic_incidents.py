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


class IncidentsMapResource(Resource):
    schema = {
        'guid': {
            'type': 'integer'
        },
        'start_date': {
            'type': 'datetime',
            'required': True
        },
        'end_date': {
            'type': 'datetime',
            'required': True
        },
        'incident_type': {
            'type': 'string'
        },
        'incident_description': {
            'type': 'string'
        },
        'city': {
            'type': 'string'
        },
        'state': {
            'type': 'string'
        },
        'from_street_name': {
            'type': 'string'
        },
        'from_cross_street_name': {
            'type': 'string'
        },
        'to_street_name': {
            'type': 'string'
        },
        'to_cross_street_name': {
            'type': 'string'
        },
        'geometry': {
            'type': 'linestring'
        }
    }
