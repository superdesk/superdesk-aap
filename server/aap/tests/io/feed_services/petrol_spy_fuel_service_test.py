from superdesk.tests import TestCase
from aap.io.feeding_services.pertol_spy_fuel_service import PetrolSpyFuelHTTPFeedingService
from aap.fuel import init_app
from httmock import urlmatch, HTTMock, response

import json


class PetrolSpyFuelHTTPFeedingServiceTestCase(TestCase):
    prices = '{\
    "header": {\
        "apiVersion": "0.1",\
        "requested": 1575941654724,\
        "type": "list",\
        "size": 36\
    },\
    "message": {\
        "expiration": {\
            "DIESEL": {\
                "fresh": 48,\
                "fade": 240,\
                "type": "DIESEL"\
            },\
            "U98": {\
                "fresh": 10,\
                "fade": 20,\
                "type": "U98"\
            },\
            "U95": {\
                "fresh": 10,\
                "fade": 20,\
                "type": "U95"\
            },\
            "LPG": {\
                "fresh": 48,\
                "fade": 240,\
                "type": "LPG"\
            },\
            "E10": {\
                "fresh": 10,\
                "fade": 20,\
                "type": "E10"\
            },\
            "TruckDSL": {\
                "fresh": 48,\
                "fade": 240,\
                "type": "TruckDSL"\
            },\
            "PremDSL": {\
                "fresh": 48,\
                "fade": 240,\
                "type": "PremDSL"\
            },\
            "E85": {\
                "fresh": 10,\
                "fade": 20,\
                "type": "E85"\
            },\
            "U91": {\
                "fresh": 10,\
                "fade": 20,\
                "type": "U91"\
            },\
            "ser": {\
                "fresh": 48,\
                "fade": 240,\
                "type": "BIODIESEL"\
            },\
            "AdBlue": {\
                "fresh": 48,\
                "fade": 240,\
                "type": "AdBlue"\
            }\
        },\
        "list": [\
            {\
                "id": "5629c75a74770a76ef24e2d4",\
                "name": "Speedway Grose Vale",\
                "brand": "SPEEDWAY",\
                "state": "NSW",\
                "suburb": "Grose Vale",\
                "address": "659 Grose Vale Rd Cnr Grose Wold Rd",\
                "postCode": "2753",\
                "country": "AU",\
                "phone": "",\
                "location": {\
                    "x": 150.660708,\
                    "y": -33.582175\
                },\
                "diesel": false,\
                "biodiesel": false,\
                "lpg": false,\
                "e10": false,\
                "u95": false,\
                "u91": false,\
                "u98": false,\
                "eftops": false,\
                "restrooms": false,\
                "accessible": false,\
                "open24": false,\
                "updated": true,\
                "prices": {\
                    "E10": {\
                        "type": "E10",\
                        "updated": 1575940936508,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 131.9\
                    },\
                    "U91": {\
                        "type": "U91",\
                        "updated": 1575940876508,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 133.9\
                    },\
                    "U98": {\
                        "type": "U98",\
                        "updated": 1575941296508,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 156.9\
                    },\
                    "DIESEL": {\
                        "type": "DIESEL",\
                        "updated": 1575941056508,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 143.9\
                    }\
                },\
                "icon": "speedway.png",\
                "brandIcon": "speedway.png",\
                "autoUpdated": false,\
                "e85": false\
            },\
            {\
                "id": "5212b1660364706598e39b40",\
                "name": "Caltex North Richmond",\
                "brand": "CALTEX",\
                "state": "NSW",\
                "suburb": "North Richmond",\
                "address": "50 Bells Line Of Road Cnr Terrace Road",\
                "postCode": "2754",\
                "country": "AU",\
                "phone": "02 4571 1550",\
                "location": {\
                    "x": 150.720102,\
                    "y": -33.579947\
                },\
                "lpg": true,\
                "e10": true,\
                "u98": true,\
                "eftops": true,\
                "open24": true,\
                "updated": true,\
                "prices": {\
                    "U91": {\
                        "type": "U91",\
                        "updated": 1575940636619,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 132.9\
                    },\
                    "U95": {\
                        "type": "U95",\
                        "updated": 1575941176619,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 148.9\
                    },\
                    "U98": {\
                        "type": "U98",\
                        "updated": 1575940816619,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 157.9\
                    },\
                    "LPG": {\
                        "type": "LPG",\
                        "updated": 1575940756619,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 70.9\
                    },\
                    "DIESEL": {\
                        "type": "DIESEL",\
                        "updated": 1575940876619,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 151.9\
                    }\
                },\
                "icon": "caltex.png",\
                "brandIcon": "caltex.png",\
                "autoUpdated": false\
            },\
            {\
                "id": "5213005e03644ac3ec69ac7c",\
                "name": "United North Richmond",\
                "brand": "UNITED",\
                "state": "NSW",\
                "suburb": "North Richmond",\
                "address": "81-87 Bells Line Of Road",\
                "postCode": "2754",\
                "country": "AU",\
                "phone": "(02) 4571 1129",\
                "location": {\
                    "x": 150.71817,\
                    "y": -33.578809\
                },\
                "diesel": true,\
                "lpg": true,\
                "e10": true,\
                "u91": true,\
                "truckpark": true,\
                "restrooms": true,\
                "open24": false,\
                "updated": true,\
                "prices": {\
                    "E10": {\
                        "type": "E10",\
                        "updated": 1575940636141,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 129.7\
                    },\
                    "U91": {\
                        "type": "U91",\
                        "updated": 1575941116141,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 131.7\
                    },\
                    "U95": {\
                        "type": "U95",\
                        "updated": 1575940996141,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 143.7\
                    },\
                    "U98": {\
                        "type": "U98",\
                        "updated": 1575940936141,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 151.7\
                    },\
                    "DIESEL": {\
                        "type": "DIESEL",\
                        "updated": 1575940876141,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 144.5\
                    },\
                    "LPG": {\
                        "type": "LPG",\
                        "updated": 1575941236141,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 69.7\
                    }\
                },\
                "icon": "united.png",\
                "brandIcon": "united.png",\
                "autoUpdated": false\
            },\
            {\
                "id": "59dd8f8ab99142726c4dd289",\
                "name": "Coles Express North Richmond",\
                "brand": "SHELL",\
                "state": "NSW",\
                "suburb": "North Richmond",\
                "address": "72-78 Bells Line of Rd",\
                "postCode": "2754",\
                "country": "AU",\
                "phone": "(02) 4571 4009",\
                "location": {\
                    "x": 150.718194,\
                    "y": -33.578025\
                },\
                "prices": {\
                    "E10": {\
                        "type": "E10",\
                        "updated": 1575940516184,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 129.9\
                    },\
                    "U91": {\
                        "type": "U91",\
                        "updated": 1575940936184,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 131.9\
                    },\
                    "U98": {\
                        "type": "U98",\
                        "updated": 1575940756184,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 153.9\
                    },\
                    "DIESEL": {\
                        "type": "DIESEL",\
                        "updated": 1575940696184,\
                        "relevant": true,\
                        "reportedBy": "",\
                        "amount": 147.9\
                    }\
                },\
                "icon": "coles.png",\
                "brandIcon": "coles.png",\
                "autoUpdated": false\
            }\
        ]\
    }\
}'

    provider = {
        "_id": 1,
        "name": "Petrol Spy Fuel",
        "config": {
            "api_url": "http://a.b.c/box",
            "market_definitions": "[{'market':'Sydney','neLat':34.2799,'neLng':151.4273,'swLat':-34.2799,"
                                  "'swLng':150.6226,'deltaLat':0.1736}]"
        },
        "content_types": [],
        "feeding_service": "petrol_spy_api_feed",
        "source": "Petrol Spy"
    }

    def setUp(self):
        init_app(self.app)
        self.setupRemoteSyncMock(self)
        self.app.data.insert('ingest_providers', [self.provider])

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.get_prices])
        context.mock.__enter__()

    @urlmatch(scheme='http', netloc='a.b.c', path='/box')
    def get_prices(self, url, request):
        headers = {'total': '900'}
        resp_bytes = self.prices
        return response(status_code=200, headers=headers, content=resp_bytes)

    def test_save(self):
        it = PetrolSpyFuelHTTPFeedingService()
        it._save(json.loads(self.prices).get('message').get('list'), {'market': 'Sydney', 'neLat': -33.4119,
                                                                      'neLng': 151.4273, 'swLat': -34.2799,
                                                                      'swLng': 150.6226, 'deltaLat': 0.1736})
        prices = self.app.data.find('fuel', None, None)
        self.assertEqual(prices.count(), 19)

    def test_get_prices(self):
        it = PetrolSpyFuelHTTPFeedingService()
        prices = it._get_prices(self.provider,
                                {'market': 'Sydney', 'neLat': -34.2799, 'neLng': 151.4273, 'swLat': -34.2799,
                                 'swLng': 150.6226, 'deltaLat': 0.1736})
        self.assertEqual(len(prices), 4)

    def test_update(self):
        it = PetrolSpyFuelHTTPFeedingService()
        it._update(self.provider, {})
