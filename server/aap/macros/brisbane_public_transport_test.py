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
from .brisbane_public_transport import expand_brisbane_transport


class SydneyBusesTestCase(AAPTestCase):

    def test_brisbane_public_transport(self):
        item = expand_brisbane_transport({'body_html': '{{bus_alerts}}'})
        self.assertNotEqual(item.get('body_html'), '{{bus_alerts}}')
