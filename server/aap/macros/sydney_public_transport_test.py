# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from unittests import AAPTestCase
from .sydney_public_transport import expand_sydney_public_transport


class SydneyBusesTestCase(AAPTestCase):
    def setUp(self):
        self.app.config['DEFAULT_TIMEZONE'] = 'Australia/Sydney'

    def test_sydney_public_transport(self):
        item = expand_sydney_public_transport({'body_html': '{{bus_alerts}}'})
        self.assertNotEqual(item.get('body_html'), '{{bus_alerts}}')
