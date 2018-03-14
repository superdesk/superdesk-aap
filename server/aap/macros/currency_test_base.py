# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.tests import TestCase
from httmock import urlmatch, HTTMock
import json
from superdesk.cache import cache


class CurrencyTestClass(TestCase):
    resp = {'success': True,
            'rates': {"EUR": 1.0, "AUD": 2.0, "USD": 1.0, "NZD": 4.0, "CHF": 1.0, "CNY": 1.0, "GBP": 1.0,
                      "JPY": 1.0}}

    def setUp(self):
        self.setupRemoteSyncMock(self)

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.rate_request])
        context.mock.__enter__()

    @urlmatch(scheme='http', netloc='data.fixer.io', path='/api/latest')
    def rate_request(self, url, request):
        resp_bytes = json.dumps(self.resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }

    def clearCache(self):
        cache.clean()
