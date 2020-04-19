# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import json
from copy import deepcopy

from superdesk.tests import TestCase
from apps.publish import init_app
from .aap_newsroom_ninjs_formatter import AAPNewsroomNinjsFormatter


class AAPNINJSFormatterTest(TestCase):

    base_article = {
        "_id": "urn:newsml:localhost:2017-08-31T11:40:29.408059:fd448b37-f35d-4bb2-a565-2433dcf1c338",
        "dateline": {
            "source": "AAP",
            "text": "MILTON KEYNES, Aug 31 AAP -",
            "date": "2017-08-31T01:40:29.000Z",
            "located": {
                "tz": "Europe/London",
                "city_code": "Milton Keynes",
                "country": "United Kingdom",
                "city": "Milton Keynes",
                "dateline": "city",
                "state": "England",
                "alt_name": "",
                "country_code": "GB",
                "state_code": "GB.ENG"
            }
        },
        "pubstatus": "usable",
        "profile": "58cf62e01d41c8208dc20375",
        "flags": {
            "marked_archived_only": False,
            "marked_for_sms": False,
            "marked_for_not_publication": False,
            "marked_for_legal": False
        },
        "version_creator": "57bcfc5d1d41c82e8401dcc0",
        "version": 1,
        "state": "in_progress",
        "event_id": "tag:localhost:2017:39642f28-ebb6-4767-863e-58ac9e5810fd",
        "unique_name": "#32467",
        "operation": "update",
        "versioncreated": "2017-08-31T01:44:24.000Z",
        "_created": "2017-08-31T01:40:29.000Z",
        "type": "text",
        "format": "HTML",
        "family_id": "urn:newsml:localhost:2017-08-31T11:40:29.408059:fd448b37-f35d-4bb2-a565-2433dcf1c338",
        "_current_version": 2,
        "sign_off": "MAR",
        "priority": 6,
        "firstcreated": "2017-08-31T01:40:29.000Z",
        "source": "AAP",
        "original_creator": "57bcfc5d1d41c82e8401dcc0",
        "language": "en",
        "unique_id": 32467,
        "guid": "urn:newsml:localhost:2017-08-31T11:40:29.408059:fd448b37-f35d-4bb2-a565-2433dcf1c338",
        "anpa_category": [
            {
                "qcode": "i",
                "scheme": None,
                "name": "International News"
            }
        ],
        "place": [
            {
                "name": "NSW",
                "country": "Australia",
                "group": "Australia",
                "qcode": "NSW",
                "state": "New South Wales",
                "world_region": "Oceania"
            }
        ],
        "urgency": 3,
        "genre": [
            {
                "qcode": "Article",
                "name": "Article"
            }
        ],
        "slugline": "Article Slugline",
        "anpa_take_key": "takekey",
        "ednote": "Article ed note",
        "byline": "Article Byline",
        "subject": [
            {
                "qcode": "01000000",
                "name": "arts, culture and entertainment",
            }
        ],
        "abstract": "<p>Article abstract</p>",
        "sms_message": "",
        "headline": "Article Headline",
        "word_count": 2,
    }

    def setUp(self):
        self.formatter = AAPNewsroomNinjsFormatter()
        init_app(self.app)
        self.maxDiff = None
        self.app.data.insert('vocabularies', [
            {
                "_id": "locators",
                "display_name": "Locators",
                "type": "unmanageable",
                "unique_field": "qcode",
                "items": [
                    {"is_active": True, "name": "NSW", "qcode": "NSW", "state": "New South Wales",
                     "country": "Australia", "world_region": "Oceania", "group": "Australia"},
                ],
            },
            {
                "_id": "crop_sizes",
                "display_name": "Image Crop Sizes",
                "type": "manageable",
                "items": [
                    {
                        "width": 800,
                        "is_active": True,
                        "height": 600,
                        "name": "4-3"
                    },
                    {
                        "width": 1280,
                        "is_active": True,
                        "height": 720,
                        "name": "16-9"
                    }
                ],
                "unique_field": "name",
                "selection_type": "do not show"
            }
        ])

    def test_associated_media_formatter(self):
        article = deepcopy(self.base_article)
        article.update({
            "headline": "‘Article Headline’",
            'body_html': "<p>“Article Body“</p>",
            "abstract": "<p>“Article abstract“</p>",
        })
        article['body_html'] = "<p>“Article Body“</p>"

        seq, doc = self.formatter.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        expected = {"guid": "urn:newsml:localhost:2017-08-31T11:40:29.408059:fd448b37-f35d-4bb2-a565-2433dcf1c338",
                    "headline": "'Article Headline'", "description_text": "\"Article abstract\"", "language": "en",
                    "located": "Milton Keynes", "anpa_take_key": "takekey",
                    "ednote": "Article ed note", "source": "AAP", "firstcreated": "2017-08-31T01:40:29.000Z",
                    "description_html": "<p>\"Article abstract\"</p>", "byline": "Article Byline", "charcount": 14,
                    "body_html": "<p>\"Article Body\"</p>", "slugline": "Article Slugline",
                    "subject": [{"name": "arts, culture and entertainment", "code": "01000000"}],
                    "versioncreated": "2017-08-31T01:44:24.000Z", "wordcount": 2,
                    "service": [{"name": "International News", "code": "i"}], "type": "text", "version": "2",
                    "genre": [{"name": "Article", "code": "Article"}], "priority": 6, "urgency": 3,
                    "readtime": 0,
                    "profile": "58cf62e01d41c8208dc20375", "place": [{"name": "New South Wales", "code": "NSW"}],
                    "pubstatus": "usable", "products": []}
        self.assertEqual(expected, json.loads(doc))

    def test_link_expansion(self):
        article = deepcopy(self.base_article)
        article['body_html'] = "<p>Article Body</p><p>Some text http://aap.com.au some more text</p><p>A bit more</p>" \
            "<p>https://a.b.c/sjhfkjhf</p><p>yadda <a href=\"https://a.b.c/existing\">Existing link text" \
            "</a> fkjhkjfhk</p>" \
            "<p>This is a NSW local court decision&nbsp;https://www.caselaw.nsw.gov.au/decision/5d243010e" \
            "4b08c5b85d8ac7f</p>" \
            "<p><br></p><p> BEFORE http://127.0.0.1:9000/#/workspace/monitoring?assignment=5cb57b165f627d" \
            "6b2c55a192&amp;item=urn:newsml:localhost:2019-07-10T14:24:14.653510:f7554544-88b1-4263-9d46" \
            "-db4424541eff&amp;action=edit AFTER<br></p>" \
            "<p>Instagram ( https://c212.net/c/link/?t=0&amp;l=en&amp;o=2519051-1&amp;h=802772405&amp;" \
            "u=https%3A%2F%2Fc212.net%2Fc%2Flink%2F%3Ft%3D0%26l%3Den%26o%3D2434488-1%26h%3D341010156" \
            "6%26u%3Dhttps%253A%252F%252Furldefense.proofpoint.com%252Fv2%252Furl%253Fu%253Dhttps-3A__" \
            "www.instagram.com_automobilityla_%2526d%253DDwMGaQ%2526c%253D9wxE0DgWbPxd1HCzjwN8Eaww1--" \
            "ViDajIU4RXCxgSXE%2526r%253DTsighQ5d9Vys_pgjwOXtbe-L7jq0CiKHyITp_PSm_7w%2526m%253D4NT5PB8" \
            "zM8WgWXWL9xj-7rCog61nziXpkuqaIM3yrvM%2526s%253DDhXARHgccri7aqVjW4fNJ33toDz3OKMKBPQzLVKKlyM" \
            "%2526e%253D%26a%3DInstagram&amp;a=Instagram )</p>"

        seq, doc = self.formatter.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        expected = {'body_html': '<p>Article Body</p><p>Some text <a '
                                 'href="http://aap.com.au" target="_blank">http://aap.com.au</a> some more '
                                 'text</p><p>A bit more</p><p><a '
                                 'href="https://a.b.c/sjhfkjhf" target="_blank">https://a.b.c/sjhfkjhf</a></p><p>yadda '
                                 '<a href="https://a.b.c/existing">Existing link text</a> '
                                 'fkjhkjfhk</p><p>This is a NSW local court decision&nbsp;<a '
                                 'href="https://www.caselaw.nsw.gov.au/decision/5d243010e4b08c5b85d8ac7f" '
                                 'target="_blank">https://www.caselaw.nsw.gov.au/decision/5d243010e4b08c5b85d8ac7f</a>'
                                 '</p><p><br/></p><p> BEFORE <a '
                                 'href="http://127.0.0.1:9000/#/workspace/monitoring?assignment=5cb57b165f627d6b2c55a'
                                 '192&item=urn:newsml:localhost:2019-07-10T14:24:14.653510:f7554544-88b1-4263-9d46-db'
                                 '4424541eff&action=edit"'
                                 ' target="_blank">http://127.0.0.1:9000/#/workspace/monitoring?assignment=5cb5'
                                 '7b165f627d6b2c55a192&amp;item=urn:newsml:localhost:2019-07-10T14:24:14.653510:f7554544-8'
                                 '8b1-4263-9d46-db4424541eff&amp;action=edit</a> '
                                 'AFTER<br/></p><p>Instagram ( <a '
                                 'href="https://c212.net/c/link/?t=0&l=en&o=2519051-1&h=802772405&u=https%3A%2F%2Fc21'
                                 '2.net%2Fc%2Flink%2F%3Ft%3D0%26l%3Den%26o%3D2434488-1%26h%3D3410101566%26u%3Dhttps%25'
                                 '3A%252F%252Furldefense.proofpoint.com%252Fv2%252Furl%253Fu%253Dhttps-3A__www.instagr'
                                 'am.com_automobilityla_%2526d%253DDwMGaQ%2526c%253D9wxE0DgWbPxd1HCzjwN8Eaww1--ViDajIU'
                                 '4RXCxgSXE%2526r%253DTsighQ5d9Vys_pgjwOXtbe-L7jq0CiKHyITp_PSm_7w%2526m%253D4NT5PB8zM8'
                                 'WgWXWL9xj-7rCog61nziXpkuqaIM3yrvM%2526s%253DDhXARHgccri7aqVjW4fNJ33toDz3OKMKBPQzLVKK'
                                 'lyM%2526e%253D%26a%3DInstagram&a=Instagram"'
                                 ' target="_blank">https://c212.net/c/link/?t=0&amp;l=en&amp;o=2519'
                                 '051-1&amp;h=802772405&amp;u=https%3A%2F%2Fc212.net%2Fc%2Flink%2F%3Ft%3D0%26l%3Den%26o%3D2434'
                                 '488-1%26h%3D3410101566%26u%3Dhttps%253A%252F%252Furldefense.proofpoint.com%252Fv2%25'
                                 '2Furl%253Fu%253Dhttps-3A__www.instagram.com_automobilityla_%2526d%253DDwMGaQ%2526c%2'
                                 '53D9wxE0DgWbPxd1HCzjwN8Eaww1--ViDajIU4RXCxgSXE%2526r%253DTsighQ5d9Vys_pgjwOXtbe-L7j'
                                 'q0CiKHyITp_PSm_7w%2526m%253D4NT5PB8zM8WgWXWL9xj-7rCog61nziXpkuqaIM3yrvM%2526s%253DD'
                                 'hXARHgccri7aqVjW4fNJ33toDz3OKMKBPQzLVKKlyM%2526e%253D%26a%3DInstagram&amp;a=Instagram'
                                 '</a> '
                                 ')</p>',
                    'byline': 'Article Byline',
                    'charcount': 960,
                    'description_html': '<p>Article abstract</p>',
                    'description_text': 'Article abstract',
                    'ednote': 'Article ed note',
                    'firstcreated': '2017-08-31T01:40:29.000Z',
                    'genre': [{'code': 'Article', 'name': 'Article'}],
                    'guid': 'urn:newsml:localhost:2017-08-31T11:40:29.408059:fd448b37-f35d-4bb2-a565-2433dcf1c338',
                    'headline': 'Article Headline',
                    'language': 'en',
                    'located': 'Milton Keynes',
                    'place': [{'code': 'NSW', 'name': 'New South Wales'}],
                    'priority': 6,
                    'products': [],
                    'profile': '58cf62e01d41c8208dc20375',
                    'pubstatus': 'usable',
                    'readtime': 0,
                    'service': [{'code': 'i', 'name': 'International News'}],
                    'slugline': 'Article Slugline',
                    'source': 'AAP',
                    'subject': [{'code': '01000000', 'name': 'arts, culture and entertainment'}],
                    'type': 'text',
                    'urgency': 3,
                    'version': '2',
                    'versioncreated': '2017-08-31T01:44:24.000Z',
                    'wordcount': 29,
                    "anpa_take_key": "takekey"}
        self.assertEqual(expected, json.loads(doc))

    def test_fs_path_guid(self):
        article = deepcopy(self.base_article)
        article.update({
            'ingest_id': '/mnt/content-fs/input/ASIANET_FTP/AsiaNet Press Release 80708'
                         '.tst-123-456-789-0abc-defg12345678',
            'auto_publish': True
        })
        seq, doc = self.formatter.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        ninjs = json.loads(doc)
        self.assertEqual(ninjs['guid'], article['family_id'])
