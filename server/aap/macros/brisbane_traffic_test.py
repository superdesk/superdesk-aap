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
from .brisbane_traffic import expand_brisbane_traffic
from httmock import urlmatch, HTTMock
import json


class BrisbanePublicTrafficTestCase(AAPTestCase):
    def setUp(self):
        self.setupRemoteSyncMock(self)

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.get_api])
        context.mock.__enter__()

    @urlmatch(scheme='https', netloc='api.qldtraffic.qld.gov.au',
              path='/v1/events')
    def get_api(self, p1, p2, p3=None):
        data = '{ \
          "type": "FeatureCollection", \
          "features": [\
            {\
              "type": "Feature",\
              "geometry": {\
                "type": "GeometryCollection",\
                "geometries": [\
                  {\
                    "type": "Point",\
                    "coordinates": [\
                      153.1764456,\
                      -27.6680651\
                    ]\
                  }\
                ]\
              },\
              "properties": {\
                "id": 185286,\
                "status": "Published",\
                "published": null,\
                "source": {\
                  "source_name": "EPS",\
                  "source_id": null,\
                  "account": null,\
                  "provided_by": "Department of Transport and Main Roads",\
                  "provided_by_url": "https://qldtraffic.qld.gov.au"\
                },\
                "url": "https://api.qldtraffic.qld.gov.au/v1/events/185286",\
                "event_type": "Crash",\
                "event_subtype": "Multi-vehicle",\
                "event_due_to": null,\
                "impact": {\
                  "direction": "Northbound",\
                  "towards": "Brisbane City",\
                  "impact_type": "Lanes affected",\
                  "impact_subtype": "Lane or lanes reduced",\
                  "delay": "Delays expected"\
                },\
                "duration": {\
                  "start": "2019-01-16T06:40:00+10:00",\
                  "end": null,\
                  "active_days": null,\
                  "recurrences": null\
                },\
                "event_priority": "Medium",\
                "description": "before Grandis St",\
                "advice": "Proceed with caution",\
                "information": null,\
                "road_summary": {\
                  "road_name": "Pacific Motorway",\
                  "locality": "Loganholme",\
                  "postcode": "4129",\
                  "local_government_area": "Logan City",\
                  "district": "South Coast"\
                },\
                "last_updated": "2019-01-16T10:39:59.973617+10:00",\
                "next_inspection": null,\
                "web_link": null\
              }\
            }\
          ]}'
        response = json.loads(data)
        data = json.dumps(response)
        return {'status_code': 200,
                'content': data.encode('utf-8')}

    def test_traffic(self):
        item = expand_brisbane_traffic({'body_html': '{{alerts_regional}}'})
        self.assertEqual(item['body_html'], '<p>Crash: Multi-vehicle, Pacific Motorway Loganholme Northbound before '
                                            'Grandis St</p>')
