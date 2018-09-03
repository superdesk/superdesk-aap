# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2016 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import superdesk
from .mission_report import MissionReportResource, MissionReportService


def init_app(app):
    endpoint_name = 'mission_report'
    service = MissionReportService(endpoint_name, backend=superdesk.get_backend())
    MissionReportResource(endpoint_name, app=app, service=service)

    superdesk.privilege(
        name='mission_report',
        label='Mission Report View',
        description='User can view mission reports.'
    )
