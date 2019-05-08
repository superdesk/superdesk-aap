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
from .am_fronters import am_fronters
from datetime import datetime


class AMFronterTest(AAPTestCase):
    published_items = [
        {
            "_id": "5c40c24b8e64b912f10de3e2",
            "_created": "2019-01-17T17:58:35.000+0000",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>Federal "
                         "Opposition Leader Bill Shorten has kicked off his election campaign with a searing attack "
                         "on big business and the wealthy, in a populist tirade that named and shamed one&nbsp;of "
                         "Australia’s most iconic companies, miner BHP.</p><p> </p><p>PAGES 2-15:</p><p>The government"
                         " is investigating a national data policy that would help law enforcement agencies and the "
                         "foreign investment regulator better adjudicate on sensitive cases. The issue&nbsp;has flared"
                         " due to Chinese group Jangho proposing a $2 billion takeover bid for Healius, which holds "
                         "medical records for millions of Australians.</p><p>The harrowing personal stories of neglect"
                         " and abuse in some aged-care facilities that will be told at the aged care royal commission "
                         "will throw light on the need to fix key issues&nbsp;such as the funding model and pending "
                         "housing crisis, peak bodies of the industry claim.</p><p>E-commerce pioneer Ruslan Kogan "
                         "has blamed Apple and overseas websites dodging GST for a 47 per cent collapse in sales of "
                         "global brands in the December half.</p><p>A little-known stockpicker has defeated 92 other "
                         "investors overseeing tens of billions of dollars to seize the crown of best long-only "
                         "Australian shares strategy in Mercer’s 2018&nbsp;survey. Stephen Woods, who manages the "
                         "$20 million Panther Trust, topped the tables with a 5.6 per cent return for the calendar "
                         "year.</p>",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in the Financial Review, published on January 18, 2019</p>",
            "headline": "Main stories in the Financial Review",
            "type": "text",
            "slugline": "Fronters National"
        },
        {
            "_id": "5c40c2428e64b910eb67af78",
            "_created": "2019-01-17T17:58:26.000+0000",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>Doctors have "
                         "blamed falling numbers of GPs seeing patients in nursing homes on poorly trained and "
                         "overworked nursing staff, younger colleagues opting out and Medicare rebates that&nbsp;"
                         "are too low to cover the cost of visits.</p><p>Pressure is mounting on Myer to provide "
                         "an update to investors on its sales performance over the critical Christmas trading period,"
                         " after revelations that the malaise enveloping&nbsp;the nation’s $310 billion retail sector"
                         " swamped upmarket department store David Jones.</p><p>EU officials are looking at plans to "
                         "delay Brexit until next year if British Prime Minister Theresa May drops her “red lines” "
                         "and returns to Brussels with a request to remain in&nbsp;the EU Customs union.</p><p> </p>"
                         "<p>PAGES 2-6:</p><p>Three of the top five seats most affected by Labor’s plan to impose "
                         "more than $17 billion in tax on family trusts over the next decade are Labor or Greens, "
                         "according to an analysis&nbsp;of tax office data by the Treasurer’s office.</p><p>Queensland"
                         " police have confirmed only 22 specialist officers keep watch on almost 2700 childsex "
                         "offenders, but have defended the monitoring program as they reveal new teams of"
                         " behavioural&nbsp;analysts, psychologists and covert investigators will boost their "
                         "ranks.</p><p>Animals Australia has been accused of “industry sabotage at its worse” -"
                         " akin to the needles in strawberries scandal - as federal MPs and the $2 billion live "
                         "export industry demand&nbsp;an investigation into allegations the charity offered money "
                         "in return for distressing footage.</p><p>Aiia Maasarwe, the young international student "
                         "murdered after getting off a Melbourne tram, was speaking to her sister in Israel when "
                         "she was attacked, with her sibling hearing her&nbsp;cry out and drop the phone.</p><p> <"
                         "/p><p>BUSINESS:</p><p>Australian fund managers have experienced their worst annual returns "
                         "in nearly a decade, buffeted by heightened volatility and sharp falls in global markets.</p"
                         "><p> </p><p>SPORT:</p><p>Australia has another emerging star in Alexei Popyrin, who "
                         "yesterday enjoyed the greatest moment of his senior career at Melbourne Park when getting "
                         "the better of French Open finalist&nbsp;Dominic Thiem.</p>",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in The Australian, published on January 18, 2019</p>",
            "headline": "Main stories in The Australian",
            "type": "text",
            "slugline": "Fronters National"
        },
        {
            "_id": "5c40c2378e64b95d6b871dd0",
            "_created": "2019-01-17T17:58:15.000+0000",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>Furious WA "
                         "farmers are preparing to sue the federal government if it does not ditch new rules they "
                         "believe will kill the $250 million live sheep export industry.</p><p> </p><p>PAGES 3-7:</p"
                         "><p>The mother of a 12-year-old boy who broke into a Geraldton school has told a magistrate"
                         " to lock him up. The boy is among a group of youths accused of jumping a fence at "
                         "Rangeway&nbsp;Primary School and jemmying open a classroom door about 7.30pm on December"
                         " 12.</p><p>Just four days into Channel Nine’s efforts to lure back alienated Today show "
                         "viewers, one of the show’s new hosts sparked a national furore yesterday by linking "
                         "Australia Day to&nbsp;imprisonment rates and rape. Brooke Boney weighed into the Australia "
                         "Day debate in her first week on the network’s revamped flagship breakfast program.</p>"
                         "<p>Gina Rinehart has kept her crown as Australia’s richest person despite her wealth "
                         "shrinking by $2.5 billion over the past year, Forbes’ rich list has revealed.</p><p>A "
                         "planned trial of non-lethal shark drum lines off the South West could start within weeks"
                         " after the environment watchdog gave the proposal the all-clear. The Environmental "
                         "Protection&nbsp;Authority said yesterday it would not assess a trial of smart drum lines"
                         " off Gracetown after concluding it posed practically no environmental risk.</p><p> </p>"
                         "<p>BUSINESS:</p><p>National Offshore Petroleum Safety and Environmental Management Authority "
                         "(NOPSEMA) has decided not to review the versions of reports that damned electrical safety "
                         "on the offshore&nbsp;facilities of Inpex’s Ichthys LNG project.</p><p> </p><p>SPORT:</p>"
                         "<p>Australian one-day captain Aaron Finch has spent time studying footage of himself at his"
                         " attacking best in a bid to find the runs that have eluded him against India.</p>",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in The West Australian, published on January 18, 2019</p>",
            "headline": "Main stories in The West Australian",
            "type": "text",
            "slugline": "Fronters WA"
        },
        {
            "_id": "5c40c2286463b96153f33582",
            "slugline": "Fronters SA",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>Charman Yari "
                         "risked his life to escape war-torn Afghanistan and save his family from the threat of "
                         "kidnapping and death. But in a tragic twist, less than a year since his wife and&nbsp;"
                         "children safely set foot in Australia, his “lovely boy” Arash Yari vanished from a dangerous"
                         " surf beach on the state’s South Coast.</p><p> </p><p>PAGES 2-8:</p><p>More pathology "
                         "samples are likely to be sent interstate for processing as SA Pathology looks for $105 "
                         "million in savings over three years as demanded in the state budget.</p><p>Australia’s "
                         "family favourite food brands are preparing to reduce serving sizes or hike up prices as "
                         "crippling drought and high labour costs and energy prices grip the nation.</p><p>Five "
                         "South Australian aged-care homes have been sanctioned and 13 more served with non-compliance"
                         " notices for failing to meet care and behaviour management standards.</p><p>More than "
                         "$1 billion of projects will be completed in the Adelaide CBD this year as the skyline of "
                         "the city continues to rapidly change.</p><p> </p><p>BUSINESS:</p><p>Gina Rinehart has"
                         " kept her crown as Australia’s richest person despite her wealth shrinking by $2.5 "
                         "billion over the past year, the Forbes’ rich list has revealed.</p><p> </p><p>SPORT:"
                         "</p><p>Three-time world champion Peter Sagan made it two wins in two years at Uraidla "
                         "with a trademark sprint finish to Stage 3 yesterday but it was Patrick Bevin who retained "
                         "the overall&nbsp;lead.</p>",
            "headline": "Main stories in The Advertiser",
            "type": "text",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in The Advertiser, published on January 18, 2019</p>",
            "_created": "2019-01-17T17:58:00.000+0000"
        },
        {
            "_id": "5c40c2166463b94948a89603",
            "slugline": "Fronters NT",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>Michael "
                         "Gunner will do “anything” to stay chief minister, says ousted cabinet member Ken Vowles. "
                         "Mr Gunner sacked Mr Vowles from his jobs as Aboriginal affairs and primary industry&nbsp;"
                         "minister and banned him from caucus late last year after he refused to back his leadership."
                         "</p><p> </p><p>PAGES 2-7:</p><p>Conman Walter Wilton who played a key role in a scheme which "
                         "rorted Royal Darwin Hospital out of almost $150,000 admitted to his crimes in the Supreme "
                         "Court yesterday and is almost&nbsp;certain to be jailed when he returns to court in early "
                         "February.</p><p>A patient, Wade Charles, at the Alice Springs Hospital has slammed the"
                         " “systemic failures” which led to a nightmare stay which saw him assaulted, stolen from "
                         "and forced to spend&nbsp;the night camped on the banks of the Todd River.</p><p>Two Cessna "
                         "aircraft came within a split-second of colliding at above 6000ft in Darwin airspace. An "
                         "investigation by the Australian Transport Safety Bureau found the two aircraft,&nbsp;"
                         "carrying four people between them, missed each other by less than 5m in a terrifying "
                         "near miss 46km southwest of Darwin two years ago.</p><p>Grocery bills are set to grow, "
                         "with popular products downsizing as the drought takes its toll on the food manufacturing "
                         "sector.</p><p> </p><p>SPORT:<br></p><p>Palmerston Magpie Aaron Lonergan has a dream and "
                         "it’s all about playing finals football. Magpie skipper Lonergan is in his seventh season"
                         " with Palmerston and is yet to play a part&nbsp;in the NTFL finals.</p>",
            "headline": "Main stories in the NT News",
            "type": "text",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in the NT News, published on January 18, 2019</p>",
            "_created": "2019-01-17T17:57:42.000+0000"
        },
        {
            "_id": "5c40c2008e64b91303147c32",
            "_created": "2019-01-17T17:57:20.000+0000",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>A brutal "
                         "killer is on the loose in Melbourne, with police desperately appealing to the community "
                         "for information as they investigate the murder of 21-year-old Israeli student Aiia&nbsp;"
                         "Maasarwe.</p><p> </p><p>PAGES 3-6:</p><p>A drop in home loans taken out across the country"
                         " has prompted warnings of further falls in house prices. Increasing interest from "
                         "first-time buyers is unable to offset a drop in&nbsp;investor numbers. Australian Bureau "
                         "of Statistics figures show the number of home loans has tumbled nationally by 18.7 per "
                         "cent.</p><p>European trade officials are digging in over a fight about whether Australian"
                         " producers can keep using household food names such as prosecco and feta, as senior "
                         "government ministers&nbsp;accelerate a $100 billion agreement with the European Union "
                         "despite the stand-off.</p><p>Labor’s controversial pledge to revamp tax benefits on "
                         "dividends has sparked a warning from Mark Freeman, that the policy was a “big risk” for"
                         " investors in the nation’s banks.</p><p>Victorian schools are facing a critical shortage "
                         "of principals, with a third of state school heads set to reach retirement age in the next"
                         " five years.</p><p> </p><p>BUSINESS:</p><p>Woodside remains confident it can hit an output"
                         " target of 100 million barrels of oil equivalent next year, despite a potentially lower-th"
                         "an-expected production forecast for 2019.</p><p> </p><p>SPORT:</p><p>John McEnroe says the"
                         " career of Nick Kyrgios is getting to the point where “there’s some real concern” but the "
                         "American great remains hopeful the 23-year-old can reach his potential.</p>",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in The Age, published on January 18, 2019</p>",
            "headline": "Main stories in The Age",
            "type": "text",
            "slugline": "Fronters Vic"
        },
        {
            "_id": "5c40c1f98e64b9564fa1a0f0",
            "_created": "2019-01-17T17:57:13.000+0000",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>Aiia Maasarwe "
                         "was living her dream in Melbourne before the “horrendous” attack, which police believe was"
                         " random and opportunistic, that ended her life.</p><p> </p><p>PAGES 2-11:</p><p>The status "
                         "of terrorist Neil Prakash remains in limbo after Scott Morrison and Fijian Prime Minister "
                         "Frank Bainimarama failed to address the Islamic State recruiter’s citizenship&nbsp;at a me"
                         "eting yesterday.</p><p>The parents of rising star Kimberly Birrell say the gutsy 20-year-o"
                         "ld won’t let the pressure of performing on the world stage rattle her. The eyes of the nat"
                         "ion will be on Birrell&nbsp;when she stares down world No. 2 Angelique Kerber in a round t"
                         "hree clash at the Australian Open tonight.</p><p>Australia’s family favourite food brands "
                         "are preparing to reduce their serving sizes or hike up their prices as the crippling droug"
                         "ht, high labour costs and increased energy prices&nbsp;grip the nation’s food manufacturin"
                         "g sector.</p><p>Vague safety guidelines and poor driver education are putting thousands of"
                         " children at risk on our roads. The RACV is warning that many motorists are failing to pro"
                         "perly restrain&nbsp;children.</p><p> </p><p>BUSINESS:</p><p>Aussies have snubbed the price"
                         "y new iPhone, according to a trading update from online retailer Kogan.com.&nbsp;Shares in"
                         " the native e-commerce pioneer jumped by more than 20 per cent yesterday after it defied t"
                         "he gloom surrounding the nation’s bricks-and-mortar retail sector to report&nbsp;its stron"
                         "gest Christmas period on record.</p><p> </p><p>SPORT:</p><p>Andre Agassi fears Alex de Min"
                         "aur will pay the price for a brutal second round when the teenager tackles Rafael Nadal at"
                         " the Australian Open.</p>",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in the Herald Sun, published on January 18, 2019</p>",
            "headline": "Main stories in the Herald Sun",
            "type": "text",
            "slugline": "Fronters Vic"
        },
        {
            "_id": "5c40c1ef8e64b95d6b871dbe",
            "_created": "2019-01-17T17:57:03.000+0000",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>Scores of "
                         "firefighters have been deployed across the state ahead of deteriorating weather condit"
                         "ions and fears a string of fires in the South-West could form into a major conflagration"
                         ".</p><p> </p><p>PAGES 4-9:</p><p>The state government says it makes no apologies for spe"
                         "nding more than $350,000 unsuccessfully fighting the Bob Brown Foundation’s High Court ch"
                         "allenge to anti-protest laws. Foundation head and former Greens leader Bob Brown and prot"
                         "ester Jessica Hoyt took the government to the High Court after being charged under the la"
                         "ws in 2016.</p><p>A police officer has fronted Hobart Magistrates Court after another off"
                         "icer accused him of repeatedly punching a suspect. Constable Benjamin Rhys Fogarty yester"
                         "day appeared before Chief Magistrate Catherine Geason for a hearing after pleading not "
                         " to one count of common assault.</p><p>Hobartians should wake up tomorrow morning with "
                         "the long-awaited Bridge of Remembrance finally in place. The two 30m spans of the pedestri"
                         "an bridge linking the Cenotaph with the&nbsp;Queens Domain are due to be lifted into place"
                         " between midnight tonight and 6am tomorrow.</p><p>A proposed luxury tourism development wi"
                         "thin the Walls of Jerusalem National Park shows the couple behind the project, Daniel and "
                         "Simone Hackett, want to erect four semi-permanent buildings on the&nbsp;island they privat"
                         "ely lease.</p><p> </p><p>BUSINESS:</p><p>Aussies have snubbed the pricey new iPhone, accor"
                         "ding to a trading update from online retailer Kogan.com. Shares in the native e-commerce p"
                         "ioneer surged yesterday after it reported&nbsp;it had defied the doom and gloom surroundin"
                         "g the nation’s bricks and mortar retail sector to report its strongest Christmas period on"
                         " record.</p><p> </p><p>SPORT:</p><p>The answers to Australia’s Test top-order woes remain "
                         "as clear as mud after the next batch of aspirants all failed in Hobart yesterday. Playing "
                         "against a mediocre Sri Lankan attack&nbsp;and in the only long-form hitout before the Test "
                         "series, all four of Australia’s Test squad failed.</p>",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in The Mercury, published on January 18, 2019</p>",
            "headline": "Main stories in The Mercury",
            "type": "text",
            "slugline": "Fronters Tas"
        },
        {
            "_id": "5c40c1e48e64b9564fa1a0e0",
            "_created": "2019-01-17T17:56:52.000+0000",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>Authorities"
                         " are pleading with Canberrans to limit their electricity usage on Friday as likely record"
                         "-breaking temperatures push ACT and NSW power networks&nbsp;to their limits.</p><p>The da"
                         "y after the death of her five-year-old daughter, Annabelle, Kathie Potts received a lette"
                         "r that caused her heart to break even further. The letter&nbsp;was from federal Health Mi"
                         "nister Greg Hunt, announcing the government had allocated more than $500,000 for research"
                         " into treating Diffuse Intrinsic Pontine Glioma (DIPG), an aggressive type of childhood br"
                         "ain cancer.</p><p> </p><p>PAGES 2-8:</p><p>The territory government will manage all ACT gov"
                         "ernment workers’ compensation claims from March 1 when it becomes a self-insurer. It means "
                         "federal workplace insurer Comcare will no longer be involved in liability decisions or the "
                         "management of compensation claims for ACT government public servants.</p><p>Labor wants to "
                         "expand the purpose of the Finance Department and end a “caricatured” view of the agency lim"
                         "iting its role to spending control.</p><p>Canberra Hospital’s medical imaging department’s"
                         " budget has blown out by almost $10 million since 2014, driven by staffing shortages in t"
                         "he troubled&nbsp;department. Government data shows costs within the department have been "
                         "steadily increasing with the blame being put on covering the leave of specialists and buy"
                         "ing medical supplies.</p><p>The consortium behind Canberra’s light rail project will star"
                         "t testing the light rail vehicles day and night along the route from Gungahlin to the cit"
                         "y&nbsp;from next Tuesday.</p><p>Australia and Fiji are family again after Scott Morrison’"
                         "s visit to the Pacific, ending a diplomatic freeze in place since a 2006 military coup. E"
                         "ven&nbsp;a stoush over the citizenship of terrorist Neil Prakash could not derail Mr Morr"
                         "ison’s meeting with Fijian Prime Minister Frank Bainimarama.</p><p> </p><p>BUSINESS:</p><"
                         "p>Woodside remains confident it can hit an output target of 100 million barrels of oil eq"
                         "uivalent next year, despite a potentially lower-than-expected&nbsp;production forecast fo"
                         "r 2019.</p><p> </p><p>SPORT:</p><p>World Cup hopeful Tom Banks is poised to turn his back"
                         " on overseas interest to make a long-term commitment to the ACT Brumbies, giving the club"
                         " a major&nbsp;boost four weeks before the Super Rugby season starts.</p>",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in The Canberra Times, published on January 18, 2019</p>",
            "headline": "Main stories in The Canberra Times",
            "type": "text",
            "slugline": "Fronters ACT"
        },
        {
            "_id": "5c40c1db6463b96153f3356e",
            "slugline": "Fronters Qld",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>Listen to the"
                         " missus and live will be the theme of a confronting new beach safety campaign aimed at pu"
                         "tting a stop to Queensland’s horror run of male drownings. Men have made up&nbsp;13 of th"
                         "e 14 victims this season, compared with a total of six tragedies recorded during the same "
                         "period last summer.</p><p> </p><p>PAGES 2-11:</p><p>The global chief of shareable transpor"
                         "tation company Lime has revealed Brisbane has been one of the world’s fastest adopters of "
                         "e-scooters, eclipsing most of the 130 cities where&nbsp;the company has launched.</p><p>Gr"
                         "ocery bills are set to grow, with popular products downsizing as the drought takes its toll"
                         " on food manufacturing.</p><p>Robert Fardon’s survivors have hit out at new sex offender l"
                         "egislation, saying they believed the notorious rapist would be monitored by GPS.</p><p>Nur"
                         "sing homes will be banned from doping elderly residents with drugs to make them easier to "
                         "manage, under tough new rules to be drawn up within weeks.</p><p> </p><p>BUSINESS:</p><p>G"
                         "ina Rinehart has kept her crown as Australia’s richest person despite her wealth shrinking"
                         " by $US2.5 billion ($3.48 billion) over the past year, the Forbes’ rich list has revealed."
                         "</p><p> </p><p>SPORT:</p><p>Friendship will be put to one side today when Queenslander Ash"
                         " Barty looks to keep the party going at Melbourne Park, her sights set on making the fourt"
                         "h round of an Australian Open&nbsp;for the first time.</p>",
            "headline": "Main stories in The Courier-Mail",
            "type": "text",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in The Courier-Mail, published on January 18, 2019</p>",
            "_created": "2019-01-17T17:56:43.000+0000"
        },
        {
            "_id": "5c40c1d08e64b91f5861c71f",
            "_created": "2019-01-17T17:56:32.000+0000",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1: The Royal A"
                         "ustralasian College of Physicians has rubbished Premier Gladys Berejiklian’s claim ther"
                         "e is insufficient evidence to support pill testing, calling on the state’s leader&nbsp;t"
                         "o introduce trials at music festivals to save lives.</p><p> </p><p>PAGES 2-5:</p><p>Nata"
                         "sha Beth Darcy, accused of staging the suicide of her grazier partner Mathew Dunbar, ble"
                         "nded a powerful cocktail of sedatives used to knock him out, the NSW Supreme Court has h"
                         "eard.</p><p>A drop in home loans taken out across the country has prompted more warnings"
                         " of further falls in house prices, with increasing interest from first-time buyers unabl"
                         "e to offset dwindling&nbsp;numbers of investors.</p><p>Labor’s controversial pledge to r"
                         "evamp tax benefits on dividends has sparked a warning from a leading fund manager that t"
                         "he policy was a “big risk” for investors in the nation’s&nbsp;banks.</p><p>European trad"
                         "e officials are digging in over a fight about whether Australian producers can keep usin"
                         "g household food names like prosecco and feta, as senior government ministers&nbsp;accel"
                         "erate a $100 billion agreement with the European Union despite the stand-off.</p><p> </p"
                         "><p>BUSINESS:</p><p>Woodside remains confident it can hit an output target of 100 millio"
                         "n barrels of oil equivalent next year, despite a potentially lower-than-expected product"
                         "ion forecast for 2019.</p><p> </p><p>SPORT:</p><p>Rugby Australia is considering introdu"
                         "cing mandatory hair-follicle tests that could uncover players taking illegal substances "
                         "up to three months before being tested.</p>",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in The Sydney Morning Herald, published on January 18, 2019</p>",
            "headline": "Main stories in The Sydney Morning Herald",
            "type": "text",
            "slugline": "Fronters NSW"
        },
        {
            "_id": "5c40c1c68e64b95b5d7d439f",
            "_created": "2019-01-17T17:56:22.000+0000",
            "body_html": "<p>(Not for publication, this is a guide only.)<br></p><p>PAGE 1:<br></p><p>Strict secrecy"
                         " rules protecting child predators and a huge rise in court suppression orders in the justi"
                         "ce system have been slammed for keeping the NSW public in the dark. Edicts&nbsp;preventing"
                         " the media from reporting on the details of cases have doubled since 2011 - with 366 issue"
                         "d by magistrates and judges in the past two years.</p><p> </p><p>PAGES 2-8:</p><p>Agricult"
                         "ure Minister David Littleproud has blasted the activists who offered cash for live export "
                         "cruelty videos saying payments should be offered “under no circumstances”.</p><p>The statu"
                         "s of terrorist Neil Prakash remains in limbo after Prime Minister Scott Morrison and Fijia"
                         "n counterpart Frank Bainimarama failed to address the Islamic State recruiter’s&nbsp;citiz"
                         "enship during a meeting yesterday.</p><p>Sweltering households in the grip of the state’s "
                         "worst heatwave since 1939 are paying more than a third more for their daily electricity ne"
                         "eds as cranked airconditioners place increased&nbsp;demand on the grid.</p><p>The family o"
                         "f Alex Ross-King, who became the fifth person in four months to die from a suspected overd"
                         "ose at a NSW music festival, have welcomed the arrest of a man police&nbsp;believe could b"
                         "e linked to the supply of the killer narcotics.</p><p> </p><p>BUSINESS:</p><p>Aussies have"
                         " snubbed the pricey new iPhone, according to a trading update from online retailer Kogan.c"
                         "om. Shares in the native e-commerce pioneer jumped by more than 20 per cent&nbsp;yesterday"
                         " after it defied the gloom surrounding the nation’s bricks-and-mortar retail sector to rep"
                         "ort its strongest Christmas period on record.</p><p> </p><p>SPORT:</p><p>Another Australia"
                         "n teen sensation, Alexei Popyrin, is into the third round of the Australian Open after Dom"
                         "inic Thiem retired midway through the third set of their Melbourne Park&nbsp;clash.</p><p>"
                         "</p>",
            "anpa_category": [
                {
                    "name": "Advisories",

                    "qcode": "v"
                }
            ],
            "abstract": "<p>Main stories in The Daily Telegraph, published on January 18, 2019</p>",
            "headline": "Main stories in The Daily Telegraph",
            "type": "text",
            "slugline": "Fronters NSW"
        }

    ]

    def setUp(self):
        now = datetime.now()
        for i in self.published_items:
            i['abstract'] = i['abstract'].replace('January 18, 2019', now.strftime('%B %-d'))
        self.app.data.insert('published', self.published_items)

    def test_fronters(self):
        item = am_fronters({})
        self.assertIn('<p>THE AGE</p><p>PAGE 1: A brutal killer', item['body_html'])
