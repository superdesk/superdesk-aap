# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from settings import INSTALLED_APPS
from app import get_app
from superdesk.tests import TestCase, setup


class AAPTestCase(TestCase):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    def setUpForChildren(self):
        """Run this `setUp` stuff for each children."""
        config = {
            'INSTALLED_APPS': INSTALLED_APPS,
            'ELASTICSEARCH_FORCE_REFRESH': True,
            'DEFAULT_TIMEZONE': 'Australia/Sydney'
        }

        setup(self, config=config, app_factory=get_app)

        self.ctx = self.app.app_context()
        self.ctx.push()

        def clean_ctx():
            if self.ctx:
                self.ctx.pop()

        self.addCleanup(clean_ctx)
