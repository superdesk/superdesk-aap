import os
from httmock import urlmatch, HTTMock
from unittest import mock
from unittests import AAPTestCase
from aap.io.feeding_services.cision import CisionFeedingService


PROVIDER = {"_id": "test_provider",
            "config": {
                "username": "test",
                "password": "test",
                "auth_required": False,
                "login_api_url": "https://contentapi.cision.com/api/v1.0/auth/login",
                "token": "token",
                "token_expiry": "20220620T041827+0000",
                "releases_api_url": "https://contentapi.cision.com/api/v1.0/releases",
                "kill_email": "test@a.com"
            }
            }

VOCABULARIES = [{
    "_id": "prnnewswire_location_map",
    "items": [
        {
            "is_active": True,
            "geocode": "USA",
            "qcode": "US"
        },
        {
            "is_active": True,
            "geocode": "CAM",
            "qcode": "CAM"
        },
        {
            "is_active": True,
            "geocode": "UNK",
            "qcode": "UK"
        },
        {
            "is_active": True,
            "geocode": "NZD",
            "qcode": "NZ"
        },
        {
            "is_active": True,
            "geocode": "MDE",
            "qcode": "MID"
        },
        {
            "is_active": True,
            "geocode": "JPN",
            "qcode": "JPN"
        },
        {
            "is_active": True,
            "geocode": "IE",
            "qcode": "IRE"
        },
        {
            "is_active": True,
            "geocode": "EUR",
            "qcode": "EUR"
        },
        {
            "is_active": True,
            "geocode": "CHN",
            "qcode": "CHN"
        },
        {
            "is_active": True,
            "geocode": "CAN",
            "qcode": "CAN"
        },
        {
            "is_active": True,
            "geocode": "AFR",
            "qcode": "AFR"
        },
        {
            "is_active": True,
            "geocode": "ASA",
            "qcode": "ASIA"
        }
    ]
},
    {"_id": "locators",
     "items": []
     }
]


class cisionTestCase(AAPTestCase):

    _calls = None

    def setUp(self):
        super().setUp()
        self.setupMock(self)
        self.app.data.insert('vocabularies', VOCABULARIES)
        self.app.data.insert('archive', [{'_id': "123456789", "ingest_id": "cision20200706C2855",
                                          "state": "published", "type": "text", "_current_version": 1,
                                          "unique_name": "1234", "pubstatus": "usable"}])
        self.app.data.insert('ingest', [{'_id': "123456789", "guid": "cision20221115AE36825:1"}])
        self.app.data.insert('ingest_providers', [PROVIDER])
        self._calls = 0

    def setupMock(self, context):
        context.mock = HTTMock(*[self.auth_request], *[self.feed_request])
        context.mock.__enter__()

    @urlmatch(scheme='https', netloc='contentapi.cision.com', path='/api/v1.0/auth/login')
    def auth_request(self, url, request):
        return {'status_code': 200, 'content': '{"auth_token": "token", "expires": "20200804T181906+0000"}'}

    @urlmatch(scheme='https', netloc='contentapi.cision.com', path='/api/v1.0/releases')
    def feed_request(self, url, request):
        if '20200706C2855' in url.path:
            dirname = os.path.dirname(os.path.realpath(__file__))
            fixture = os.path.normpath(os.path.join(dirname, '../fixtures', 'cision.json'))
            with open(fixture, 'r') as f:
                feed_raw = f.read()
            return {'status_code': 200, 'content': feed_raw}

        if self._calls == 0:
            data = '{"data": [{"company": ["ACME Limited"],"date": "20200706T154100+0000",' \
                   '"release_id": "20200706C2855","title": "ACME Does Something"' \
                   ',"url": "https://contentapi.cision.com/api/v1.0/releases/20200706C2855","status": "PUBLISHED",' \
                   '"summary": "no dateline source", "dateline": "DALLAS, Aug. 28, 2020"}]}'
            self._calls = 1
        else:
            data = '{"data":[{"company": ["ACME"], "release_id": "20200706C2855", "status": "DELETED", "summary":' \
                   '"<p>We are advised by ACME that journalists and other readers should disregard the news ' \
                   'release, ACME Got it wrong and will pretend it never happened,' \
                   ' issued <span class=\\"xn-chron\\">July 19, 2022</span> over PR Newswire.</p><p></p>' \
                   '<p>SOURCE  ACME</p>","date": "20200706T154100+0000",' \
                   '"title": "/DISREGARD RELEASE: ACME/",' \
                   '"url": null}]}'
        return {'status_code': 200, 'content': data}

    @mock.patch.object(CisionFeedingService, 'get_feed_parser')
    def test_request(self, get_feed_parser):
        with self.app.app_context():
            with self.app.mail.record_messages() as outbox:
                provider = PROVIDER.copy()
                service = CisionFeedingService()
                service.provider = provider
                items = service._update(provider, {})[0]
                self.assertEqual(items[0]['headline'], 'ACME Provides Business Update on Hurricane Laura Impact')
                items = service._update(provider, {})[0]
                self.assertEqual(len(items), 0)
                self.assertEqual(len(outbox), 1)
                self.assertEqual(outbox[0].subject, 'CISION: /DISREGARD RELEASE: ACME/')
                outbox = []
                items = service._update(provider, {})[0]
                self.assertEqual(len(outbox), 0)
                self.assertEqual(len(items), 0)
                provider['config']['last_deleted_release_id'] = ''
                items = service._update(provider, {})[0]
                self.assertEqual(len(outbox), 0)
                self.assertEqual(len(items), 0)
