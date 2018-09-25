from superdesk.tests import TestCase
from aap.io.feeding_services.intelematics_incidents_service import IntelematicsIncidentHTTPFeedingService
from aap.traffic_incidents import init_app
from httmock import urlmatch, HTTMock, response

import json


class IntelematicsIncidentHTTPFeedingServiceTestCase(TestCase):
    resp = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "EPSG:4326"
            }
        },
        "features": [
            {
                "type": "Feature",
                "crs": {
                    "type": "name",
                    "properties": {
                        "name": "EPSG:4326"
                    }
                },
                "properties": {
                    "id": 394632,
                    "startDate": 1534406640017,
                    "endDate": 1543561380017,
                    "type": "One lane closed",
                    "description": "One lane closed due to Roadworks on Wakehurst Parkway Northbound in Oxford Falls "
                                   "between Dreadnought Road and Warringa Aquatic Centre.",
                    "city": "Oxford Falls",
                    "state": "NSW",
                    "fromStreetName": "Wakehurst Parkway",
                    "fromCrossStreetName": "Dreadnought Road",
                    "toStreetName": "Wakehurst Parkway",
                    "toCrossStreetName": "Warringa Aquatic Centre"
                },
                "geometry": {
                    "type": "LineString",
                    "crs": {
                        "type": "name",
                        "properties": {
                            "name": "EPSG:4326"
                        }
                    },
                    "coordinates": [
                        [
                            151.24453,
                            -33.73945
                        ],
                        [
                            151.24444,
                            -33.73967
                        ]
                    ]
                },
                "id": "394632"
            }]
    }

    provider = {
        "_id": 1,
        "name": "Intelematics Fuel",
        "config": {
            "api_url": "http://a.b.c/incidents/rest/all.geojson",
        },
        "content_types": [],
        "feeding_service": "intelematics_incident_api_feed",
        "source": "Intelematics"
    }

    def setUp(self):
        init_app(self.app)
        self.setupRemoteSyncMock(self)
        self.app.data.insert('ingest_providers', [self.provider])

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.get_incidents])
        context.mock.__enter__()

    @urlmatch(scheme='http', netloc='a.b.c', path='/incidents/rest/all.geojson')
    def get_incidents(self, user, pwd):
        resp_bytes = json.dumps(self.resp)
        return response(status_code=200, content=resp_bytes)

    def test_update(self):
        it = IntelematicsIncidentHTTPFeedingService()
        it._update(self.provider, {})
        it._update(self.provider, {})
