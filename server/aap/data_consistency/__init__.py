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
from .legal_archive_consistency import LegalArchiveConsistencyResource
from aap.data_consistency.consistency_record import ConsistencyRecordResource, \
    ConsistencyRecordService
from aap.data_consistency.compare_repositories import CompareRepositories  # noqa
from superdesk import get_backend
from superdesk.services import BaseService

logger = logging.getLogger(__name__)


def init_app(app):
    endpoint_name = 'legal_archive_consistency'
    service = BaseService(endpoint_name, backend=get_backend())
    LegalArchiveConsistencyResource(endpoint_name, app=app, service=service)

    endpoint_name = 'consistency'
    service = ConsistencyRecordService(endpoint_name, backend=get_backend())
    ConsistencyRecordResource(endpoint_name, app=app, service=service)


# must be imported for registration
import aap.data_consistency.compare_repositories  # NOQA
import aap.data_consistency.consistency_record  # NOQA
