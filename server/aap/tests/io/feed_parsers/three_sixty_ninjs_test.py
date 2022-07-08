# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


import os

from aap.io.feed_parsers.three_sixty_ninjs import ThreeSixtyNinjs

from superdesk.tests import TestCase


class BaseNewMLTwoTestCase(TestCase):
    crop_sizes = {
        "_id": "crop_sizes",
        "display_name": "Image Crop Sizes",
        "type": "manageable",
        "items": [
            {"is_active": True, "name": "4-3", "width": 800, "height": 600},
            {"is_active": True, "name": "16-9", "width": 1280, "height": 720}
        ]
    }

    def setUp(self):
        self.app.data.insert('vocabularies', [self.crop_sizes])
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', self.filename))
        provider = {'name': 'Test'}
        self.parser = ThreeSixtyNinjs()
        self.item = self.parser.parse(fixture, provider=provider)


class ThreeSixtyTestCase(BaseNewMLTwoTestCase):
    filename = '776d6548-f45d-46e3-a3d9-25a1727531f4-8-43.json'

    def test_content(self):
        self.assertEqual(len(self.item), 2)
        self.assertEqual(self.item[0].get('headline'), "Man controls trade sculpture")
        self.assertEqual(self.item[1].get('headline'), "How tech rebooted economics and platforms broke "
                                                       "the invisible hand")
        self.assertEqual(self.item[0].get('guid'), '4dbb15d3-6a17-4827-8aa3-0cefe214bebe')
        self.assertEqual(self.item[1].get('guid'), "776d6548-f45d-46e3-a3d9-25a1727531f4")
        self.assertEqual(self.item[1].get('uri'), "776d6548-f45d-46e3-a3d9-25a1727531f4")
        self.assertEqual(self.item[0].get('type'), "picture")
        self.assertEqual(self.item[1].get('type'), "text")
