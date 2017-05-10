
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
import superdesk
from flask import current_app as app


logger = logging.getLogger(__name__)


class ApplyElasticSearchMappings(superdesk.Command):

    def run(self, ):
        logger.info('Starting to apply elasticsearch mappings.')
        try:
            app.data.elastic.put_mapping(app=app)
            logger.info('Mappings applied.')
        except:
            logger.exception('Failed to apply mappings...')
            return 1


superdesk.command('app:apply_elasticsearch_mappings', ApplyElasticSearchMappings())
