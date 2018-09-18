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


class FuelMapResource(Resource):
    schema = {
        # The date (only) that the data was retrieved from the Intelematics API
        'sample_date': {
            'type': 'string',
            'required': True
        },
        # The market that the data belongs to Sydney, Melbourne, Brisbane, Adelaide or Perth
        'market': {
            'type': 'string',
            'required': True
        },
        # The fuel type as retrieved from the Intelematics API
        'fuel_type': {
            'type': 'string',
            'required': True
        },
        # The address of the servo as retrurned by the Intelematics API, Only stored for testing and sanity checking
        # It is not to be published.
        'address': {
            'type': 'dict'
        },
        # The geo location of the service station
        'location': {
            'type': 'point'
        },
        # The available price for the fuel of type fuel_type
        'price': {
            'type': 'string'
        }
    }
    mongo_indexes = {'geo_index': [('location', '2dsphere')]}
