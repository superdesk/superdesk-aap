# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.tests import TestCase
from .yonhap_format import yonhap_format
import datetime


class yonhapTestCase(TestCase):
    #    vocab = [{'_id': 'locators', 'items': [{'qcode': 'US'}]}]

    #    def setUp(self):
    #        self.app.data.insert('vocabularies', self.vocab)

    def test_story(self):
        item = {
            "_id": "urn:newsml:localhost:2017-10-12T12:18:20.363433:d33bd45c-9be2-464f-8305-b7d1ca388007",
            "family_id": "urn:newsml:localhost:2017-10-12T12:18:20.363433:d33bd45c-9be2-464f-8305-b7d1ca388007",
            "original_source": "asiapulse@yna.co.kr",
            "headline": "S. Korean defense chief orders anti-hacking measures",
            "unique_id": 3542601,
            "guid": "<813445789.9548.1507771049748.JavaMail.0900209@mail01a.yna.co.kr>",
            "word_count": 207,
            "language": "en",
            "type": "text",
            "format": "HTML",
            "ingest_provider": "57203c7fca6a9341bedb3fb9",
            "urgency": 3,
            "genre": [
                {
                    "name": "Article (news)",
                    "qcode": "Article"
                }
            ],
            "source": "AAP",
            "pubstatus": "usable",
            "unique_name": "#3542601",
            "body_html": "<div>&#13;\n<body>&#13;\nS. Korean defense chief orders anti-hacking measures<br/>"
                         "&#13;\n   SEOUL, Oct. 12 (Yonhap) -- South Korean Defense Minister Song Young-moo<br/>"
                         "&#13;\nhas ordered the military to take measures to fend off North Korea's<br/>"
                         "&#13;\nhacking attempts, his ministry said Thursday.<br/>"
                         "&#13;\n   The move came amid public criticism of the defense authorities over<br/>"
                         "&#13;\na fresh allegation that the North's hackers stole a vast cache of classified<br/>"
                         "&#13;\nmilitary documents in 2016.<br/>"
                         "&#13;\n   The leaked data includes a South Korea-U.S. wartime operational<br/>"
                         "&#13;\nplan and a \"decapitation\" scheme to remove the Kim Jong-un leadership<br/>"
                         "&#13;\nin the communist nation, according to Rep. Lee Cheol-hee of the ruling<br/>"
                         "&#13;\nDemocratic Party.<br/>&#13;\n<br/>&#13;\n<br/>&#13;\n<br/>"
                         "&#13;\n   There have been a number of reports on the North's cyber threats,<br/>"
                         "&#13;\nincluding its hacking into the South's military database, which was<br/>"
                         "&#13;\nmade public in September last year. But the scale of the hacking had<br/>"
                         "&#13;\nremained undisclosed.<br/>"
                         "&#13;\n   Song and other ministry officials neither confirmed nor denied Lee's<br/>"
                         "&#13;\nclaim.<br/>"
                         "&#13;\n   The minister pointed out the cited hacking case occurred under the<br/>"
                         "&#13;\nprevious administration of Park Geun-hye.<br/>"
                         "&#13;\n   \"Nonetheless, related measures that have been taken stop short of<br/>"
                         "&#13;\nthe people's expectations,\" he said.<br/>"
                         "&#13;\n   He instructed the military to closely review what has been done<br/>"
                         "&#13;\nand find ways to beef up cybersecurity.<br/>"
                         "&#13;\n   lcd@yna.co.kr<br/>"
                         "&#13;\n(END)"
                         "&#13;\n</body>"
                         "&#13;\n<br/><br/><p>(Yonhap)"
                         "&#13;\n</p></div>",
            "priority": 6,
            "ingest_provider_sequence": "1548",
            "operation": "create",
            "state": "ingested",
            "original_creator": ""
        }
        item['firstcreated'] = datetime.datetime(2015, 10, 26, 11, 45, 19, 0)
        res = yonhap_format(item)
        self.assertEqual(item['dateline']['located']['city'], 'Seoul')
        self.assertTrue(res['body_html'].startswith('<p>S. Korean defense chief orders anti-hacking measures'))
