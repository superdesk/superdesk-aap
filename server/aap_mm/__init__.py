# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from apps.search_providers import register_search_provider
from superdesk import intrinsic_privilege
from apps.io.search_ingest import SearchIngestService, SearchIngestResource
from .aap_mm_datalayer import AAPMMDatalayer

PROVIDER_NAME = 'aapmm'


def init_app(app):
    aapmm_datalayer = AAPMMDatalayer(app)
    service = SearchIngestService(datasource=None, backend=aapmm_datalayer, source=PROVIDER_NAME)
    SearchIngestResource(endpoint_name=PROVIDER_NAME, service=service, app=app)
    intrinsic_privilege(resource_name=PROVIDER_NAME, method=['GET', 'POST'])


register_search_provider(name=PROVIDER_NAME, fetch_endpoint=PROVIDER_NAME)
