# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from unittests import AAPTestCase
from .am_bob_publisher import am_bob_publish


class AMBOBPublisherTest(AAPTestCase):
    vocab = [{'_id': 'locators', 'items': [{'qcode': 'FED'}, {
        "group": "Australia",
        "state": "Queensland",
        "qcode": "QLD",
        "country": "Australia",
        "world_region": "Oceania",
        "name": "QLD"
    }, {"country": "",
        "name": "UK",
        "state": "",
        "world_region": "Europe",
        "group": "Rest Of World",
        "qcode": "UK"
        }]}]

    def setUp(self):
        self.app.data.insert('vocabularies', self.vocab)

    def test_sport(self):
        item_in = {
            "_id": "urn:newsml:localhost:2019-05-28T16:07:36.682236:7c1afb83-5cd6-40e0-8223-4ddb44c0fae8",
            "anpa_category": [
                {
                    "name": "Domestic Sport",
                    "qcode": "t"
                }
            ],
            "sign_off": "RTV",
            "anpa_take_key": "(MELBOURNE)",
            "genre": [
                {
                    "name": "Broadcast Script",
                    "qcode": "Broadcast Script"
                }
            ],
            "pubstatus": "usable",
            "type": "text",
            "place": [],
            "original_source": "BOB",
            "source": "AAP",
            "subject": [
                {
                    "name": "Australian rules football",
                    "qcode": "15084000"
                },
                {
                    "name": "sport",
                    "qcode": "15000000"
                }
            ],
            "format": "HTML",
            "body_html": "<p>Collingwood stars Jordan De Goey and Darcy Moore will look to prove their fitness for "
                         "Saturday's AFL clash with Fremantle but midfielder Taylor Adams' groin injury will keep"
                         " him sidelined until after the Magpies' mid-season bye.</p><p>De Goey (shin) and Moore "
                         "(ankle) both missed last week's win over Sydney but will undergo fitness tests before the "
                         "Pies host the Dockers at the MCG.</p><p>Adams had been considered a chance to face the "
                         "Swans but has suffered a setback which will keep him out of action until at least "
                         "round 14.</p><p></p>",
            "headline": "AFL: Mixed injury news for Magpies' AFL stars",
            "slugline": "AFL Injuries",
            "family_id": "urn:newsml:localhost:2019-05-28T16:07:36.682236:7c1afb83-5cd6-40e0-8223-4ddb44c0fae8",
        }

        item = am_bob_publish(item_in)
        self.assertEqual(item['headline'], "Mixed injury news for Magpies' AFL stars")
        self.assertEqual(item['slugline'], 'AM AFL Injuries')
        self.assertEqual(item['place'], [{'qcode': 'FED'}])
        self.assertEqual(item['genre'], [{'name': 'AM Service', 'qcode': 'AM Service'}])

    def test_domestic_news(self):
        item_in = {
            "_id": "urn:newsml:localhost:2019-05-28T16:07:34.981426:16f9f2d3-74de-4b6a-a9a0-02eabdd1f07e",
            "anpa_category": [
                {
                    "name": "Australian General News",
                    "qcode": "a"
                }
            ],
            "sign_off": "RTV",
            "anpa_take_key": "(BRISBANE)",
            "genre": [
                {
                    "name": "Broadcast Script",
                    "qcode": "Broadcast Script"
                }
            ],
            "type": "text",
            "place": [
                {
                    "group": "Australia",
                    "state": "Queensland",
                    "qcode": "QLD",
                    "country": "Australia",
                    "world_region": "Oceania",
                    "name": "QLD"
                }
            ],
            "original_source": "BOB",
            "source": "AAP",
            "subject": [
                {
                    "name": "crime, law and justice",
                    "qcode": "02000000"
                }
            ],
            "format": "HTML",
            "body_html": "<p>A man been charged with fraud and money laundering after an investigation into a cold "
                         "calling investment scam on the Gold Coast.</p><p>The 49-year-old man was extradited from "
                         "Adelaide on Tuesday by detectives from Queensland's Organised Crime Gangs Group to face "
                         "charges in the Brisbane Magistrates Court on Wednesday.</p><p>The detectives were "
                         "investigating a cold call \"boiler room\" scam involving more than 30 businesses "
                         "fraudulently trading on the Gold Coast between 2012 and 2013.</p><p></p>",
            "headline": "QLD: Alleged Qld 'boiler room' scammer charged",
            "slugline": "Scam",
        }

        item = am_bob_publish(item_in)
        self.assertEqual(item['headline'], "Alleged Qld 'boiler room' scammer charged")
        self.assertEqual(item['slugline'], 'AM Scam')
        self.assertEqual(item['place'], [{'country': 'Australia', 'group': 'Australia', 'state': 'Queensland',
                                          'qcode': 'QLD', 'name': 'QLD', 'world_region': 'Oceania'}])
        self.assertEqual(item['genre'], [{'name': 'AM Service', 'qcode': 'AM Service'}])

    def test_agency_content(self):
        item_in = {
            "_id": "urn:newsml:localhost:2019-05-27T12:45:22.037077:4b622ecd-070a-47ad-87d5-8755dd001bac",
            "headline": "UK: Michael Gove joins race to be UK PM",
            "anpa_category": [
                {
                    "name": "International News",
                    "qcode": "i"
                }
            ],
            "genre": [
                {
                    "name": "Broadcast Script",
                    "qcode": "Broadcast Script",
                }
            ],
            "source": "AAP",
            "type": "text",
            "anpa_take_key": "(LONDON)",
            "place": [
                {
                    "country": "",
                    "name": "UK",
                    "state": "",
                    "world_region": "Europe",
                    "group": "Rest Of World",
                    "qcode": "UK"
                }
            ],
            "format": "HTML",
            "body_html": "<p>British environment minister and prominent pro-Brexit campaigner Michael Gove says he "
                         "will be running to replace Theresa May as British prime minister, Sky News reports.</p>"
                         "<p>\"I can confirm that I will be putting my name forward to be prime minister of this "
                         "country,\" Sky News quoted Gove as telling reporters outside his house on Sunday.</p>"
                         "<p>\"I believe that I'm ready to unite the Conservative and Unionist Party, ready to "
                         "deliver Brexit, and ready to lead this great country.\"</p><p>RAW RTV</p><p></p>",
            "subject": [
                {
                    "name": "politics",
                    "qcode": "11000000"
                }
            ],
            "slugline": "UK Gove",
        }
        item = am_bob_publish(item_in)
        self.assertEqual(item['headline'], "Michael Gove joins race to be UK PM")
        self.assertEqual(item['slugline'], 'AM UK Gove')
        self.assertEqual(item['place'], [{'country': '', 'qcode': 'UK', 'group': 'Rest Of World', 'name': 'UK',
                                          'world_region': 'Europe', 'state': ''}])
        self.assertIn('<p>RAW</p>', item['body_html'])
        self.assertEqual(item['genre'], [{'name': 'AM Service', 'qcode': 'AM Service'}])
