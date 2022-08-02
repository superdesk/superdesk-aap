# 202207228604113-en.xml
import os
from superdesk.tests import TestCase
from superdesk.etree import etree
from aap.io.feed_parsers.globenewswire import GlobeNewsWireNITF


class GlobeNewsWireNITFTestCase(TestCase):

    filename = "202207228604113-en.xml"

    def setUp(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, "../fixtures", self.filename))
        provider = {"name": "Test"}
        with open(fixture) as f:
            self.nitf = f.read()
            self.item = GlobeNewsWireNITF().parse(etree.fromstring(self.nitf), provider)

    def test_item(self):
        self.assertEqual(self.item.get("headline"), "Enernet Global selected to build, own and operate hybrid "
                                                    "power plant for Global Atomic’s Dasa mine in Niger")
        self.assertNotIn("byline", self.item)
        self.assertTrue(self.item['abstract'].startswith('<p>JOHANNESBURG, South Africa, July  22, 2022'
                                                         '  (GLOBE NEWSWIRE) -- '))
        self.assertEqual(self.item["anpa_take_key"], "Enernet Global")
        self.assertEqual(self.item["slugline"], "GlobeNewswire")
