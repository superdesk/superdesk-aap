import os
from httmock import urlmatch, HTTMock
from unittest import mock
from unittests import AAPTestCase
from aap.io.feeding_services.aapr import AAPRFeedingService


PROVIDER = {
    "_id": "test_provider",
    "config": {
        "username": "test",
        "password": "test",
        "auth_required": False,
        # Fake URLs used as we are mocking a request anyway
        "login_api_url": "https://contentaapr.com.au/api/v1.0/auth/login",
        "token": "token",
        "token_expiry": "20261020T041827+0000",
        "releases_api_url": "https://contentaapr.com.au/api/v1.0/releases",
        "releases_public_url": "https://contentaapr.com.au/api/v1.0/releases"
        # "kill_email": "test@a.com"
    },
}


class AAPRTestCase(AAPTestCase):
    _calls = None

    def setUp(self):
        super().setUp()
        self.setupMock(self)
        self.app.data.insert(
            "archive",
            [
                {
                    "_id": "123456789",
                    "ingest_id": "AAPR20261016T043100",
                    "state": "published",
                    "type": "text",
                    "_current_version": 1,
                    "unique_name": "1234",
                    "pubstatus": "usable",
                }
            ],
        )
        self.app.data.insert(
            "ingest",
            [
                {
                    "_id": "123456789",
                    "guid": "AAPRb02c6ea1-2d4c-481a-b33a-5d9b5790ced7:1",
                }
            ],
        )
        self.app.data.insert("ingest_providers", [PROVIDER])
        self._calls = 0

    def setupMock(self, context):
        context.mock = HTTMock(*[self.auth_request], *[self.feed_request])
        context.mock.__enter__()

    @urlmatch(scheme="https", netloc="contentaapr.com.au", path="/api/v1.0/auth/login")
    def auth_request(self, url, request):
        return {
            "status_code": 200,
            "content": '{"auth_token": "token", "expires": "20261020T041827+0000"}',
        }

    @urlmatch(scheme="https", netloc="contentaapr.com.au", path="/api/v1.0/releases")
    def feed_request(self, url, request):
        # Check if release_id in url
        if "b02c6ea1-2d4c-481a-b33a-5d9b5790ced7" in url.path:
            dirname = os.path.dirname(os.path.realpath(__file__))
            fixture = os.path.normpath(
                os.path.join(dirname, "../fixtures", "aapr.json")
            )
            with open(fixture, "r") as f:
                feed_raw = f.read()
            return {"status_code": 200, "content": (feed_raw)}

        # This data is slightly different to the file being read in
        data = {
            "data": [
                {
                    "url": "https://contentaapr.com.au/api/v1.0/releases/b02c6ea1-2d4c-481a-b33a-5d9b5790ced7",
                    "dateline": "SYDNEY, Oct. 16, 2026",
                    "summary": "Revolutionary breath lozenges - delivering breath that smells like burnt toast.",
                    "release_id": "b02c6ea1-2d4c-481a-b33a-5d9b5790ced7",
                    "date": "20261016T043100+0000",
                    "title": "AAPR launches revolutionary breath lozenges - TOAST",
                }
            ]
        }
        return {"status_code": 200, "content": data}

    @mock.patch.object(AAPRFeedingService, "get_feed_parser")
    def test_request(self, get_feed_parser):
        with self.app.app_context():
            provider = PROVIDER.copy()
            service = AAPRFeedingService()
            service.provider = provider

            items = service._update(provider, {})[0]

            # Can it access the data
            self.assertEqual(
                items[0]["headline"],
                "AAPR launches revolutionary breath lozenges - TOAST",
            )

            # THUMBNAIL FUNCTIONALITY TESTS
            # Did it get all the attachments
            self.assertEqual(len(items[0]["extra"]["multimedia"]), 3)

            # Did the thumbnail get properly assigned and moved to the front of the array
            self.assertEqual(
                "thumbnailurl" in (items[0]["extra"]["multimedia"][0]), True
            )

            # Was the "photo" tag applied to the thumbnail for AAP Photos thumbnailing
            self.assertEqual(items[0]["extra"]["multimedia"][0].get("type"), "photo")
