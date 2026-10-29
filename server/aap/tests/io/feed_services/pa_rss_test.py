import os
from bson import ObjectId
from unittests import AAPTestCase
from httmock import urlmatch, HTTMock
from aap.io.feeding_services.pa_rss import PARSSFeedingService

PROVIDER = {
    "_id": ObjectId("68eeeb7f3690206b3712d0a6"),
    "config": {"url": "https://some.api.io/v1/item", "field_aliases": []},
}


class aprssTestCase(AAPTestCase):
    filename = "pa_rss.xml"

    def setUp(self):
        super().setUp()
        self.setupMock(self)
        self.app.data.insert("ingest_providers", [PROVIDER])
        self._calls = 0
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, "../fixtures", self.filename))
        with open(fixture) as f:
            self.xml = f.read()

    def setupMock(self, context):
        context.mock = HTTMock(*[self.atom_request])
        context.mock.__enter__()

    @urlmatch(scheme="https", netloc="some.api.io", path="/v1/item")
    def atom_request(self, url, request):
        return {"status_code": 200, "content": self.xml}

    def test_pa_atom(self):
        with self.app.app_context():
            provider = PROVIDER.copy()
            service = PARSSFeedingService()
            service.provider = provider
            results = service._update(provider, {})
            items = results[0]

            self.assertEqual(len(items), 1)
            target_item = items[0]

            self.assertEqual(
                target_item.get("body_html"), "<p>England loses the Ashes again.</p>"
            )
            self.assertNotIn("abstract", target_item)

            subjects = target_item.get("subject", [])
            self.assertTrue(any(s["qcode"] == "15000000" for s in subjects))

            qcodes = [s["qcode"] for s in subjects]

            target_item["slugline"] = "Cricket England"

            self.assertEqual(len(qcodes), len(set(qcodes)), "Duplicate subjects found!")
