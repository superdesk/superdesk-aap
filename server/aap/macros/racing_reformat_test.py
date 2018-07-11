# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import unittest
from .racing_reformat import racing_reformat_macro


class PreserveFormatTestCase(unittest.TestCase):
    def test_normal_story(self):
        article = {
            'body_html': '<pre>   Race One - Neil Mansell Transport Mdn Hcp 1640m\n\t   BERNIE&#x27;S TIGER '
                         '(R W Stephenson) 3g By Bernardini - La Sangre (10:0-1-2): Ran wide early stages when 9 len '
                         '8th of 11 (6) $17.00 57.0 Straight Home 1800m Gold Coast Mdn Good(3) June 2. Overraced '
                         'early, middle stages, blocked for run near turn when 1-3/4 len 4th of 7 (1) $4.00 57.0 '
                         'Rocking Ossie 1640m Toowoomba Mdn Plate Good(4) June 23. Right in the thick of it here at '
                         'latest. Right in this.\n\t   TAPROCK (R W Stephenson) 3c By Red Dazzler - Araluen Star '
                         '(4:0-1-1): Slowly away, overraced early, middle stages, blocked for run near turn when n'
                         'ose 2nd of 7 (7) $21.00 57.5 Whitman 1300m Toowoomba Mdn Hcp Good(4) June 23. Slowly away'
                         ', eased near 1000m when 1-1/2 len, 3/4 len 3rd of 10 (9) $8.50 57.0 Higher Love, Stannis '
                         '1300m Toowoomba Mdn Plate Soft(5) July 7. Kept working to line here last start. Rates hig'
                         'hly.\n\t   ROULETTE ROYAL (P H Duncan) 3g By Casino Prince - Shara Princess (2:0-0-0): Slo'
                         'wly away, hung out near 800m when 5 len 7th of 11 (9) $14.00 57.0 All Love 1200m Sunshine '
                         'Coast 3yo Mdn Heavy(8) June 10. Settled midfield when 11-3/4 len 9th of 11 (1) $13.00 57.5'
                         ' Sultry Testa 1400m Gold Coast Mdn Good(4) June 23. Went to line tamely at Gold Coast last '
                         'outing. Has claims.\n\t   HEADLIGHTS (Ms T Green) 3g By Big Brown - Moodlighting (4:0-0-0):'
                         ' Wide throughout, inconvenienced near 100m when 25 len 11th of 12 (9) $91.00 56.5 Mr B'
                         'oombastic 1800m Gold Coast Mdn Heavy(9) Feb 3. Eased concluding stages when 8-1/4 len 1'
                         '0th of 11 (8) $51.00 54.5 Country Luck 1400m Gatton Mdn Good(3) June 21. Freshened. Fa'
                         'iled to make an impression at Gatton first-up. Place appeal only.\n\t   I&#x27;M SASSY'
                         ' (P J Richardson) 3f By Sequalo - Avenel (12:0-2-2): Gave all for 2 len 2nd of 6 (1) $'
                         '2.80F 54.0 Written Guarantee 1200m Cunnamulla 2yo+ Mdn Good(3) June 16. Tried hard but'
                         ' no match for winner 3/4 len, 3-3/4 len 3rd of 10 (4) $21.00 57.0 He&#x27;s Our Dragon'
                         ', Galshadow 1000m Alpha 2yo+ Mdn Good(3) June 30. Worth thought.   Ends Toowoomba '
                         'comment race seven\n\t   Ends Toowoomba comment Friday races 1-7\n\t   AAP COMMENT\n</pre>',
            'format': 'preserved'}

        racing_reformat_macro(article)
        self.assertTrue(article['body_html'].startswith('<p>   Race One - Neil Mansell Transport Mdn Hcp '))
        self.assertEqual(article['format'], 'HTML')
