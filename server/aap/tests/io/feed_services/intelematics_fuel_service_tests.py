from superdesk.tests import TestCase
from aap.io.feeding_services.intelematics_fuel_service import IntelematicsFuelHTTPFeedingService
from aap.fuel import init_app
from httmock import urlmatch, HTTMock, response

import json


class IntelematicsFuelHTTPFeedingServiceTestCase(TestCase):
    prices = [{
        'fuelPrice': [{
            'price': 146.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'E10',
            'displayName': 'E10 or Ethanol-94',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 174.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-98',
            'displayName': 'P98 or 98-RON',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 154.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PDSL',
            'displayName': 'Premium Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 77.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'LPG',
            'displayName': 'LPG',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 149.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'ULP',
            'displayName': 'Unleaded 91',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 149.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'DSL',
            'displayName': 'Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': None,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-95',
            'displayName': 'Premium 95',
            'priceRestricted': False,
            'lastUpdated': '2017-11-29T06:15:00.000Z'
        }],
        'fuelStation': {
            'pricesAvailable': True,
            'location': {
                'lat': -34.927586,
                'lon': 149.90945
            },
            'address': {
                'country': 'AUS',
                'street': '69 Sesame Rd',
                'suburb': 'Liverpool',
                'state': 'NSW'
            },
            'hours': [],
            'locationOffsetMeters': 17288,
            'name': 'The Servo',
            'attributes': [{
                'key': 'source',
                'value': 'MM'
            }],
            'brand': 'BP',
            'fuelTypes': [{
                'pricesAvailable': True,
                'description': 'E10 or Ethanol-94',
                'value': 'E10'
            }, {
                'pricesAvailable': True,
                'description': 'P98 or 98-RON',
                'value': 'PULP-98'
            }, {
                'pricesAvailable': True,
                'description': 'Premium Diesel',
                'value': 'PDSL'
            }, {
                'pricesAvailable': True,
                'description': 'LPG',
                'value': 'LPG'
            }, {
                'pricesAvailable': True,
                'description': 'Unleaded 91',
                'value': 'ULP'
            }, {
                'pricesAvailable': True,
                'description': 'Diesel',
                'value': 'DSL'
            }, {
                'pricesAvailable': False,
                'description': 'Premium 95',
                'value': 'PULP-95'
            }],
            'icon': [{
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/a.png',
                'type': 'mapicon',
                'iconScale': None
            }, {
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/b.png',
                'type': 'icon',
                'iconScale': None
            }],
            'id': 1
        }
    }, {
        'fuelPrice': [{
            'price': 145.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'ULP',
            'displayName': 'Unleaded 91',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': 162.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-98',
            'displayName': 'P98 or 98-RON',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': 155.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-95',
            'displayName': 'Premium 95',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': 79.7,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'LPG',
            'displayName': 'LPG',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': 142.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'E10',
            'displayName': 'E10 or Ethanol-94',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': 147.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'DSL',
            'displayName': 'Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }],
        'fuelStation': {
            'pricesAvailable': True,
            'location': {
                'lat': -36.897007,
                'lon': 156.14903
            },
            'address': {
                'country': 'AUS',
                'street': '208 Sesame Rd',
                'suburb': 'Petersham',
                'state': 'NSW'
            },
            'hours': [],
            'locationOffsetMeters': 7341,
            'name': 'The Servo',
            'attributes': [{
                'key': 'source',
                'value': 'MM'
            }],
            'brand': 'Budget',
            'fuelTypes': [{
                'pricesAvailable': True,
                'description': 'Unleaded 91',
                'value': 'ULP'
            }, {
                'pricesAvailable': True,
                'description': 'P98 or 98-RON',
                'value': 'PULP-98'
            }, {
                'pricesAvailable': True,
                'description': 'Premium 95',
                'value': 'PULP-95'
            }, {
                'pricesAvailable': True,
                'description': 'LPG',
                'value': 'LPG'
            }, {
                'pricesAvailable': True,
                'description': 'E10 or Ethanol-94',
                'value': 'E10'
            }, {
                'pricesAvailable': True,
                'description': 'Diesel',
                'value': 'DSL'
            }],
            'icon': [{
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/c.png',
                'type': 'mapicon',
                'iconScale': None
            }, {
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/d.png',
                'type': 'icon',
                'iconScale': None
            }],
            'id': 2
        }
    }, {
        'fuelPrice': [{
            'price': 170.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-98',
            'displayName': 'P98 or 98-RON',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 149.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'ULP',
            'displayName': 'Unleaded 91',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 79.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'LPG',
            'displayName': 'LPG',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 156.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PDSL',
            'displayName': 'Premium Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': None,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'DSL',
            'displayName': 'Diesel',
            'priceRestricted': False,
            'lastUpdated': '2016-11-16T05:47:00.000Z'
        }],
        'fuelStation': {
            'pricesAvailable': True,
            'location': {
                'lat': -37.767235,
                'lon': 157.95213
            },
            'address': {
                'country': 'AUS',
                'street': 'Sesame Road',
                'suburb': 'Seven Hills',
                'state': 'NSW'
            },
            'hours': [],
            'locationOffsetMeters': 16018,
            'name': 'The Servo',
            'attributes': [{
                'key': 'source',
                'value': 'MM'
            }],
            'brand': 'BP',
            'fuelTypes': [{
                'pricesAvailable': True,
                'description': 'P98 or 98-RON',
                'value': 'PULP-98'
            }, {
                'pricesAvailable': True,
                'description': 'Unleaded 91',
                'value': 'ULP'
            }, {
                'pricesAvailable': True,
                'description': 'LPG',
                'value': 'LPG'
            }, {
                'pricesAvailable': True,
                'description': 'Premium Diesel',
                'value': 'PDSL'
            }, {
                'pricesAvailable': False,
                'description': 'Diesel',
                'value': 'DSL'
            }],
            'icon': [{
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/e.png',
                'type': 'mapicon',
                'iconScale': None
            }, {
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/f.png',
                'type': 'icon',
                'iconScale': None
            }],
            'id': 3
        }
    }, {
        'fuelPrice': [{
            'price': 174.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-98',
            'displayName': 'P98 or 98-RON',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 153.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'ULP',
            'displayName': 'Unleaded 91',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 159.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PDSL',
            'displayName': 'Premium Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 165.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-95',
            'displayName': 'Premium 95',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 79.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'LPG',
            'displayName': 'LPG',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }],
        'fuelStation': {
            'pricesAvailable': True,
            'location': {
                'lat': -31.73094,
                'lon': 153.08061
            },
            'address': {
                'country': 'AUS',
                'street': 'Sesame Road',
                'suburb': 'Thornleigh',
                'state': 'NSW'
            },
            'hours': [],
            'locationOffsetMeters': 14823,
            'name': 'The Servo',
            'attributes': [{
                'key': 'source',
                'value': 'MM'
            }],
            'brand': 'BP',
            'fuelTypes': [{
                'pricesAvailable': True,
                'description': 'P98 or 98-RON',
                'value': 'PULP-98'
            }, {
                'pricesAvailable': True,
                'description': 'Unleaded 91',
                'value': 'ULP'
            }, {
                'pricesAvailable': True,
                'description': 'Premium Diesel',
                'value': 'PDSL'
            }, {
                'pricesAvailable': True,
                'description': 'Premium 95',
                'value': 'PULP-95'
            }, {
                'pricesAvailable': True,
                'description': 'LPG',
                'value': 'LPG'
            }],
            'icon': [{
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/g.png',
                'type': 'mapicon',
                'iconScale': None
            }, {
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/h.png',
                'type': 'icon',
                'iconScale': None
            }],
            'id': 4
        }
    }, {
        'fuelPrice': [{
            'price': 156.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PDSL',
            'displayName': 'Premium Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T17:55:45.000Z'
        }, {
            'price': 79.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'LPG',
            'displayName': 'LPG',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T17:55:45.000Z'
        }, {
            'price': None,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-98',
            'displayName': 'P98 or 98-RON',
            'priceRestricted': False,
            'lastUpdated': '2018-09-05T18:36:29.000Z'
        }, {
            'price': 154.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'DSL',
            'displayName': 'Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T17:55:45.000Z'
        }, {
            'price': None,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'E10',
            'displayName': 'E10 or Ethanol-94',
            'priceRestricted': False,
            'lastUpdated': '2018-09-05T18:36:29.000Z'
        }, {
            'price': None,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-95',
            'displayName': 'Premium 95',
            'priceRestricted': False,
            'lastUpdated': '2018-09-05T18:36:29.000Z'
        }],
        'fuelStation': {
            'pricesAvailable': True,
            'location': {
                'lat': -29.819412,
                'lon': 155.98932
            },
            'address': {
                'country': 'AUS',
                'street': '149 Sesame Hwy ',
                'suburb': 'Mays Hill',
                'state': 'NSW'
            },
            'hours': [],
            'locationOffsetMeters': 9765,
            'name': 'The Servo',
            'attributes': [{
                'key': 'source',
                'value': 'FC'
            }],
            'brand': 'BP',
            'fuelTypes': [{
                'pricesAvailable': True,
                'description': 'Premium Diesel',
                'value': 'PDSL'
            }, {
                'pricesAvailable': True,
                'description': 'LPG',
                'value': 'LPG'
            }, {
                'pricesAvailable': False,
                'description': 'P98 or 98-RON',
                'value': 'PULP-98'
            }, {
                'pricesAvailable': True,
                'description': 'Diesel',
                'value': 'DSL'
            }, {
                'pricesAvailable': False,
                'description': 'E10 or Ethanol-94',
                'value': 'E10'
            }, {
                'pricesAvailable': False,
                'description': 'Premium 95',
                'value': 'PULP-95'
            }],
            'icon': [{
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/i@1x.png',
                'type': 'mapicon',
                'iconScale': None
            }, {
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/j.png',
                'type': 'icon',
                'iconScale': None
            }],
            'id': 5
        }
    }, {
        'fuelPrice': [{
            'price': 171.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-98',
            'displayName': 'P98 or 98-RON',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 157.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PDSL',
            'displayName': 'Premium Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 162.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-95',
            'displayName': 'Premium 95',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 148.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'E10',
            'displayName': 'E10 or Ethanol-94',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': 79.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'LPG',
            'displayName': 'LPG',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:27:00.000Z'
        }, {
            'price': None,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'DSL',
            'displayName': 'Diesel',
            'priceRestricted': False,
            'lastUpdated': '2016-11-16T01:32:00.000Z'
        }],
        'fuelStation': {
            'pricesAvailable': True,
            'location': {
                'lat': -34.81948,
                'lon': 154.02126
            },
            'address': {
                'country': 'AUS',
                'street': 'Sesame Street',
                'suburb': 'Rosehill',
                'state': 'NSW'
            },
            'hours': [],
            'locationOffsetMeters': 7374,
            'name': 'The Servo',
            'attributes': [{
                'key': 'source',
                'value': 'MM'
            }],
            'brand': 'BP',
            'fuelTypes': [{
                'pricesAvailable': True,
                'description': 'P98 or 98-RON',
                'value': 'PULP-98'
            }, {
                'pricesAvailable': True,
                'description': 'Premium Diesel',
                'value': 'PDSL'
            }, {
                'pricesAvailable': True,
                'description': 'Premium 95',
                'value': 'PULP-95'
            }, {
                'pricesAvailable': True,
                'description': 'E10 or Ethanol-94',
                'value': 'E10'
            }, {
                'pricesAvailable': True,
                'description': 'LPG',
                'value': 'LPG'
            }, {
                'pricesAvailable': False,
                'description': 'Diesel',
                'value': 'DSL'
            }],
            'icon': [{
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/k@1x.png',
                'type': 'mapicon',
                'iconScale': None
            }, {
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/l.png',
                'type': 'icon',
                'iconScale': None
            }],
            'id': 6
        }
    }, {
        'fuelPrice': [{
            'price': 136.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'ULP',
            'displayName': 'Unleaded 91',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': 152.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-98',
            'displayName': 'P98 or 98-RON',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': 79.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'LPG',
            'displayName': 'LPG',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': 133.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'E10',
            'displayName': 'E10 or Ethanol-94',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': 142.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'DSL',
            'displayName': 'Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }],
        'fuelStation': {
            'pricesAvailable': True,
            'location': {
                'lat': -31.852505,
                'lon': 151.9348
            },
            'address': {
                'country': 'AUS',
                'street': "729 Sesame St",
                'suburb': 'Smithfield',
                'state': 'NSW'
            },
            'hours': [],
            'locationOffsetMeters': 13503,
            'name': 'The Servo',
            'attributes': [{
                'key': 'source',
                'value': 'MM'
            }],
            'brand': 'Budget',
            'fuelTypes': [{
                'pricesAvailable': True,
                'description': 'Unleaded 91',
                'value': 'ULP'
            }, {
                'pricesAvailable': True,
                'description': 'P98 or 98-RON',
                'value': 'PULP-98'
            }, {
                'pricesAvailable': True,
                'description': 'LPG',
                'value': 'LPG'
            }, {
                'pricesAvailable': True,
                'description': 'E10 or Ethanol-94',
                'value': 'E10'
            }, {
                'pricesAvailable': True,
                'description': 'Diesel',
                'value': 'DSL'
            }],
            'icon': [{
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/m.png',
                'type': 'mapicon',
                'iconScale': None
            }, {
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/n.png',
                'type': 'icon',
                'iconScale': None
            }],
            'id': 7
        }
    }, {
        'fuelPrice': [{
            'price': 153.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'ULP',
            'displayName': 'Unleaded 91',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }, {
            'price': 172.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-98',
            'displayName': 'P98 or 98-RON',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }, {
            'price': 165.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-95',
            'displayName': 'Premium 95',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }, {
            'price': 163.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PDSL',
            'displayName': 'Premium Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }, {
            'price': 79.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'LPG',
            'displayName': 'LPG',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }, {
            'price': 151.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'E10',
            'displayName': 'E10 or Ethanol-94',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }],
        'fuelStation': {
            'pricesAvailable': True,
            'location': {
                'lat': -34.726665,
                'lon': 158.08363
            },
            'address': {
                'country': 'AUS',
                'street': '200-202 Sesame',
                'suburb': 'Thornleigh',
                'state': 'NSW'
            },
            'hours': [],
            'locationOffsetMeters': 15303,
            'name': 'The Servo',
            'attributes': [{
                'key': 'source',
                'value': 'MM'
            }],
            'brand': 'Caltex',
            'fuelTypes': [{
                'pricesAvailable': True,
                'description': 'Unleaded 91',
                'value': 'ULP'
            }, {
                'pricesAvailable': True,
                'description': 'P98 or 98-RON',
                'value': 'PULP-98'
            }, {
                'pricesAvailable': True,
                'description': 'Premium 95',
                'value': 'PULP-95'
            }, {
                'pricesAvailable': True,
                'description': 'Premium Diesel',
                'value': 'PDSL'
            }, {
                'pricesAvailable': True,
                'description': 'LPG',
                'value': 'LPG'
            }, {
                'pricesAvailable': True,
                'description': 'E10 or Ethanol-94',
                'value': 'E10'
            }],
            'icon': [{
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/o.png',
                'type': 'mapicon',
                'iconScale': None
            }, {
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/p.png',
                'type': 'icon',
                'iconScale': None
            }],
            'id': 8
        }
    }, {
        'fuelPrice': [{
            'price': 155.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'ULP',
            'displayName': 'Unleaded 91',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }, {
            'price': 174.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-98',
            'displayName': 'P98 or 98-RON',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }, {
            'price': 167.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-95',
            'displayName': 'Premium 95',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }, {
            'price': 163.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PDSL',
            'displayName': 'Premium Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }, {
            'price': 79.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'LPG',
            'displayName': 'LPG',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }, {
            'price': 153.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'E10',
            'displayName': 'E10 or Ethanol-94',
            'priceRestricted': False,
            'lastUpdated': '2018-09-11T05:03:00.000Z'
        }],
        'fuelStation': {
            'pricesAvailable': True,
            'location': {
                'lat': -39.906593,
                'lon': 133.23203
            },
            'address': {
                'country': 'AUS',
                'street': '2 Sesame Rd',
                'suburb': 'Randwick',
                'state': 'NSW'
            },
            'hours': [],
            'locationOffsetMeters': 14806,
            'name': 'The Servo',
            'attributes': [{
                'key': 'source',
                'value': 'MM'
            }],
            'brand': 'Caltex',
            'fuelTypes': [{
                'pricesAvailable': True,
                'description': 'Unleaded 91',
                'value': 'ULP'
            }, {
                'pricesAvailable': True,
                'description': 'P98 or 98-RON',
                'value': 'PULP-98'
            }, {
                'pricesAvailable': True,
                'description': 'Premium 95',
                'value': 'PULP-95'
            }, {
                'pricesAvailable': True,
                'description': 'Premium Diesel',
                'value': 'PDSL'
            }, {
                'pricesAvailable': True,
                'description': 'LPG',
                'value': 'LPG'
            }, {
                'pricesAvailable': True,
                'description': 'E10 or Ethanol-94',
                'value': 'E10'
            }],
            'icon': [{
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/q.png',
                'type': 'mapicon',
                'iconScale': None
            }, {
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/r.png',
                'type': 'icon',
                'iconScale': None
            }],
            'id': 9
        }
    }, {
        'fuelPrice': [{
            'price': 163.3,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PULP-95',
            'displayName': 'Premium 95',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T21:40:00.000Z'
        }, {
            'price': 148.5,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'PDSL',
            'displayName': 'Premium Diesel',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }, {
            'price': 148.5,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'E10',
            'displayName': 'E10 or Ethanol-94',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T21:40:00.000Z'
        }, {
            'price': 79.9,
            'priceUnit': {
                'priceResolution': -2,
                'deliveryUnit': 'LITR',
                'currency': 'AUD'
            },
            'priceUnits': None,
            'fuelType': 'LPG',
            'displayName': 'LPG',
            'priceRestricted': False,
            'lastUpdated': '2018-09-10T14:10:00.000Z'
        }],
        'fuelStation': {
            'pricesAvailable': True,
            'location': {
                'lat': -38.90446,
                'lon': 154.16795
            },
            'address': {
                'country': 'AUS',
                'street': '379 Sesame Rd',
                'suburb': 'Marrickville',
                'state': 'NSW'
            },
            'hours': [],
            'locationOffsetMeters': 9271,
            'name': 'The Servo',
            'attributes': [{
                'key': 'source',
                'value': 'MM'
            }],
            'brand': 'Metro Fuel',
            'fuelTypes': [{
                'pricesAvailable': True,
                'description': 'Premium 95',
                'value': 'PULP-95'
            }, {
                'pricesAvailable': True,
                'description': 'Premium Diesel',
                'value': 'PDSL'
            }, {
                'pricesAvailable': True,
                'description': 'E10 or Ethanol-94',
                'value': 'E10'
            }, {
                'pricesAvailable': True,
                'description': 'LPG',
                'value': 'LPG'
            }],
            'icon': [{
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/metro_fuel/mapicon_metro_fuel@1x.png',
                'type': 'mapicon',
                'iconScale': None
            }, {
                'imageurl': 'http://a.b.c/fuelapi/icons/aus/metro_fuel/icon_metro_fuel@1x.png',
                'type': 'icon',
                'iconScale': None
            }],
            'id': 10
        }
    }]

    provider = {
        "_id": 1,
        "name": "Intelematics Fuel",
        "config": {
            "unique_user_id": "AAP",
            "app_name": "AAPSuperdesk",
            "api_url": "http://a.b.c",
            "api_key": "MyAPIKey",
            "market_definitions": "[{'market':'Sydney', 'radius': '30000', 'lat':'-33.8641', 'lon':'151.0802'}]"
        },
        "content_types": [],
        "feeding_service": "intelematics_api_feed",
        "source": "Intelematics"
    }

    def setUp(self):
        init_app(self.app)
        self.setupRemoteSyncMock(self)
        self.app.data.insert('ingest_providers', [self.provider])

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.get_key], *[self.get_prices])
        context.mock.__enter__()

    @urlmatch(scheme='http', netloc='a.b.c', path='/token')
    def get_key(self, url, request):
        resp = {'id': 'YourNewSessionKey'}
        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }

    @urlmatch(scheme='http', netloc='a.b.c', path='/fuel')
    def get_prices(self, url, request):
        headers = {'total': '900'}
        resp_bytes = json.dumps(self.prices)
        return response(status_code=200, headers=headers, content=resp_bytes)

    def test_token(self):
        it = IntelematicsFuelHTTPFeedingService()
        token = it._get_token(self.provider)
        self.assertEqual(token, {'id': 'YourNewSessionKey'})

    def test_save(self):
        it = IntelematicsFuelHTTPFeedingService()
        it._save(self.prices, {'market': 'Sydney', 'radius': '30000', 'lat': '-33.8641', 'lon': '151.0802'})
        prices = self.app.data.find('fuel', None, None)
        self.assertEqual(prices.count(), 50)

    def test_get_prices(self):
        it = IntelematicsFuelHTTPFeedingService()
        prices = it._get_prices(self.provider, {'market': 'Sydney', 'radius': '30000', 'lat': '-33.8641',
                                                'lon': '151.0802'})
        self.assertEqual(len(prices), 10)

    def test_update(self):
        it = IntelematicsFuelHTTPFeedingService()
        it._update(self.provider, {})
