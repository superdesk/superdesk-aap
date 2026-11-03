# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import pytz
from datetime import datetime
from superdesk.tests import TestCase
from .aap_apple_news_formatter import AAPAppleNewsFormatter


class AAPAppleNewsFormatterTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.formatter = AAPAppleNewsFormatter()
        self.app.config["DEFAULT_TIMEZONE"] = "Australia/Sydney"

    def _get_article(self):
        return {
            "type": "text",
            "genre": [{"qcode": "Article"}],
            "format": "HTML",
            "item_id": "1",
            "firstcreated": datetime(
                year=2018,
                month=2,
                day=15,
                hour=11,
                minute=30,
                second=0,
                tzinfo=pytz.UTC,
            ),
            "firstpublished": datetime(
                year=2018,
                month=2,
                day=15,
                hour=12,
                minute=30,
                second=0,
                tzinfo=pytz.UTC,
            ),
            "versioncreated": datetime(
                year=2018,
                month=2,
                day=15,
                hour=13,
                minute=45,
                second=0,
                tzinfo=pytz.UTC,
            ),
            "abstract": "This is abstract",
            "headline": "Headline of the story",
            "byline": "John Doe",
            "dateline": {
                "source": "AAP",
                "located": {
                    "city": "Sydney",
                    "dateline": "city",
                    "city_code": "Sydney",
                },
            },
            "body_html": "<p>The Statement</p>"
            "<p>This is statement first line</p>"
            "<p>This is statement second line</p>"
            "<p></p>"
            "<p>The Verdict</p>"
            "<p>This is verdict 1 first line</p>"
            "<p>This is verdict 1 second line</p>"
            "<p></p>"
            "<p>The Analysis</p>"
            "<p>This is analysis first line</p>"
            "<p>This is analysis second line</p>"
            "<p></p>"
            "<p>The Verdict</p>"
            "<p>This is verdict 2 first line</p>"
            "<p>This is verdict 2 second line</p>"
            "<p></p>"
            "<p>The References</p>"
            "<p>1. This is references http://test.com</p>"
            "<p>2. This is references second line</p>"
            "<p></p>",
        }

    def test_can_format_check(self):
        self.assertTrue(
            self.formatter.can_format(
                self.formatter.format_type,
                {"type": "text", "genre": [{"qcode": "Article"}], "format": "HTML"},
            )
        )

    def test_format_title(self):
        article = self._get_article()
        apple_news = self.formatter._format(article)
        self.assertEqual(apple_news.get("identifier"), "1")
        self.assertEqual(apple_news.get("title"), "Headline of the story")
        self.assertEqual(
            apple_news.get("components"),
            [
                {
                    "layout": "titleLayout",
                    "role": "title",
                    "text": "Headline of the story",
                    "textStyle": "titleStyle",
                    "format": "html",
                },
                {
                    "role": "byline",
                    "text": "By John Doe",
                    "layout": "bylineLayout",
                    "textStyle": "bylineStyle",
                },
                {
                    "role": "byline",
                    "text": "Feb 16, 2018",
                    "layout": "dateLineLayout",
                    "textStyle": "dateLineStyle",
                },
                {
                    "format": "html",
                    "layout": "bodyLayout",
                    "role": "body",
                    "text": "<p>The Statement</p>"
                    "<p>This is statement first line</p>"
                    "<p>This is statement second line</p>"
                    "<p><br></p><p>The Verdict</p>"
                    "<p>This is verdict 1 first line</p>"
                    "<p>This is verdict 1 second line</p>"
                    "<p><br></p><p>The Analysis</p>"
                    "<p>This is analysis first line</p>"
                    "<p>This is analysis second line</p>"
                    "<p><br></p><p>The Verdict</p>"
                    "<p>This is verdict 2 first line</p>"
                    "<p>This is verdict 2 second line</p>"
                    "<p><br></p><p>The References</p>"
                    "<p>1. This is references http://test.com</p>"
                    "<p>2. This is references second line</p><p><br></p>",
                    "textStyle": "bodyStyle",
                },
            ],
        )

    def test_format_article_with_embeds(self):
        article = self._get_article()
        article["associations"] = {
            "featuremedia": {
                "description_text": "Protesters participate in a Halloween themed "
                "Extinction Rebellion rally in Sydney, "
                "Thursday, October 31, 2019."
            },
            "editor_0": {"type": "video"},
            "editor_1": {"type": "picture"},
            "editor_2": None,
        }
        article["fields_meta"] = {
            "body_html": {
                "draftjsState": [
                    {
                        "blocks": [
                            {
                                "key": "f8mk1",
                                "text": "First paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {"MULTIPLE_HIGHLIGHTS": {}},
                            },
                            {
                                "key": "97qeo",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [{"offset": 0, "length": 1, "key": 0}],
                                "data": {},
                            },
                            {
                                "key": "bu6bt",
                                "text": "Second paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {},
                            },
                            {
                                "key": "66lpo",
                                "text": "Third paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {},
                            },
                            {
                                "key": "4sgtb",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [{"offset": 0, "length": 1, "key": 1}],
                                "data": {},
                            },
                            {
                                "key": "9n4jj",
                                "text": "Fourth paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {},
                            },
                            {
                                "key": "1trdb",
                                "text": "Fifth paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {},
                            },
                            {
                                "key": "2jrhi",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [{"offset": 0, "length": 1, "key": 2}],
                                "data": {},
                            },
                            {
                                "key": "d51og",
                                "text": "Sixth paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {},
                            },
                        ],
                        "entityMap": {
                            "0": {"type": "MEDIA", "mutability": "MUTABLE", "data": {}},
                            "1": {
                                "type": "MEDIA",
                                "mutability": "MUTABLE",
                                "data": {
                                    "media": {
                                        "headline": "POLESTAR ELECTRIC VEHICLE",
                                        "alt_text": "Alt Text",
                                        "description_text": "Description text or caption",
                                        "source": "PR Handout Image",
                                        "byline": "PR Handout Image/POLESTAR",
                                        "type": "picture",
                                        "format": "HTML",
                                    }
                                },
                            },
                            "2": {
                                "type": "EMBED",
                                "mutability": "MUTABLE",
                                "data": {
                                    "data": {
                                        "html": '<blockquote class="twitter-tweet"><p lang="en" dir="ltr">'
                                        "&quot;This is actually my first time to ever enter a competition"
                                        ".&quot;<br><br>Photographer Jialing Cai went diving in the dark to "
                                        "capture her award-winning image of a female paper nautilus, a type "
                                        "of octopus that can grow its own shell.<br><br>Via "
                                        '<a href="https://twitter.com/liz?ref_src=twsrc%5Etfw">'
                                        '@liz</a>: <a href="https://t.co/u1rGHr1heD">'
                                        'https://t.co/u1rGHr1heD</a> <a href="https://t.co/SIBTwJfisP">'
                                        "pic.twitter.com/SIBTwJfisP</a></p>&mdash; "
                                        "Australian Associated Press (AAP) (@AAPNewswire) "
                                        '<a href="https://twitter.com/AAPNewswire/status/1">'
                                        "November 16, 2023</a></blockquote> <script async "
                                        'src="https://platform.twitter.com/widgets.js" charset="utf-8">'
                                        "</script>"
                                    }
                                },
                            },
                        },
                    }
                ]
            }
        }
        apple_news = self.formatter._format(article)
        self.assertEqual(apple_news["components"][6]["URL"], "bundle://editor_1")
        self.assertEqual(
            apple_news["components"][0]["style"]["fill"]["URL"], "bundle://featuremedia"
        )
        self.assertEqual(
            apple_news["components"][9]["URL"],
            "https://twitter.com/AAPNewswire/status/1",
        )

    def test_format_article_with_instagram(self):
        article = self._get_article()
        article["fields_meta"] = {
            "body_html": {
                "draftjsState": [
                    {
                        "blocks": [
                            {
                                "key": "bkf9p",
                                "text": "instagram",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {"MULTIPLE_HIGHLIGHTS": {}},
                            },
                            {
                                "key": "ed90t",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [{"offset": 0, "length": 1, "key": 0}],
                                "data": {},
                            },
                            {
                                "key": "30a8e",
                                "text": "",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {},
                            },
                        ],
                        "entityMap": {
                            "0": {
                                "type": "EMBED",
                                "mutability": "MUTABLE",
                                "data": {
                                    "data": {
                                        "html": '<blockquote class="instagram-media" data-instgrm-captioned '
                                        'data-instgrm-permalink="https://www.instagram.com/reel/C" '
                                        'data-instgrm-version="14" style=" background:#FFF; border:0; '
                                        "border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 "
                                        "rgba(0,0,0,0.15); margin: 1px; max-width:540px; min-width:326px; "
                                        "padding:0; width:99.375%; width:-webkit-calc(100% - 2px); "
                                        'width:calc(100% - 2px);"></blockquote> '
                                    },
                                    "description": "Test Instagram post",
                                },
                            }
                        },
                    }
                ]
            }
        }
        apple_news = self.formatter._format(article)
        self.assertEqual(
            apple_news["components"][4]["URL"], "https://www.instagram.com/reel/C"
        )

    def test_format_article_with_facebook(self):
        article = self._get_article()
        article["fields_meta"] = {
            "body_html": {
                "draftjsState": [
                    {
                        "blocks": [
                            {
                                "key": "tqgt",
                                "text": "Facebook post",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {"MULTIPLE_HIGHLIGHTS": {}},
                            },
                            {
                                "key": "b0nn5",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [{"offset": 0, "length": 1, "key": 0}],
                                "data": {},
                            },
                            {
                                "key": "1loq9",
                                "text": "Following text",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {},
                            },
                        ],
                        "entityMap": {
                            "0": {
                                "type": "EMBED",
                                "mutability": "MUTABLE",
                                "data": {
                                    "data": {
                                        "html": '<iframe src="https://www.facebook.com/plugins/post.php?'
                                        "href=https%3A%2F%2Fwww.facebook.com%2Faapnewswire%2Fposts%2Fpfbid"
                                        '&show_text=true&width=500" width="500" height="716" '
                                        'style="border:none;overflow:hidden" scrolling="no" frameborder="0" '
                                        'allowfullscreen="true" allow="autoplay; clipboard-write; '
                                        'encrypted-media; picture-in-picture; web-share"/>'
                                    },
                                    "description": "Embed description",
                                },
                            }
                        },
                    }
                ]
            }
        }
        apple_news = self.formatter._format(article)
        self.assertEqual(
            apple_news["components"][4]["URL"],
            "https://www.facebook.com/aapnewswire/posts/pfbid",
        )

    def test_format_article_with_tik_tok(self):
        article = self._get_article()
        article["fields_meta"] = {
            "body_html": {
                "draftjsState": [
                    {
                        "blocks": [
                            {
                                "key": "36ias",
                                "text": "Tcik Tock Test",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {"MULTIPLE_HIGHLIGHTS": {}},
                            },
                            {
                                "key": "cshfs",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [{"offset": 0, "length": 1, "key": 0}],
                                "data": {},
                            },
                            {
                                "key": "7n6o7",
                                "text": "Following text",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {},
                            },
                            {
                                "key": "bsq3s",
                                "text": "",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {},
                            },
                        ],
                        "entityMap": {
                            "0": {
                                "type": "EMBED",
                                "mutability": "MUTABLE",
                                "data": {
                                    "data": {
                                        "html": '<blockquote class="tiktok-embed" '
                                        'cite="https://www.tiktok.com/@dic/video/7" data-video-id="7" '
                                        'style="max-width: 605px;min-width: 325px;" ></blockquote>'
                                    },
                                    "description": "Tik Toc Test description",
                                },
                            }
                        },
                    }
                ]
            }
        }
        apple_news = self.formatter._format(article)
        self.assertEqual(
            apple_news["components"][4]["URL"], "https://www.tiktok.com/@dic/video/7"
        )

    def test_format_article_invalid_state(self):
        article = dict(
            {
                "_id": "urn:newsml:aap.com.au:2024-08-19T13:54:44.202653:7dadef10-6d92-4ae0-a5d6-a37b542fbf7d",
                "type": "text",
                "version": 1,
                "headline": "Rashid Khan to skip BBL in blow to CA and Strikers",
                "slugline": "BBL",
                "abstract": "<p>",
                "byline": "Scott Bailey",
                "priority": 5,
                "pubstatus": "usable",
                "description_text": None,
                "body_html": "<p></p>",
                "format": "HTML",
                "associations": {
                    "editor_0": {
                        "_id": "tag:aap.com.au:2024:83ac9832-27a3-401a-8e43-053df110f7b0",
                        "guid": "tag:aap.com.au:2024:83ac9832-27a3-401a-8e43-053df110f7b0",
                        "headline": "CRICKET AUSTRALIA WEST INDIES",
                        "description_text": "Windies pace ace Shamar Joseph will bring star power as a new "
                                            "BBL addition.",
                        "source": "AAP Image",
                        "original_source": "AAP Image/AAP",
                        "versioncreated": "2024-08-19T04:43:23+0000",
                        "firstcreated": "2024-01-28T06:30:57+0000",
                        "pubstatus": "usable",
                        "type": "picture",
                        "state": "published",
                        "slugline": "BBL",
                        "byline": "Darren England/AAP PHOTOS",
                        "mimetype": "image/jpeg",
                        "uri": "20240128001894692527",
                        "unique_id": 25927104,
                        "unique_name": "#25927104",
                        "_current_version": 1,
                    },
                    "featuremedia": {
                        "_id": "tag:aap.com.au:2024:831ead76-ee07-440e-8ffd-1e1713ae1d11",
                        "guid": "tag:aap.com.au:2024:831ead76-ee07-440e-8ffd-1e1713ae1d11",
                        "headline": "BBL HEAT STRIKERS",
                        "description_text": "Popular spin star Rashid Khan will miss the BBL again this summer. ",
                        "source": "AAP Image",
                        "original_source": "AAP Image/AAP",
                        "versioncreated": "2024-08-19T04:40:29+0000",
                        "firstcreated": "2022-01-12T09:34:55+0000",
                        "pubstatus": "usable",
                        "type": "picture",
                        "state": "published",
                        "slugline": "BBL",
                        "byline": "Darren England/AAP PHOTOS",
                        "ednote": "NO ARCHIVING",
                        "mimetype": "image/jpeg",
                        "uri": "20220112001612767199",
                        "unique_id": 25927100,
                        "unique_name": "#25927100",
                        "_current_version": 1,
                    },
                    "editor_3": {
                        "_id": "tag:aap.com.au:2024:b691c82c-cdc4-4242-9aac-a66c05dfeb12",
                        "guid": "tag:aap.com.au:2024:b691c82c-cdc4-4242-9aac-a66c05dfeb12",
                        "headline": "CRICKET WBBL RENEGADES HEAT",
                        "description_text": "India's Harmanpreet Kaur will be back in the WBBL.",
                        "source": "AAP Image",
                        "original_source": "AAP Image/AAP",
                        "versioncreated": "2024-08-19T05:02:36+0000",
                        "firstcreated": "2023-10-20T05:19:49+0000",
                        "pubstatus": "usable",
                        "type": "picture",
                    },
                },
                "_updated": "2024-08-19T05:06:51.000+0000",
                "_created": "2024-08-19T03:54:44.000+0000",
                "_current_version": 12,
                "firstcreated": "2024-08-19T03:54:44.000+0000",
                "versioncreated": "2024-08-19T05:06:05.000+0000",
                "original_creator": "576b7955a5398f65d12ad0dc",
                "guid": "urn:newsml:aap.com.au:2024-08-19T13:54:44.202653:7dadef10-6d92-4ae0-a5d6-a37b542fbf7d",
                "state": "published",
                "source": "AAP",
                "urgency": 1,
                "dateline": {
                    "source": "AAP",
                    "date": "2024-08-19T03:54:44.000+0000",
                    "located": {
                        "city": "Sydney",
                        "state": "New South Wales",
                        "country": "Australia",
                        "dateline": "city",
                        "tz": "Australia/Sydney",
                        "alt_name": "",
                        "state_code": "NSW",
                        "city_code": "Sydney",
                        "country_code": "AU",
                    },
                    "text": "SYDNEY, Aug 19 AAP -",
                },
                "language": "en",
                "operation": "publish",
                "expiry": "2024-08-22T05:06:30.000+0000",
                "fields_meta": {
                    "body_html": {
                        "draftjsState": [
                            {
                                "blocks": [
                                    {
                                        "key": "8smap",
                                        "text": " ",
                                        "type": "atomic",
                                        "depth": 0,
                                        "inlineStyleRanges": [],
                                        "entityRanges": [
                                            {"offset": 0, "length": 1, "key": 1}
                                        ],
                                        "data": {},
                                    },
                                    {
                                        "key": "fq1t0",
                                        "text": "Suspect text block with a table at the end!",
                                        "type": "unstyled",
                                        "depth": 0,
                                        "inlineStyleRanges": [],
                                        "entityRanges": [
                                            {"offset": 127, "length": 1, "key": 2}
                                        ],
                                        "data": {},
                                    },
                                    {
                                        "key": "ffusc",
                                        "text": " ",
                                        "type": "atomic",
                                        "depth": 0,
                                        "inlineStyleRanges": [],
                                        "entityRanges": [
                                            {"offset": 0, "length": 1, "key": 3}
                                        ],
                                        "data": {},
                                    },
                                ],
                                "entityMap": {
                                    "0": {
                                        "type": "MEDIA",
                                        "mutability": "MUTABLE",
                                        "data": {
                                            "media": {
                                                "_id": "tag:aap.com.au:2024:83ac9832-27a3-401a-8e43-053df110f7b0",
                                                "guid": "tag:aap.com.au:2024:83ac9832-27a3-401a-8e43-053df110f7b0",
                                                "headline": "CRICKET AUSTRALIA WEST INDIES",
                                                "description_text": "Windies pace ace Shamar Joseph will "
                                                                    "bring star power",
                                                "source": "AAP Image",
                                                "original_source": "AAP Image/AAP",
                                                "versioncreated": "2024-08-19T04:43:23+0000",
                                                "firstcreated": "2024-01-28T06:30:57+0000",
                                                "pubstatus": "usable",
                                                "type": "picture",
                                                "state": "fetched",
                                                "slugline": "CRICKET AUSTRALIA WEST INDIES",
                                                "byline": "Darren England/AAP PHOTOS",
                                                "mimetype": "image/jpeg",
                                            }
                                        },
                                    },
                                    "1": {
                                        "type": "MEDIA",
                                        "mutability": "MUTABLE",
                                        "data": {
                                            "media": {
                                                "_id": "tag:aap.com.au:2024:49b4d3cc-1055-402f-82b4-fb42378d4d7f",
                                                "guid": "tag:aap.com.au:2024:49b4d3cc-1055-402f-82b4-fb42378d4d7f",
                                                "headline": "CRICKET BBL STRIKERS SIXERS",
                                                "description_text": "Rashid Khan won plenty of fans.",
                                                "source": "AAP Image",
                                                "original_source": "AAP Image/AAP",
                                                "versioncreated": "2024-08-19T04:40:21+0000",
                                                "firstcreated": "2022-12-14T10:17:21+0000",
                                                "pubstatus": "usable",
                                                "type": "picture",
                                                "state": "fetched",
                                                "slugline": "CRICKET BBL STRIKERS SIXERS",
                                                "byline": "Matt Turner/AAP PHOTOS",
                                                "mimetype": "image/jpeg",
                                                "uri": "20221214001742440638",
                                                "unique_id": 25927099,
                                                "unique_name": "#25927099",
                                                "_current_version": 1,
                                            }
                                        },
                                    },
                                    "2": {
                                        "type": "TABLE",
                                        "mutability": "MUTABLE",
                                        "data": {
                                            "data": {
                                                "numRows": 1,
                                                "numCols": 2,
                                                "cells": [
                                                    [
                                                        {
                                                            "blocks": [
                                                                {
                                                                    "key": "53ilp",
                                                                    "text": "Sophie Ecclestone ",
                                                                    "type": "unstyled",
                                                                    "depth": 0,
                                                                    "inlineStyleRanges": [],
                                                                    "entityRanges": [],
                                                                    "data": {},
                                                                }
                                                            ],
                                                            "entityMap": {},
                                                        },
                                                        {"blocks": [], "entityMap": {}},
                                                    ]
                                                ],
                                            }
                                        },
                                    },
                                    "3": {
                                        "type": "MEDIA",
                                        "mutability": "MUTABLE",
                                        "data": {
                                            "media": {
                                                "_id": "tag:aap.com.au:2024:b691c82c-cdc4-4242-9aac-a66c05dfeb12",
                                                "guid": "tag:aap.com.au:2024:b691c82c-cdc4-4242-9aac-a66c05dfeb12",
                                                "headline": "CRICKET WBBL RENEGADES HEAT",
                                                "description_text": "India's Harmanpreet Kaur will "
                                                                    "be back in the WBBL.",
                                                "source": "AAP Image",
                                                "original_source": "AAP Image/AAP",
                                                "versioncreated": "2024-08-19T05:02:36+0000",
                                                "firstcreated": "2023-10-20T05:19:49+0000",
                                                "pubstatus": "usable",
                                                "type": "picture",
                                                "state": "fetched",
                                                "slugline": "CRICKET WBBL RENEGADES HEAT",
                                                "byline": "James Ross/AAP PHOTOS",
                                                "mimetype": "image/jpeg",
                                                "uri": "20231020001854383455",
                                                "unique_id": 25927147,
                                                "unique_name": "#25927147",
                                                "_current_version": 1,
                                            }
                                        },
                                    },
                                },
                            }
                        ]
                    },
                    "headline": {
                        "draftjsState": [
                            {
                                "blocks": [
                                    {
                                        "key": "e6730",
                                        "text": "Rashid Khan to skip BBL in blow to CA and Strikers",
                                        "type": "unstyled",
                                        "depth": 0,
                                        "inlineStyleRanges": [],
                                        "entityRanges": [],
                                        "data": {"MULTIPLE_HIGHLIGHTS": {}},
                                    }
                                ],
                                "entityMap": {},
                            }
                        ]
                    },
                    "abstract": {
                        "draftjsState": [
                            {
                                "blocks": [
                                    {
                                        "key": "7dbu4",
                                        "text": "Highly-marketable and successful Afghanistan spinner Rashid Khan",
                                        "type": "unstyled",
                                        "depth": 0,
                                        "inlineStyleRanges": [],
                                        "entityRanges": [],
                                        "data": {"MULTIPLE_HIGHLIGHTS": {}},
                                    }
                                ],
                                "entityMap": {},
                            }
                        ]
                    },
                },
                "firstpublished": "2024-08-19T05:06:30.000+0000",
            }
        )
        article["firstcreated"] = datetime(
            year=2018, month=2, day=15, hour=11, minute=30, second=0, tzinfo=pytz.UTC
        )
        article["firstpublished"] = datetime(
            year=2018, month=2, day=15, hour=12, minute=30, second=0, tzinfo=pytz.UTC
        )
        article["versioncreated"] = datetime(
            year=2018, month=2, day=15, hour=13, minute=45, second=0, tzinfo=pytz.UTC
        )
        article["item_id"] = article["_id"]

        apple_news = self.formatter._format(article)
        self.assertNotIn("<table>", apple_news["components"][8]["text"])

    def test_format_article_invalid_state_pic(self):
        article = dict(
            {
                "_id": "urn:newsml:aap.com.au:2024-08-19T13:54:44.202653:7dadef10-6d92-4ae0-a5d6-a37b542fbf7d",
                "type": "text",
                "version": 1,
                "headline": "Rashid Khan to skip BBL in blow to CA and Strikers",
                "slugline": "BBL",
                "abstract": "<p>",
                "byline": "Scott Bailey",
                "priority": 5,
                "pubstatus": "usable",
                "description_text": None,
                "body_html": "<p></p>",
                "format": "HTML",
                "associations": {
                    "editor_0": {
                        "_id": "tag:aap.com.au:2024:83ac9832-27a3-401a-8e43-053df110f7b0",
                        "guid": "tag:aap.com.au:2024:83ac9832-27a3-401a-8e43-053df110f7b0",
                        "headline": "CRICKET AUSTRALIA WEST INDIES",
                        "description_text": "Windies pace ace Shamar Joseph will bring star power "
                                            "as a new BBL addition.",
                        "source": "AAP Image",
                        "original_source": "AAP Image/AAP",
                        "versioncreated": "2024-08-19T04:43:23+0000",
                        "firstcreated": "2024-01-28T06:30:57+0000",
                        "pubstatus": "usable",
                        "type": "picture",
                        "state": "published",
                        "slugline": "BBL",
                        "byline": "Darren England/AAP PHOTOS",
                        "mimetype": "image/jpeg",
                        "uri": "20240128001894692527",
                        "unique_id": 25927104,
                        "unique_name": "#25927104",
                        "_current_version": 1,
                    },
                    "featuremedia": {
                        "_id": "tag:aap.com.au:2024:831ead76-ee07-440e-8ffd-1e1713ae1d11",
                        "guid": "tag:aap.com.au:2024:831ead76-ee07-440e-8ffd-1e1713ae1d11",
                        "headline": "BBL HEAT STRIKERS",
                        "description_text": "Popular spin star Rashid Khan will miss the BBL again this summer. ",
                        "source": "AAP Image",
                        "original_source": "AAP Image/AAP",
                        "versioncreated": "2024-08-19T04:40:29+0000",
                        "firstcreated": "2022-01-12T09:34:55+0000",
                        "pubstatus": "usable",
                        "type": "picture",
                        "state": "published",
                        "slugline": "BBL",
                        "byline": "Darren England/AAP PHOTOS",
                        "ednote": "NO ARCHIVING",
                        "mimetype": "image/jpeg",
                        "uri": "20220112001612767199",
                        "unique_id": 25927100,
                        "unique_name": "#25927100",
                        "_current_version": 1,
                    },
                },
                "_updated": "2024-08-19T05:06:51.000+0000",
                "_created": "2024-08-19T03:54:44.000+0000",
                "_current_version": 12,
                "firstcreated": "2024-08-19T03:54:44.000+0000",
                "versioncreated": "2024-08-19T05:06:05.000+0000",
                "original_creator": "576b7955a5398f65d12ad0dc",
                "guid": "urn:newsml:aap.com.au:2024-08-19T13:54:44.202653:7dadef10-6d92-4ae0-a5d6-a37b542fbf7d",
                "state": "published",
                "source": "AAP",
                "urgency": 1,
                "dateline": {
                    "source": "AAP",
                    "date": "2024-08-19T03:54:44.000+0000",
                    "located": {
                        "city": "Sydney",
                        "state": "New South Wales",
                        "country": "Australia",
                        "dateline": "city",
                        "tz": "Australia/Sydney",
                        "alt_name": "",
                        "state_code": "NSW",
                        "city_code": "Sydney",
                        "country_code": "AU",
                    },
                    "text": "SYDNEY, Aug 19 AAP -",
                },
                "language": "en",
                "operation": "publish",
                "expiry": "2024-08-22T05:06:30.000+0000",
                "fields_meta": {
                    "body_html": {
                        "draftjsState": [
                            {
                                "blocks": [
                                    {
                                        "key": "7onrg",
                                        "text": 'An excessive reliance on renewables "is going to cause a lot '
                                                'of grief to the country", Mr Dutton said. ',
                                        "type": "unstyled",
                                        "depth": 0,
                                        "inlineStyleRanges": [],
                                        "entityRanges": [
                                            {"offset": 0, "length": 1, "key": 1}
                                        ],
                                        "data": {},
                                    },
                                    {
                                        "key": "1n0hk",
                                        "text": " ",
                                        "type": "atomic",
                                        "depth": 0,
                                        "inlineStyleRanges": [],
                                        "entityRanges": [
                                            {"offset": 0, "length": 1, "key": 1}
                                        ],
                                        "data": {},
                                    },
                                ],
                                "entityMap": {
                                    "1": {
                                        "type": "MEDIA",
                                        "mutability": "MUTABLE",
                                        "data": {
                                            "media": {
                                                "_id": "tag:aap.com.au:2024:9b4d52f0-9fb1-4f81-933c-1f12527e39a9",
                                                "guid": "tag:aap.com.au:2024:9b4d52f0-9fb1-4f81-933c-1f12527e39a9",
                                                "headline": "QUESTION TIME",
                                                "description_text": "Energy Minister Chris Bowen",
                                                "archive_description": "Australian Energy Minister Chris Bowen",
                                                "source": "AAP Image",
                                                "original_source": "AAP Image/AAP",
                                                "versioncreated": "2024-12-12T21:14:08+0000",
                                                "firstcreated": "2024-11-28T02:52:30+0000",
                                                "pubstatus": "usable",
                                                "type": "picture",
                                                "state": "fetched",
                                                "slugline": "QUESTION TIME",
                                                "byline": "Lukas Coch/AAP PHOTOS",
                                                "ednote": "NO ARCHIVING",
                                                "mimetype": "image/jpeg",
                                                "uri": "20241128153046915660",
                                                "unique_id": 26446441,
                                                "unique_name": "#26446441",
                                                "_current_version": 1,
                                                "expiry": "2024-12-15T21:14:08+0000",
                                                "family_id": "20241128153046915660",
                                                "ingest_id": "20241128153046915660",
                                                "operation": "fetch",
                                                "original_creator": "670465255fa0f76eb5372a22",
                                                "ingest_provider": "59265fbcca6a93a44445ce61",
                                                "format": "HTML",
                                                "event_id": "tag:aap.com.au:2024:87db7ad8-fa93-493c-8c41-d9001db5f1e4",
                                                "priority": 6,
                                                "urgency": 0,
                                                "genre": [
                                                    {
                                                        "qcode": "Article",
                                                        "name": "Article",
                                                    }
                                                ],
                                                "sign_off": "DS",
                                                "language": "en",
                                                "version_creator": "670465255fa0f76eb5372a22",
                                                "_updated": "2024-12-13T00:05:58+0000",
                                                "_etag": "9482955c3a97406430d4893a516cba04f57bdd21",
                                            }
                                        },
                                    },
                                },
                            }
                        ]
                    }
                },
                "firstpublished": "2024-08-19T05:06:30.000+0000",
            }
        )
        article["firstcreated"] = datetime(
            year=2018, month=2, day=15, hour=11, minute=30, second=0, tzinfo=pytz.UTC
        )
        article["firstpublished"] = datetime(
            year=2018, month=2, day=15, hour=12, minute=30, second=0, tzinfo=pytz.UTC
        )
        article["versioncreated"] = datetime(
            year=2018, month=2, day=15, hour=13, minute=45, second=0, tzinfo=pytz.UTC
        )
        article["item_id"] = article["_id"]

        apple_news = self.formatter._format(article)
        self.assertNotIn("<img src=", apple_news["components"][5]["text"])
