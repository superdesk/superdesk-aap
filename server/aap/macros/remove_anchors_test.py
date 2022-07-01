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
from .remove_anchors import remove_anchors
import datetime


class RemoveAnchorsTests(TestCase):
    def test_ap_story_with_anchor(self):
        firstcreated = datetime.datetime(2015, 10, 26, 11, 45, 19, 0)
        item = {
            "source": "AP",
            "state": "ingested",
            "_id": "tag:localhost:2017:77b03a97-df04-446e-a112-94941f1bb12c",
            "firstcreated": firstcreated,
            "subject": [
                {
                    "name": "lifestyle and leisure",
                    "qcode": "10000000"
                },
                {
                    "name": "politics",
                    "qcode": "11000000"
                },
                {
                    "name": "diplomacy",
                    "qcode": "11002000"
                }
            ],
            "place": [
                {
                    "name": "United States"
                }
            ],
            'body_html': "<block>\n                    <p>UNITED NATIONS (AP) — Days after kicking out seven U.N. "
                         "officials, Ethiopia accused them without providing evidence Wednesday of inflating the "
                         "magnitude of humanitarian crisis and taking sides in the war in its Tigray region, while "
                         "U.N. Secretary-General Antonio Guterres pressed the country’s ambassador for documentation "
                         "of the allegations.</p>\n                    <p>The unexpected exchange came at a Security "
                         "Council meeting called to discuss the officials' expulsion amid what the U.N. sees as an "
                         "escalating humanitarian catastrophe in the Horn of Africa nation. To some council members, "
                         "the ejection of the officials — most of them with the U.N.'s humanitarian agency — will "
                         "complicate already difficult aid operations. </p>\n                    <p>Ethiopian "
                         "Ambassador Taye Atske Selassie laid out newly detailed claims about the officials. He "
                         "alleged they inflated the number of needy people by 1 million, cheered the Tigrayan "
                         "forces who are fighting the government, invented a dozen deaths in a camp for displaced "
                         "people, and helped channel Ethiopian migrants from Saudi Arabia to another African nation "
                         "“for training and preparation” to fight with the Tigrayans, among other a"
                         "ccusations. </p>\n                    <p>“Ethiopia deeply resents this experience,\" "
                         "the ambassador said, adding that the government had written to the U.N. about staff conduct "
                         "in July. </p>\n                    <p>A surprised Guterres responded that he had known "
                         "nothing of these allegations and that he had twice asked Prime Minister Abiy Ahmed to "
                         "send him details on any concerns about the impartiality of U.N. staffers.</p>\n           "
                         "         <p>Guterres, <a href=\"https://apnews.com/f5c9015472474462081a8fd769e5b18e\">who "
                         "maintains Ethiopia had no right under the U.N. charter to expel </a> the officials, took a "
                         "rare step for a secretary-general by responding directly in the council chamber. He asked "
                         "the ambassador to provide any written documents that the government may have about any "
                         "alleged wrongdoing by any of the seven officials. </p>\n                    <p>“It is my "
                         "duty to defend the honor of the United Nations,” Guterres told reporters afterward. He said "
                         "if such documents are provided, the U.N. will investigate why he wasn't alerted "
                         "about the matter. </p>\n                    <p>Ethiopia <a href=\"https://apnews.com/"
                         "article/africa-united-nations-ethiopia-tigray-4dbbff1c6fa65da8d9d5c4b2c0029125\">announced "
                         "the expulsions last Thursday</a>, accusing the U.N. officials of meddling in the country’s i"
                         "nternal business.</p>\n                    <p>The country’s foreign ministry later added "
                         "some more specific claims of “grave violations,” such as violating security agreements, "
                         "transferring communications equipment to be used by Tigray forces, spreading misinformation "
                         "and “politicization of humanitarian assistance.” </p>\n                    <p>But much of"
                         " what the ambassador said Wednesday had not been raised publicly before. </p>\n         "
                         "           <p>The expulsions came as the U.N. was increasingly outspoken about what it "
                         "calls the Ethiopian government’s de facto blockade of the Tigray region, where local forces"
                         " have been fighting government soldiers and allied troops since November. </p>\n       "
                         "             <p>The conflict began as a political dispute after Prime Minister Abiy Ahmed "
                         "sidelined the Tigrayan regional party that had dominated Ethiopia’s government for "
                         "decades. The clash spiraled into a war that has killed thousands of people and a "
                         "hunger crisis that threatens still more.</p>\n                    <p>Up to 7 million "
                         "people need food and other aid in Tigray and nearby regions where the fighting has sprea"
                         "d, and an estimated 400,000 people are living in “famine-like conditions,” Guterres said. "
                         "</p>\n                    <p>“The people of Ethiopia are suffering. We have no other "
                         "interest but to help stop that suffering,” he said. </p>\n                    <p>U.N. "
                         "humanitarian chief Martin Griffiths <a href=\"https://apnews.com/article/africa-health-"
                         "united-nations-only-on-ap-famine-a2b1639797c2a31973ce12985d82b865\">told The Associated "
                         "Press </a> last week that only 10% of needed humanitarian supplies have been reaching "
                         "Tigray in recent weeks, </p>\n                    <p>Five of the officials expelled work "
                         "with the U.N. humanitarian agency, another is with the U.N. human rights office and the "
                         "seventh is with UNICEF, the U.N. children’s agency.</p>"
        }

        remove_anchors(item)
        self.assertNotIn('http', item.get('body_html'))
