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
        self.app.config['DEFAULT_TIMEZONE'] = 'Australia/Sydney'

    def _get_article(self):
        return {
            'type': 'text',
            'genre': [{'qcode': 'Article'}],
            'format': 'HTML',
            'item_id': '1',
            'firstcreated': datetime(year=2018, month=2, day=15, hour=11, minute=30, second=0, tzinfo=pytz.UTC),
            'firstpublished': datetime(year=2018, month=2, day=15, hour=12, minute=30, second=0, tzinfo=pytz.UTC),
            'versioncreated': datetime(year=2018, month=2, day=15, hour=13, minute=45, second=0, tzinfo=pytz.UTC),
            'abstract': 'This is abstract',
            'headline': 'Headline of the story',
            'byline': 'John Doe',
            'dateline': {
                "source": "AAP",
                "located": {
                    "city": "Sydney",
                    "dateline": "city",
                    "city_code": "Sydney",
                }
            },
            'body_html': '<p>The Statement</p>'
                         '<p>This is statement first line</p>'
                         '<p>This is statement second line</p>'
                         '<p></p>'
                         '<p>The Verdict</p>'
                         '<p>This is verdict 1 first line</p>'
                         '<p>This is verdict 1 second line</p>'
                         '<p></p>'
                         '<p>The Analysis</p>'
                         '<p>This is analysis first line</p>'
                         '<p>This is analysis second line</p>'
                         '<p></p>'
                         '<p>The Verdict</p>'
                         '<p>This is verdict 2 first line</p>'
                         '<p>This is verdict 2 second line</p>'
                         '<p></p>'
                         '<p>The References</p>'
                         '<p>1. This is references http://test.com</p>'
                         '<p>2. This is references second line</p>'
                         '<p></p>'

        }

    def test_can_format_check(self):
        self.assertTrue(
            self.formatter.can_format(
                self.formatter.format_type,
                {
                    'type': 'text',
                    'genre': [{'qcode': 'Article'}],
                    'format': 'HTML'
                }
            )
        )

    def test_format_title(self):
        article = self._get_article()
        apple_news = self.formatter._format(article)
        self.assertEqual(apple_news.get('identifier'), '1')
        self.assertEqual(apple_news.get('title'), 'Headline of the story')
        self.assertEqual(apple_news.get('components'), [{"layout": "titleLayout",
                                                         "role": "title", "text": "Headline of the story",
                                                         "textStyle": "titleStyle",
                                                         "format": "html"},
                                                        {"role": "divider",
                                                         "layout": {"columnStart": 2, "columnSpan": 3,
                                                                    "margin": {"top": 5, "bottom": 5}},
                                                         "stroke": {"color": "#063c7f", "style": "solid", "width": 1}},
                                                        {"role": "byline", "text": "By John Doe",
                                                         "layout": "bylineLayout",
                                                         "textStyle": "bylineStyle"},
                                                        {"role": "byline", "text": "SYDNEY, Feb 16 at 12:45AM",
                                                         "layout": "dateLineLayout", "textStyle": "dateLineStyle"},
                                                        {"format": "html", "layout": "bodyLayout", "role": "body",
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
                                                         "textStyle": "bodyStyle"}])

    def test_format_article_with_embeds(self):
        article = self._get_article()
        article['associations'] = {'featuremedia': {'description_text': 'Protesters participate in a Halloween themed '
                                                                        'Extinction Rebellion rally in Sydney, '
                                                                        'Thursday, October 31, 2019.'},
                                   'editor_0': {'type': 'video'},
                                   'editor_1': {'type': 'picture'}}
        article['fields_meta'] = {
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
                                "data": {
                                    "MULTIPLE_HIGHLIGHTS": {}
                                }
                            },
                            {
                                "key": "97qeo",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [
                                    {
                                        "offset": 0,
                                        "length": 1,
                                        "key": 0
                                    }
                                ],
                                "data": {}
                            },
                            {
                                "key": "bu6bt",
                                "text": "Second paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {}
                            },
                            {
                                "key": "66lpo",
                                "text": "Third paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {}
                            },
                            {
                                "key": "4sgtb",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [
                                    {
                                        "offset": 0,
                                        "length": 1,
                                        "key": 1
                                    }
                                ],
                                "data": {}
                            },
                            {
                                "key": "9n4jj",
                                "text": "Fourth paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {}
                            },
                            {
                                "key": "1trdb",
                                "text": "Fifth paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {}
                            },
                            {
                                "key": "2jrhi",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [
                                    {
                                        "offset": 0,
                                        "length": 1,
                                        "key": 2
                                    }
                                ],
                                "data": {}
                            },
                            {
                                "key": "d51og",
                                "text": "Sixth paragraph",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {}
                            }
                        ],
                        "entityMap": {
                            "0": {
                                "type": "MEDIA",
                                "mutability": "MUTABLE",
                                "data": {
                                }
                            },
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
                                }
                            },
                            "2": {
                                "type": "EMBED",
                                "mutability": "MUTABLE",
                                "data": {
                                    "data": {
                                        "html": "<blockquote class=\"twitter-tweet\"><p lang=\"en\" dir=\"ltr\">"
                                                "&quot;This is actually my first time to ever enter a competition"
                                                ".&quot;<br><br>Photographer Jialing Cai went diving in the dark to "
                                                "capture her award-winning image of a female paper nautilus, a type "
                                                "of octopus that can grow its own shell.<br><br>Via "
                                                "<a href=\"https://twitter.com/liz?ref_src=twsrc%5Etfw\">"
                                                "@liz</a>: <a href=\"https://t.co/u1rGHr1heD\">"
                                                "https://t.co/u1rGHr1heD</a> <a href=\"https://t.co/SIBTwJfisP\">"
                                                "pic.twitter.com/SIBTwJfisP</a></p>&mdash; "
                                                "Australian Associated Press (AAP) (@AAPNewswire) "
                                                "<a href=\"https://twitter.com/AAPNewswire/status/1\">"
                                                "November 16, 2023</a></blockquote> <script async "
                                                "src=\"https://platform.twitter.com/widgets.js\" charset=\"utf-8\">"
                                                "</script>"
                                    }
                                }
                            }
                        }
                    }
                ]
            }}
        apple_news = self.formatter._format(article)
        self.assertEqual(apple_news['components'][7]['URL'], 'bundle://editor_1')
        self.assertEqual(apple_news['components'][0]['style']['fill']['URL'], 'bundle://featuremedia')
        self.assertEqual(apple_news['components'][10]['URL'], 'https://twitter.com/AAPNewswire/status/1')

    def test_format_article_with_instagram(self):
        article = self._get_article()
        article['fields_meta'] = {
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
                                "data": {
                                    "MULTIPLE_HIGHLIGHTS": {}
                                }
                            },
                            {
                                "key": "ed90t",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [
                                    {
                                        "offset": 0,
                                        "length": 1,
                                        "key": 0
                                    }
                                ],
                                "data": {}
                            },
                            {
                                "key": "30a8e",
                                "text": "",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {}
                            }
                        ],
                        "entityMap": {
                            "0": {
                                "type": "EMBED",
                                "mutability": "MUTABLE",
                                "data": {
                                    "data": {
                                        "html": "<blockquote class=\"instagram-media\" data-instgrm-captioned "
                                                "data-instgrm-permalink=\"https://www.instagram.com/reel/C\" "
                                                "data-instgrm-version=\"14\" style=\" background:#FFF; border:0; "
                                                "border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 "
                                                "rgba(0,0,0,0.15); margin: 1px; max-width:540px; min-width:326px; "
                                                "padding:0; width:99.375%; width:-webkit-calc(100% - 2px); "
                                                "width:calc(100% - 2px);\"></blockquote> "
                                    },
                                    "description": "Test Instagram post"
                                }
                            }
                        }
                    }
                ]
            }
        }
        apple_news = self.formatter._format(article)
        self.assertEqual(apple_news['components'][5]['URL'], "https://www.instagram.com/reel/C")

    def test_format_article_with_facebook(self):
        article = self._get_article()
        article['fields_meta'] = {
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
                                "data": {
                                    "MULTIPLE_HIGHLIGHTS": {}
                                }
                            },
                            {
                                "key": "b0nn5",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [
                                    {
                                        "offset": 0,
                                        "length": 1,
                                        "key": 0
                                    }
                                ],
                                "data": {}
                            },
                            {
                                "key": "1loq9",
                                "text": "Following text",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {}
                            }
                        ],
                        "entityMap": {
                            "0": {
                                "type": "EMBED",
                                "mutability": "MUTABLE",
                                "data": {
                                    "data": {
                                        "html": "<iframe src=\"https://www.facebook.com/plugins/post.php?"
                                                "href=https%3A%2F%2Fwww.facebook.com%2Faapnewswire%2Fposts%2Fpfbid\" "
                                                "width=\"500\" height=\"508\" style=\"border:none;overflow:hidden\" "
                                                "scrolling=\"no\" frameborder=\"0\" allowfullscreen=\"true\" "
                                                "allow=\"autoplay; clipboard-write; encrypted-media; "
                                                "picture-in-picture; web-share\"></iframe>"
                                    },
                                    "description": "Embed description"
                                }
                            }
                        }
                    }
                ]
            }
        }
        apple_news = self.formatter._format(article)
        self.assertEqual(apple_news['components'][5]['URL'], 'https://www.facebook.com/aapnewswire/posts/pfbid')

    def test_format_article_with_tik_tok(self):
        article = self._get_article()
        article['fields_meta'] = {
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
                                "data": {
                                    "MULTIPLE_HIGHLIGHTS": {}
                                }
                            },
                            {
                                "key": "cshfs",
                                "text": " ",
                                "type": "atomic",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [
                                    {
                                        "offset": 0,
                                        "length": 1,
                                        "key": 0
                                    }
                                ],
                                "data": {}
                            },
                            {
                                "key": "7n6o7",
                                "text": "Following text",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {}
                            },
                            {
                                "key": "bsq3s",
                                "text": "",
                                "type": "unstyled",
                                "depth": 0,
                                "inlineStyleRanges": [],
                                "entityRanges": [],
                                "data": {}
                            }
                        ],
                        "entityMap": {
                            "0": {
                                "type": "EMBED",
                                "mutability": "MUTABLE",
                                "data": {
                                    "data": {
                                        "html": "<blockquote class=\"tiktok-embed\" "
                                                "cite=\"https://www.tiktok.com/@dic/video/7\" data-video-id=\"7\" "
                                                "style=\"max-width: 605px;min-width: 325px;\" ></blockquote>"
                                    },
                                    "description": "Tik Toc Test description"
                                }
                            }
                        }
                    }
                ]
            }
        }
        apple_news = self.formatter._format(article)
        self.assertEqual(apple_news['components'][5]['URL'], 'https://www.tiktok.com/@dic/video/7')
