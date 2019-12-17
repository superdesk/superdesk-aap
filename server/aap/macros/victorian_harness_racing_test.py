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
from .victorian_harness_racing import process_victorian_harness_racing
from apps.publish import init_app
from bson.objectid import ObjectId


class RacingServiceTestCase(TestCase):
    article = {
        "_id": "urn:newsml:localhost:2019-12-30T16:10:00.167898:42d3e777-a9b9-4a49-8e2d-aa7d33abe50d",
        "subject": [
            {
                "qcode": "15030000",
                "name": "horse racing, harness racing",
                "parent": "15000000"
            }
        ],
        "format": "HTML",
        "source": "AAP",
        "state": "in_progress",
        "task": {
            "desk": ObjectId("54e698a31024542de76d664a"),
            "user": ObjectId("57bcfc5d1d41c82e8401dcc0"),
            "stage": "54e698a31024542de76d6649"
        },
        "pubstatus": "usable",
        "slugline": "",
        "type": "text",
        "body_html": "<p>Craig Rail’s</p><p>Harness Form Guide</p><p>VENUE: Mildura</p><p>DATE:  11/12/19</p><p>RAIL’S "
                     "SPECIALS:</p><p>BEST BET: (Race 4 No.6 Augustus Jack) </p><p>BEST VALUE: (Race 8 No.7 Come On "
                     "Elvis) </p><p>BEST ROUGHIE: (Race 5 No.2 Badelaide)</p><p>RAIL’S $50 FLEXI QUADDIE</p><p>$50.00 "
                     "Flexi Early Quaddie Races 1 – 4 for 138%</p><p>1,2,7/ 1,3,9/ 1,7/ 6,7</p><p>$50.00 Flexi "
                     "Quaddie Races 5 – 8 for 34.72%</p><p>1,2,6,9/ 2,4,6/ 1,6,8/ 1,3,6,7</p><p>Race 1:</p><p>"
                     "OVERVIEW: SHE SAID YES (7) is awkwardly drawn on the inside of the second line but she was a "
                     "dominant winner against a similar line up at Mildura last week and beat a reasonable field at "
                     "Swan Hill in November so she should be competitive again. SAINT HOUDINI (1) went back at the st"
                     "art from a wide gate and didn’t have much luck when sixth last week. He pushed forward to race "
                     "without cover and went to the lead on the home turn but was gunned down by Polonis Our Mate thr"
                     "ee starts back so he must be included amongst the leading chances from the pole position. STYLI"
                     "SH GEM (2) is resuming since May but she finished second behind the smart pacer Gottahaveahobbi"
                     "e at a recent Ararat trial second and both of her victories have come at Mildura so she must be"
                     " respected. JOHNS GRIN (11) ran a much sharper race when second behind SHE SAID YES (7) last we"
                     "ek and has claims along with the fast beginner LITTLE BELIEVER (4) and SYSTAMATIC (8). </p><p>"
                     ""
                     "EARLY SPEED: 4 (likely leader), 1</p><p>SELECTIONS: SHE SAID YES (7), SAINT HOUDINI (1), STYLI"
                     "SH GEM (2), JOHNS GRIN (11) </p><p>RATINGS: 7/ 1,2/ 11/ 4,8</p><p>SUGGESTED BET: SAINT HOUDINI"
                     " (1) each way</p><p>Race 2:</p><p>OVERVIEW: PASSIONATE PURSUIT (1) has been placed in ten of h"
                     "er eleven starts for the season without winning and deserves to break through in this event. Sh"
                     "e raced without cover and went down fighting from the outside of the front line draw two starts"
                     " back so she is a good chance of leading throughout in this event. THE SPIN PROFESSOR (3) has b"
                     "een very lightly raced recently and comes into this race without a trial but he has ability and"
                     " strikes a suitable race first up. VALIANT GEM (9) defeated a field of similar standard last we"
                     "ek where he gained a nice trail behind BULLDOG MACRAY (6) and just got the money. He was travel"
                     "ling nicely but broke stride just prior to the home turn at his previous effort. He is drawn be"
                     "hind a </p><p>moderate beginner but he should be finishing strongly at the end. LOCHSTER (7) ha"
                     "s the perfect trailing draw behind PASSIONATE PURSUIT (1) and JITTABUG (11) was able to win fro"
                     "m the death seat at Maryborough on September 30. </p><p>EARLY SPEED: 1 (possible leader), 3,</p"
                     "><p>SELECTIONS: PASSIONATE PURSUIT (1), THE SPIN PROFESSOR (3), VALIANT GEM (9), LOCHSTER (7) <"
                     "/p><p>RATINGS: 1/ 3/ 7,9/ 11/ 6</p><p>SUGGESTED BET: PASSIONATE PURSUIT (1) to win</p><p>Race 3"
                     ":</p><p>OVERVIEW: SIR ROMAN (7) is a nicely bred pacer, which impressed on debut where he outst"
                     "ayed Sovereigne Bay to win in a sharp mile rate of 1.58.5. This promising South Australian trai"
                     "ned pacer is awkwardly drawn but he appears to be the horse to beat. </p><p>BELLA BRONSKI (1) h"
                     "as had numerous chances but she will appreciate a drop back in class for this assignment and sh"
                     "e does possess a nice sprint when she gains the right conditions. She is worth an investment fr"
                     "om the pole position. WICKED AZZ (4) is making her debut for trainer Luke Watson. She hasn’t ra"
                     "ced since June but she did win a trial at Mildura last week so she cannot be left out of "
                     ". KENSINGTON MAID (2) has been placed in five of her past six starts but she has had a run of "
                     "being drawn on the pole position and she moves out a spot here. She trailed the leader and even"
                     "tual winner Rambunctious last week and is a minor place chance again. </p><p>EARLY SPEED: 1 (po"
                     "ssible leader), 2,4</p><p>SELECTIONS: SIR ROMAN (7), BELLA BRONSKI (1), WICKED AZZ (4), KENSING"
                     "TON MAID (2) </p><p>RATINGS: 7/ 1,4/ 2/ 5,6</p><p>SUGGESTED BET: SIR ROMAN (7) to win</p><p>Rac"
                     "e 4:</p><p>OVERVIEW: AUGUSTUS JACK (6) makes his debut for trainer Boris Devcic and considering"
                     " he worked very hard and outstayed the subsequent Mildura winner Penny Snatcher in reasonable t"
                     "ime at a recent trial victory, he should go close despite the wide draw. CAULONIA TERROR (7) br"
                     "oke through for a deserved victory last week after putting in some big performances where he mi"
                     "ssed away and chased hard. He is a durable pacer and looms as one of the leading chances again."
                     " ARTISTIC CLAIRE (5) will find this race to be a little easier than her latest performances at"
                     " Mildura and she worked home nicely for a close up fourth two weeks ago. Her back luck with the"
                     " barrier draw continues here but she should be finishing off nicely. RUBBERS DILEMMA (4) will u"
                     "tilize her brilliant early pace to find a forward position in the early stages of the event. Sh"
                     "e led out then took cover when a close second two weeks ago and started from a second row draw "
                     "last week. </p><p>EARLY SPEED: 4 (likely early leader), 2,6</p><p>SELECTIONS: AUGUSTUS JACK (6)"
                     ", CAULONIA TERROR (7), ARTISTIC CLAIRE (5), RUBBERS DILEMMA (4)</p><p>RATINGS: 6/ 7/ 4,5/ 3/ 2<"
                     "/p><p>SUGGESTED BET: AUGUSTUS JACK (6) to win</p><p>Race 5:</p><p>OVERVIEW: PATTYS ANGEL (1) is"
                     " shooting for four wins in succession and has the barrier draw to go close again. She led throu"
                     "ghout and recorded a quick mile rate of 1.59.2 when she scored last week. BETTOR B NICE (9) mov"
                     "ed into the death seat mid-race and battled on reasonably well for third in his heat. He produc"
                     "ed a very good performance when third in a strong race prior and he is capable of winning again"
                     "st this class. APACHE WIND (6) showed brilliant early pace to find the front and never looked i"
                     "n any danger of defeat when he won his heat comfortably last week. It will be hard to clear the"
                     " field from barrier six early but he has won three of his past five starts and is worth followi"
                     "ng. BADELAIDE (2) is a handy South Australian trained mare that ran a fair race for third last "
                     "week and is an upset chance from her good draw. </p><p>EARLY SPEED: 1 (possible leader), 3,4,6<"
                     "/p><p>SELECTIONS: PATTYS ANGEL (1), BETTOR B NICE (9), APACHE WIND (6), BADELAIDE (2) </p><p>RA"
                     "TINGS: 1/ 6,9/ 2/ 4/ 3,7,8</p><p>SUGGESTED BET: BETTOR B NICE (9) each way </p><p>Race 6:</p><p"
                     ">OVERVIEW: VELOX EQUUS (6) may lack high speed but he is the strongest horse in the race and he"
                     " will make his presence felt despite drawing on the outside of the front line. He worked hard to"
                     " find the front, was driven along a long way from home and held off his rivals to win last outin"
                     "g. ROCKNROLL LEGEND (2) was able to muster a little more speed than usual at the start when he g"
                     "ot to the front and dictated the terms at his latest victory. BEST OF BEAUTY (1) is a very good "
                     "chance of taking cover over the middle distance so ROCKNROLL LEGEND (2) is definitely a chance o"
                     "f finding the lead again. SMYNANNA MICKEY (4) is a lightly raced mare that has won four of her s"
                     "ix starts to date. She broke stride but made up a lot of ground when third (last of 3) in the tr"
                     "ial won by Augustus Jack last week. She usually possesses early speed and her chances will be en"
                     "hanced if she is able to find the markers in the early stages of the event. FREMARKSGONZO (3) is"
                     " usually competitive at Mildura and is drawn to receive a nice trail just off the pace. </p><p>E"
                     "ARLY SPEED: 2 (possible leader), 1,4</p><p>SELECTIONS: VELOX EQUUS (6), ROCKNROLL LEGEND (2), SM"
                     "YNANNA MICKEY (4), FREMARKSGONZO (3) </p><p>RATINGS: 6/ 2,4/ 3/ 1/ 8?</p><p>SUGGESTED BET: VELOX"
                     " EQUUS (6) each way</p><p>Race 7:</p><p>OVERVIEW: BABY LUV (1) has been placed at her past three"
                     " starts against similar opposition and is drawn to run a big race. She possesses early speed and"
                     " usually aims for the position behind the leader so she is perfectly drawn for this assignment. "
                     "PRESIDENTIALCHANGE (6) ran into second at Mildura last week and has the speed to be in the "
                     " if he can gain some luck from the extreme draw. BAILIEBOROUGH (8) ran a reasonable race for fou"
                     "rth last week and her overall form has been consistent against similar opposition. She can sprin"
                     "t to the line nicely with the right trail forward and will be suited if the leaders go hard in t"
                     "he early stages of the event. SPRINGFIELD SHADOW (4) disappointed last week when he tired in the"
                     " latter stages but he led throughout to win at Mildura prior and he will be aiming to find the l"
                     "ead again here so he is worth another chance. </p><p>EARLY SPEED: 1 (likely early leader), 4,5</"
                     "p><p>SELECTIONS: BABY LUV (1), PRESIDENTIALCHANGE (6), BAILIEBOROUGH (8), SPRINGFIELD SHADOW (4)"
                     " </p><p>RATINGS: 1/ 6,9/ 4/ 7/ 2,5</p><p>SUGGESTED BET: BABY LUV (1) to win</p><p>Race 8:</p><p>"
                     ": COME ON ELVIS (7) has had numerous chances since his latest victory but he gets his chance in "
                     "this event as it is a significant drop back in class on his recent performances. He worked into "
                     "third behind the in-form pacer Magic in Her Moves two starts back. He should be finishing quickl"
                     "y against this opposition. MARKLEIGH JILL (1) couldn’t find the lead in the early stages and bat"
                     "tled on quite well after using some energy at the start when fifth last week. She has run some g"
                     "ood races from the pole position at Mildura recently so she should be suited under these conditi"
                     "ons. FIRE HOUSE ROCK (3) has ordinary numerical form on paper but he is much better than his for"
                     "m suggests and he gets into this race nicely with a concession claim. He also moves to a front r"
                     "ow draw, which will aid his chances. RAINBOW RACER (6) pushed forward to find the lead and won c"
                     "omfortably at Mildura last week. That was a much easier race and he is stepping up in distance h"
                     "ere but he is racing too well to dismiss. </p><p>EARLY SPEED: 1 (possible early leader), 2,3,5,6"
                     "</p><p>SELECTIONS: COME ON ELVIS (7), MARKLEIGH JILL (1), FIRE HOUSE ROCK (3), RAINBOW RACER (6)"
                     " </p><p>RATINGS: 1,7/ 3/ 6/ 2/ 5/ 4</p><p>SUGGESTED BET: COME ON ELVIS (7) each way</p>",
        "profile": "5b272948a5398f8233db14fc",
        "genre": [
            {
                "qcode": "Article",
                "name": "Article"
            }
        ],
        "place": [
            {
                "state": "Victoria",
                "name": "VIC",
                "group": "Australia",
                "country": "Australia",
                "qcode": "VIC",
                "world_region": "Oceania"
            }
        ],
        "original_creator": "57bcfc5d1d41c82e8401dcc0",
        "anpa_category": [
            {
                "subject": "15030001",
                "qcode": "r",
                "name": "Racing (Turf)"
            }
        ],
        "language": "en",
    }

    def setUp(self):
        self.app.data.insert('desks', [{'_id': ObjectId('54e698a31024542de76d664a'), 'source': 'AAP'}])
        self.stage = self.app.data.insert('stages',
                                          [{"_id": ObjectId('54e698a31024542de76d6649'),
                                              "working_stage": True, "default_incoming": True,
                                            "desk": ObjectId('54e698a31024542de76d664a')}])
        init_app(self.app)

    def test_stories(self):
        doc = process_victorian_harness_racing(self.article)
        self.assertTrue(doc.get('body_html').startswith('<p>Race One:</p>'))
        selections = self.app.data.find('archive', None, None)
        self.assertTrue('Selections for Wednesday\'s Mildura trots.-</p><p>Race 1: She Said Yes, '
                        'Saint Houdini, Stylish Gem, Johns Grin </p>' in selections[0].get('body_html'))
