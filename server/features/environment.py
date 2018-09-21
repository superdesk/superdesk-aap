# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


from superdesk.tests.environment import before_feature, before_step, after_scenario, before_all  # noqa
from superdesk.tests.environment import setup_before_scenario
from app import get_app
from settings import INSTALLED_APPS, MACROS_MODULE


def before_scenario(context, scenario):
    config = {
        'INSTALLED_APPS': INSTALLED_APPS,
        'ELASTICSEARCH_FORCE_REFRESH': True,
        'MACROS_MODULE': MACROS_MODULE
    }
    setup_before_scenario(context, scenario, config, app_factory=get_app)
