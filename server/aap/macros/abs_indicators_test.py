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
from .abs_indicators import abs_expand
from httmock import urlmatch, HTTMock


class ABSTestCase(AAPTestCase):
    def setUp(self):
        self.setupRemoteSyncMock(self)
        self.app.config['ABS_WEB_SERVICE_URL'] = 'https://api.xxx.yyy.au/ws/data/sdmx-json-indicators/v1/data/'
        self.app.config['ABS_WEB_SERVICE_TOKEN'] = 'super secret token'

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.get_cpi])
        context.mock.__enter__()

    def test_CPI(self):
        item = {'body_html': 'something something {{__CPI/2.50.999901.20.Q__}} {{__CPI/2.50.999901.20.Q#PERIOD__}} '
                             'something else {{(__CPI/2.50.999901.20.Q__|float)*100|int}}',
                'headline': 'Test', 'abstract': 'Test'}
        updated_item = abs_expand(item)
        self.assertEqual(updated_item, {'body_html': 'something something 0.5 Dec-2017 something else 50.0',
                                        'abstract': 'Test', 'headline': 'Test'})

    @urlmatch(scheme='https', netloc='api.xxx.yyy.au',
              path='/ws/data/sdmx-json-indicators/v1/data/CPI/2.50.999901.20.Q/all')
    def get_cpi(self, p1, p2, p3=None):
        data = '{"header":{"id":"555555","test":false,' \
               '"prepared":"2018-02-13T05:49:34.4114953Z","sender":{"id":"XXX","name":"AAAAAAA ' \
               'BBBBBB of SSSSSS"},"links":[{"href":"http://api.xxx.yyy.au/ws/data/sdmx-json-' \
               'indicators/v1/data/CPI/2.50.' \
               '999902.20.Q/all?dimensionAtObservation=allDimensions&detail=DataOnly","rel":"request"}]},"dataSets":' \
               '[{"action":"Information","observations":{"0:0:0:0:0:0":[0.5]}}],"structure":{"links":' \
               '[{"href":"http://api.xxx.yyy.au/ws/data/sdmx-json-indicators/v1/dataflow/CPI/all",' \
               '"rel":"dataflow"}],"name":"Some Index (SI) 17th Series",' \
               '"description":"Some Index (SI) 16th Series","dimensions":{"observation":' \
               '[{"keyPosition":0,"id":"MEASURE","name":"Measure","values":[{"id":"2","name":"Percentage Change ' \
               'from Previous Period"}]},{"keyPosition":1,"id":"REGION","name":"Region","values":[{"id":"50","name' \
               '":"Weighted average of eight capital cities"}]},{"keyPosition":2,"id":"INDEX","name":"Index","valu' \
               'es":[{"id":"999902","name":"Trimmed Mean"}]},{"keyPosition":3,"id":"TSEST","name":"Adjustment Type' \
               '","values":[{"id":"20","name":"Seasonally Adjusted"}]},{"keyPosition":4,"id":"FREQUENCY","name":"F' \
               'requency","values":[{"id":"Q","name":"Quarterly"}],"role":"FREQ"},{"id":"TIME_PERIOD","name":"Time' \
               '","values":[{"id":"2017-Q4","name":"Dec-2017"}],"role":"TIME_PERIOD"}]},"annotations":[{"title":"D' \
               'isclaimer","uri":"http://xxx.yyy.au/Something","text":""}]}}'
        return {'status_code': 200,
                'content': data.encode('utf-8')}
