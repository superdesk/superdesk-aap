import os
from superdesk.tests import TestCase
from superdesk.etree import etree
from aap.io.feed_parsers.bang_parser import BangShowbizParser


class BangShowbizParserTestCase(TestCase):
    filename = "ABC3058248.xml"

    def setUp(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, "../fixtures", self.filename))
        provider = {
            "name": "Test",
            "current_id": "showbiz_url",
            "config": {"showbiz_url": "https://url.com/111/aa"},
        }
        with open(fixture) as f:
            self.xml = f.read()
            self.item = BangShowbizParser().parse(
                etree.fromstring(self.xml.encode("UTF-8")), provider
            )

    def test_item(self):
        self.assertEqual(self.item[0]["headline"], "Headline text here")
        self.assertNotIn("byline", self.item[0])
        self.assertEqual(self.item[0]["abstract"], "Summary text here")
        self.assertEqual(self.item[0]["body_html"], "<p>Body here</p><p>more here</p>")
