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
from .melbourne_public_transport import expand_melbourne_public_transport
from httmock import urlmatch, HTTMock
import json
from superdesk.utc import utcnow


class MelbournePublicTransportTestCase(AAPTestCase):
    def setUp(self):
        self.setupRemoteSyncMock(self)

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.get_api])
        context.mock.__enter__()

    @urlmatch(scheme='http', netloc='timetableapi.ptv.vic.gov.au',
              path='/v3/disruptions')
    def get_api(self, p1, p2, p3=None):
        data = '{ "disruptions": { \
        "metro_train": [ \
            { \
                "disruption_id": 160308, \
                "title": "The 9.08am Flinders Street Station to Blackburn Station ' \
               'will terminate at Box Hill Station today.",\
                "url": "http://ptv.vic.gov.au/live-travel-updates/",\
                "description": "The 9.08am Flinders Street Station to Blackburn Station will ' \
               'terminate at Box Hill Station today.",\
                "disruption_status": "Current",\
                "disruption_type": "Minor Delays",\
                "published_on": "2019-01-07T22:45:01Z",\
                "last_updated": "2019-01-07T22:45:06Z",\
                "from_date": "2019-01-07T22:43:00Z",\
                "to_date": null,\
                "routes": [\
                    {\
                        "route_type": 0,\
                        "route_id": 2,\
                        "route_name": "Belgrave",\
                        "route_number": "",\
                        "route_gtfs_id": "2-BEL",\
                        "direction": {\
                            "route_direction_id": 35,\
                            "direction_id": 3,\
                            "direction_name": "Belgrave",\
                            "service_time": null\
                        }\
                    },\
                    {\
                        "route_type": 0,\
                        "route_id": 9,\
                        "route_name": "Lilydale",\
                        "route_number": "",\
                        "route_gtfs_id": "2-LIL",\
                        "direction": {\
                            "route_direction_id": 1,\
                            "direction_id": 8,\
                            "direction_name": "Lilydale",\
                            "service_time": null\
                        }\
                    }\
                ],\
                "stops": [],\
                "colour": "#ee9b00",\
                "display_on_board": true,\
                "display_status": true\
            }\
        ],\
        "metro_tram": [\
            {\
                "disruption_id": 159908,\
                "title": "Buses replace Route 75 trams between Stop 48 Orrong Crescent and Vermont South from first' \
               ' tram Thursday 3 January to 5am Saturday 12 January 2019, due to track renewal works on Toorak Road ' \
               'between Warrigal Road and Camberwell Road.",\
                "url": "http://ptv.vic.gov.au/live-travel-updates/",\
                "description": "Buses replace Route 75 trams between Stop 48 Orrong Crescent and Vermont South from ' \
               'first tram Thursday 3 January to 5am Saturday 12 January 2019, due to track renewal works on Toorak' \
               ' Road between Warrigal Road and Camberwell Road.",\
                "disruption_status": "Current",\
                "disruption_type": "Service Information",\
                "published_on": "2019-01-02T03:23:56Z",\
                "last_updated": "2019-01-02T22:46:06Z",\
                "from_date": "2019-01-02T16:00:00Z",\
                "to_date": "2019-01-11T18:00:00Z",\
                "routes": [\
                    {\
                        "route_type": 1,\
                        "route_id": 958,\
                        "route_name": "Etihad Stadium Docklands - Vermont South",\
                        "route_number": "75",\
                        "route_gtfs_id": "3-075",\
                        "direction": null\
                    }\
                ],\
                "stops": [],\
                "colour": "#ffd500",\
                "display_on_board": true,\
                "display_status": false\
            }\
        ],\
        "metro_bus": [\
            {\
                "disruption_id": 160253,\
                "title": "Due to a police incident outside Taylors Lakes Secondary College, Route 419 buses will ' \
               'be diverting along Chichester Drive and missing bus stops on Parmelia Drive until further notice.",\
                "url": "http://ptv.vic.gov.au/live-travel-updates/",\
                "description": "Due to a police incident outside Taylors Lakes Secondary College, Route 419 buses ' \
               'will be diverting along Chichester Drive and missing bus stops on Parmelia Drive until ' \
               'further notice.",\
                "disruption_status": "Current",\
                "disruption_type": "Diversion",\
                "published_on": "2019-01-07T03:19:51Z",\
                "last_updated": "2019-01-07T04:26:51Z",\
                "from_date": "2019-01-07T02:57:00Z",\
                "to_date": null,\
                "routes": [\
                    {\
                        "route_type": 2,\
                        "route_id": 11513,\
                        "route_name": "St Albans Station - Watergardens Station via Keilor Downs",\
                        "route_number": "419",\
                        "route_gtfs_id": "4-419",\
                        "direction": null\
                    }\
                ],\
                "stops": [],\
                "colour": "#ffd500",\
                "display_on_board": true,\
                "display_status": true\
            }\
        ]\
    },\
    "status": {\
        "version": "3.0",\
        "health": 1\
    }}'
        response = json.loads(data)
        response['disruptions']['metro_train'][0]['from_date'] = utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data = json.dumps(response)
        return {'status_code': 200,
                'content': data.encode('utf-8')}

    def test_pt(self):
        item = expand_melbourne_public_transport({'body_html': '{{train_alerts}}'})
        self.assertEqual(item['body_html'], '<p>The 9.08am Flinders Street Station to Blackburn Station will terminate'
                                            ' at Box Hill Station today.</p>')
