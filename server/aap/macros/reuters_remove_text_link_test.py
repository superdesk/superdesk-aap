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
from .reuters_remove_text_link import reuters_remove_text_link
import datetime


class ReutersRemoveLinkInTestTests(TestCase):
    def test_reuters_story_with_link(self):
        firstcreated = datetime.datetime(2015, 10, 26, 11, 45, 19, 0)
        item = {
            "source": "Reuters",
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
            'body_html': '<p>The outline, drawn up by a panel to debate Japan''s growth strategy, will likely '
                         'serve as a backbone for any new stimulus package the government may compile later this '
                         'year.</p><p>It also comes ahead of the ruling party''s leadership '
                         'race https://www.reuters.com/world/asia-pacific/digitalisation-minister-backs-japan-pms-'
                         'rival-fight-ruling-party-h that Prime Minister Yoshihide Suga must win to stay on as head '
                         'of state and pursue his policy initiatives.</p><p>The government hopes to raise Japan''s '
                         'long-term growth by boosting labour productivity and the participation rate.</p><p>In the '
                         'growth strategy announced https://www.reuters.com/world/asia-pacific/japan-growth-'
                         'strategy-draft-calls-digitalisation-greener-society-2021-06-02 in June, the government '
                         'also called for stimulating innovation and digital transformation, but the plan''s fate '
                         'could be introuble with Suga''s political standing wavering ahead of elections. (Reporting by'
                         ' Daniel Leussink and Kantaro Komiya; Editing by Jacqueline Wong)</p>'
        }

        reuters_remove_text_link(item)
        self.assertNotIn('http', item.get('body_html'))

