# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.services import BaseService
import superdesk
from .traffic_incidents import IncidentsMapResource


def init_app(app):
    endpoint_name = 'traffic_incidents'
    service = BaseService(endpoint_name, backend=superdesk.get_backend())
    IncidentsMapResource(endpoint_name, app=app, service=service)
