import json
from httmock import urlmatch, HTTMock

from superdesk.tests import TestCase
from apps.publish import init_app
from .gender_agent import GenderAgentFormatter


class GenderAgentFormatterTest(TestCase):
    def setUp(self):
        super().setUp()
        self.formatter = GenderAgentFormatter()
        init_app(self.app)

        self.valid_article = {
            "guid": "1234",
            "headline": "Premier's announcement on local 'schools'",
            "type": "text",
            "byline": "Jane Doe",
            "subject": [{"qcode": "05005002", "name": "middle schools"}],
            "anpa_category": [{"name": "Australian General News", "qcode": "a"}],
            "body_html": "<p>First 'quoted' paragraph.</p><p>Second paragraph.</p>",
        }

        self.subscriber = {
            "_id": 1,
            "name": "Test Subscriber",
            "destinations": [
                {
                    "delivery_type": "http_push",
                    "config": {
                        "resource_url": "http://test.com.au/run_sse",
                        "secret_token": "SecretApp",
                    },
                }
            ],
        }

    def test_can_format(self):
        self.assertTrue(self.formatter.can_format("aap gender", {"type": "text"}))

    def test_format_existing_session_success(self):
        @urlmatch(scheme="http", netloc="test.com.au", method="GET")
        def mock_get(url, request):
            self.assertEqual(
                url.path, "/apps/SecretApp/users/user_sd/sessions/session_sd"
            )
            return {"status_code": 200, "content": "{}"}

        with HTTMock(mock_get):
            results = self.formatter.format(self.valid_article, self.subscriber)

        self.assertEqual(len(results), 1)
        seq, raw_doc = results[0]
        payload = json.loads(raw_doc)

        self.assertEqual(payload["app_name"], "SecretApp")
        self.assertEqual(payload["user_id"], "user_sd")
        self.assertEqual(payload["session_id"], "session_sd")

        # Validate the payload
        inner_body = json.loads(payload["new_message"]["parts"][0]["text"])
        self.assertEqual(inner_body["item_id"], "1234")
        self.assertEqual(
            inner_body["title"], "Premier s announcement on local  schools "
        )
        self.assertIn("First  quoted  paragraph. Second paragraph.", inner_body["body"])
        self.assertEqual(inner_body["byline"], "Jane Doe")

    def test_format_creates_session_when_missing(self):
        post_called = []

        @urlmatch(scheme="http", netloc="test.com.au")
        def mock_endpoints(url, request):
            if request.method == "GET":
                return {"status_code": 404, "content": "not found"}
            if request.method == "POST":
                post_called.append(True)
                return {"status_code": 200, "content": '{"created": true}'}
            return {"status_code": 500}

        with HTTMock(mock_endpoints):
            results = self.formatter.format(self.valid_article, self.subscriber)

        self.assertTrue(post_called)
        self.assertEqual(len(results), 1)
