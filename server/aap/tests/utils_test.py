from superdesk.tests import TestCase
from aap.utils import remove_dateline


class RemoveDatelineTestCase(TestCase):

    def test_opta_dateline(self):

        item = {
            'body_html': '<p>Oct 30 (OPTA) - Results from the NBA games on '
                         'Monday (home team in CAPS)(start times are EST)<br/><br/> '
                         'Portland      103  INDIANA      93<br/> '
                         'PHILADELPHIA  113  Atlanta      92<br/> '
                         'Sacramento     at  Miami            in play<br/> '
                         'Brooklyn       at  New York         in play<br/> '
                         'Golden State   at  Chicago          in play<br/> '
                         'Toronto        at  Milwaukee        in play<br/> '
                         'LA Lakers      at  Minnesota        in play<br/> '
                         'Dallas         at  San Antonio      in play<br/> '
                         'New Orleans    at  Denver           in play<br/></p>'
        }

        remove_dateline(item)
        self.assertNotIn('Oct 30 (OPTA) - ', item.get('body_html'))
        self.assertTrue(item.get('body_html').startswith('<p>Results from the NBA games on'))

    def test_reuters_dateline(self):
        self.maxDiff = None
        item = {
            'body_html': '<p>BENGALURU, Nov 5 (Reuters) - Gold prices were steady in\nearly Asian trade on Monday '
                         'as the dollar eased, while investors\nare tuned in to the U.S. congressional elections'
                         ' on Tuesday.</p>\n<p>FUNDAMENTALS</p>\n<p>* Spot gold was steady at $1,232.86 per '
                         'ounce, as of\n0126 GMT.</p>\n<p>* U.S. gold futures was up 0.1 percent '
                         'at $1,234.6\nper ounce.</p>\n<p>* The dollar index, which measures the '
                         'greenback\nagainst a basket of six major currencies, was down '
                         '0.1 percent.</p>\n<p>* In equities, MSCI\'s broadest index of Asia-Pacific '
                         'shares\noutside Japan slipped 0.2 percent in early\ntrades amid worries about'
                         ' tense Sino-U.S. trade relations.</p>\n<p>* Investors are now focused on the'
                         ' U.S. congressional\nelections on Nov. 6, which will determine whether the '
                         'Republican\nor Democratic party controls Congress, with some predicting\nincreased '
                         'market volatility on the outcome.</p>\n<p>* U.S. job growth rebounded sharply in '
                         'October and wages\nrecorded their largest annual gain in 9-1/2 years, '
                         'pointing to\nfurther labor market tightening that could encourage '
                         'the Federal\nReserve to raise interest rates again in December.</p>\n<p>* The U.S. '
                         'and China are not close to a deal to resolve\ntheir trade differences, the '
                         'White House\'s top economic adviser\nsaid on Friday, adding that he was less '
                         'optimistic than\npreviously that such an agreement would come together.</p>\n<p>* British '
                         'Prime Minister Theresa May\'s office has dismissed\nas \"speculation\" a newspaper report '
                         'that suggests an all-UK\ncustoms deal will be written into the legally binding '
                         'agreement\ngoverning Britain\'s withdrawal from the EU.</p>\n<p>* SPDR Gold Trust, '
                         'the world\'s largest gold-backed\nexchange-traded fund, said its holdings fell '
                         '0.23 percent to\n759.06 tonnes on Friday from 760.82 tonnes on Thursday.</p>\n<p>* Hedge '
                         'funds and money managers raised their net short\nposition in gold by 18,723 contracts '
                         'to 45,622 contracts,\naccording to U.S. Commodity Futures Trading Commission '
                         'data on\nFriday. This was the highest in three weeks.</p>\n<p>* Physical gold demand in '
                         'India was lacklustre last week,\nwith dealers offering discounts for the metal '
                         'ahead of a\ntraditionally busy festival week for the first time in '
                         'at least\nthree years, as high prices kept consumers away.</p>\n<p>* Barrick Gold '
                         'shareholders have voted\noverwhelmingly in favour of the Canadian miner\'s $6.1 '
                         'billion\nacquisition of Africa-focused Randgold Resources, three\npeople familiar '
                         'with the preliminary vote count told Reuters on\nFriday.\n(Reporting by Eileen '
                         'Soreng in Bengaluru; Editing by Gopakumar\nWarrier)</p>'
        }

        body_html = '<p>Gold prices were steady in\nearly Asian trade on Monday ' \
                    'as the dollar eased, while investors\nare tuned in to the U.S. congressional elections' \
                    ' on Tuesday.</p>\n<p>FUNDAMENTALS</p>\n<p>* Spot gold was steady at $1,232.86 per ' \
                    'ounce, as of\n0126 GMT.</p>\n<p>* U.S. gold futures was up 0.1 percent ' \
                    'at $1,234.6\nper ounce.</p>\n<p>* The dollar index, which measures the ' \
                    'greenback\nagainst a basket of six major currencies, was down ' \
                    '0.1 percent.</p>\n<p>* In equities, MSCI\'s broadest index of Asia-Pacific ' \
                    'shares\noutside Japan slipped 0.2 percent in early\ntrades amid worries about' \
                    ' tense Sino-U.S. trade relations.</p>\n<p>* Investors are now focused on the' \
                    ' U.S. congressional\nelections on Nov. 6, which will determine whether the ' \
                    'Republican\nor Democratic party controls Congress, with some predicting\nincreased ' \
                    'market volatility on the outcome.</p>\n<p>* U.S. job growth rebounded sharply in ' \
                    'October and wages\nrecorded their largest annual gain in 9-1/2 years, ' \
                    'pointing to\nfurther labor market tightening that could encourage ' \
                    'the Federal\nReserve to raise interest rates again in December.</p>\n<p>* The U.S. ' \
                    'and China are not close to a deal to resolve\ntheir trade differences, the ' \
                    'White House\'s top economic adviser\nsaid on Friday, adding that he was less ' \
                    'optimistic than\npreviously that such an agreement would come together.</p>\n<p>* British ' \
                    'Prime Minister Theresa May\'s office has dismissed\nas \"speculation\" a newspaper report ' \
                    'that suggests an all-UK\ncustoms deal will be written into the legally binding ' \
                    'agreement\ngoverning Britain\'s withdrawal from the EU.</p>\n<p>* SPDR Gold Trust, ' \
                    'the world\'s largest gold-backed\nexchange-traded fund, said its holdings fell ' \
                    '0.23 percent to\n759.06 tonnes on Friday from 760.82 tonnes on Thursday.</p>\n<p>* Hedge ' \
                    'funds and money managers raised their net short\nposition in gold by 18,723 contracts ' \
                    'to 45,622 contracts,\naccording to U.S. Commodity Futures Trading Commission ' \
                    'data on\nFriday. This was the highest in three weeks.</p>\n<p>* Physical gold demand in ' \
                    'India was lacklustre last week,\nwith dealers offering discounts for the metal ' \
                    'ahead of a\ntraditionally busy festival week for the first time in ' \
                    'at least\nthree years, as high prices kept consumers away.</p>\n<p>* Barrick Gold ' \
                    'shareholders have voted\noverwhelmingly in favour of the Canadian miner\'s $6.1 ' \
                    'billion\nacquisition of Africa-focused Randgold Resources, three\npeople familiar ' \
                    'with the preliminary vote count told Reuters on\nFriday.\n(Reporting by Eileen ' \
                    'Soreng in Bengaluru; Editing by Gopakumar\nWarrier)</p>'

        remove_dateline(item)
        self.assertNotIn('BENGALURU, Nov 5 (Reuters) - ', item.get('body_html'))
        self.assertTrue(item.get('body_html').startswith('<p>Gold prices were steady in\nearly Asian trade on Monday'))
        self.assertEqual(item.get('body_html'), body_html)

    def test_variety_dateline(self):
        item = {
            'body_html': '<p>By Ted Johnson</p>\n<p>LOS ANGELES (Variety.com) - WASHINGTON -- Axios debuts a '
                         'four-week HBO series on Sunday, starting with an interview with President Trump in which '
                         'he confirmed that he was considering an immigration executive order to end birthright '
                         'citizenship and defended his attacks on the media.</p>\n<p>On the latest \'PopPolitics\' '
                         'on SiriusXM, Axios co-founder Jim VandeHei said that during the interview '
                         'he \'got into it\' with Trump over his rhetoric, in the wake of mail bombs sent to '
                         'CNN, top Democrats and other prominent critics, as well as the deadly shooting massacre '
                         'at a Jewish synagogue in Pittsburgh.</p>\n<p>Some of the clips of the interview have '
                         'already been released in advance of the show\'s debut on Sunday evening, but VandeHei '
                         'says that Trump\'s attacks on the press as the \'enemy of the people\' are not just a '
                         'tactic to rouse his base in advance of the midterms.</p>'
        }

        body_html = '<p>By Ted Johnson</p>\n<p>WASHINGTON -- Axios debuts a ' \
                    'four-week HBO series on Sunday, starting with an interview with President Trump in which ' \
                    'he confirmed that he was considering an immigration executive order to end birthright ' \
                    'citizenship and defended his attacks on the media.</p>\n<p>On the latest \'PopPolitics\' ' \
                    'on SiriusXM, Axios co-founder Jim VandeHei said that during the interview ' \
                    'he \'got into it\' with Trump over his rhetoric, in the wake of mail bombs sent to ' \
                    'CNN, top Democrats and other prominent critics, as well as the deadly shooting massacre ' \
                    'at a Jewish synagogue in Pittsburgh.</p>\n<p>Some of the clips of the interview have ' \
                    'already been released in advance of the show\'s debut on Sunday evening, but VandeHei ' \
                    'says that Trump\'s attacks on the press as the \'enemy of the people\' are not just a ' \
                    'tactic to rouse his base in advance of the midterms.</p>'

        remove_dateline(item)
        self.assertNotIn('LOS ANGELES (Variety.com) - ', item.get('body_html'))
        self.assertEqual(item.get('body_html'), body_html)
