import os
from httmock import urlmatch, HTTMock
from unittests import AAPTestCase
from aap.io.feeding_services.bang import BangFeedingService


PROVIDER = {"_id": "test_provider",
            "config": {
                "showbiz_url": "https://url.com/111/aa",
                "music_url": "https://url.com/222/bb",
                "movies_url": "https://url.com/333/cc"
            },
            "feed_parser": "Bang Showbiz"
            }

VOCABULARIES = [
    {"_id": "locators",
     "items": []
     }
]


class bangTestCase(AAPTestCase):

    _calls = None
    filename = "ABC3058248.xml"

    def setUp(self):
        super().setUp()
        self.setupMock(self)
        self.app.data.insert('vocabularies', VOCABULARIES)
        self.app.data.insert('ingest_providers', [PROVIDER])
        self._calls = 0
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, "../fixtures", self.filename))
        with open(fixture) as f:
            self.xml = f.read()

    def setupMock(self, context):
        context.mock = HTTMock(*[self.showbiz_request], *[self.music_request], *[self.movies_request])
        context.mock.__enter__()

    @urlmatch(scheme='https', netloc='url.com', path='/111/aa')
    def showbiz_request(self, url, request):
        return {'status_code': 200, 'content': self.xml}

    @urlmatch(scheme='https', netloc='url.com', path='/222/bb')
    def music_request(self, url, request):
        return {'status_code': 200, 'content': self.xml}

    @urlmatch(scheme='https', netloc='url.com', path='/333/cc')
    def movies_request(self, url, request):
        return {'status_code': 200, 'content': self.xml}

    def test_request(self):
        with self.app.app_context():
            provider = PROVIDER.copy()
            service = BangFeedingService()
            service.provider = provider
            items = service._update(provider, {})
            self.assertEqual(len(items), 3)
