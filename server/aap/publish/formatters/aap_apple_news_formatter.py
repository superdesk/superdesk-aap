# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
import json
from datetime import datetime
from pytz import timezone
from superdesk.utc import get_date
from copy import deepcopy
from eve.utils import config
import lxml.html as lxml_html
from draftjs_exporter.dom import DOM
from textwrap import dedent
from urllib.parse import urlparse, unquote
from superdesk.publish.formatters import Formatter
from superdesk.metadata.item import FORMAT, FORMATS
from superdesk import get_resource_service
from superdesk.utils import json_serialize_datetime_objectId
from superdesk.utc import utc_to_local
from superdesk.text_utils import get_text
from superdesk.editor_utils import get_content_state_fields, Editor3Content, DraftJSHTMLExporter, render_fragment
from aap.errors import AppleNewsError

logger = logging.getLogger(__name__)


class AAPAppleNewsFormatter(Formatter):
    name = 'AAP Apple News'

    type = 'AAP Apple News'

    APPLE_NEWS_VERSION = '1.8'

    def __init__(self):
        self.format_type = 'AAP Apple News'
        self.can_preview = False
        self.can_export = False

    def format(self, article, subscriber, codes=None):
        try:
            formatted_article = deepcopy(article)
            pub_seq_num = get_resource_service('subscribers').generate_sequence_number(subscriber)
            output = self._format(formatted_article)
            return [(pub_seq_num, json.dumps(output, default=json_serialize_datetime_objectId))]
        except Exception as ex:
            raise AppleNewsError.AppleNewsFormatter(exception=ex)

    def _filter_blocks(self, item, field, bfilter, remove):
        """
        Function to filter the embed blocks for video and audio and also will regenerate the html in a more friendly
        form using the AppleExporter class
        :param item: The article
        :param field: the field to operate on
        :param bfilter: Filter function to determine if the block is to be kept
        :param remove: list of keys to remove
        :return:
        """
        editor = Editor3Content(item, field, True)
        exporter = AppleExporter(editor)
        editor.html_exporter = exporter
        blocks = []
        for block in editor.blocks:
            if bfilter(block, remove):
                blocks.append(block)
        editor.set_blocks(blocks)
        editor.update_item()

    def _not_embed(self, block, remove):
        if block.type.lower() == "atomic":
            bk = [e.key for e in block.entities if e.key in remove]
            if bk:
                return False
        return True

    def _remove_embeds(self, article, remove_keys):
        """
        Removes the nominated embeds from the draftjs state and regenerates the HTML.
        :param article:
        :param remove_keys
        :return:
        """
        to_remove = [k.lstrip("editor_") for k in remove_keys]
        fields = get_content_state_fields(article)
        for field in fields:
            self._filter_blocks(article, field, self._not_embed, to_remove)

        for key in remove_keys:
            article.get("associations", {}).pop(key, None)
            if article.get("refs") is not None:
                article["refs"] = [r for r in article.get("refs", []) if r["key"] != key]

    def _remove_unwanted_embeds(self, article):
        """
        Removes all embeds that are not images/pictures
        :param article:
        :return:
        """
        remove_keys = []

        # can only handle pictures at the moment
        for key, item in (article.get("associations") or {}).items():
            if key.startswith("editor_") and item.get("type") != 'picture':
                remove_keys.append(key)

        self._remove_embeds(article, remove_keys)

    def format_dateline(self, located, current_timestamp):
        """
        Formats dateline to "Location, Month Date Source -"

        :return: formatted dateline string
        """

        dateline_location = "{city_code}"
        dateline_location_format_fields = located.get("dateline", "city")
        dateline_location_format_fields = dateline_location_format_fields.split(",")
        if "country" in dateline_location_format_fields and "state" in dateline_location_format_fields:
            dateline_location = "{city_code}, {state_code}, {country_code}"
        elif "state" in dateline_location_format_fields:
            dateline_location = "{city_code}, {state_code}"
        elif "country" in dateline_location_format_fields:
            dateline_location = "{city_code}, {country_code}"
        dateline_location = dateline_location.format(**located)

        if located.get("tz") and located["tz"] != "UTC":
            current_timestamp = datetime.fromtimestamp(current_timestamp.timestamp(), tz=timezone(located["tz"]))
        else:
            current_timestamp = utc_to_local(config.DEFAULT_TIMEZONE, current_timestamp)
        if current_timestamp.month == 9:
            formatted_date = "Sept {}".format(current_timestamp.strftime("%-d"))
        elif 3 <= current_timestamp.month <= 7:
            formatted_date = current_timestamp.strftime("%B %-d")
        else:
            formatted_date = current_timestamp.strftime("%b %-d")

        return "{location}, {mmmdd} at {hhmmpa}".format(
            location=dateline_location.upper(), mmmdd=formatted_date, hhmmpa=current_timestamp.strftime('%I:%M%p')
        )

    def _format(self, article):
        # Remove any video or audio  embeds since for apple news they must be externally hosted
        self._remove_unwanted_embeds(article)

        apple_news = {}
        self._set_article_document(apple_news, article)

        # Set the associations for the transmitter to be able to get the binaries
        apple_news['associations'] = article.get('associations', {})
        return apple_news

    def can_format(self, format_type, article):
        """Can format text article that are not preformatted"""
        return format_type == self.format_type and article.get(FORMAT) == FORMATS.HTML

    def _set_advertising_settings(self, apple_news):
        """Function to set the advertising settings"""
        apple_news['autoplacement'] = {
            "advertisement": {
                "enabled": True,
                "bannerType": "any",
                "distanceFromMedia": "10vh",
                "frequency": 10,
                "layout": {
                    "margin": 10
                }
            }
        }

    def _is_featuremedia_exists(self, article):
        """Checks if the feature media exists"""
        return True if (article.get('associations') or {}).get('featuremedia') else False

    def _set_language(self, apple_news, article):
        """Set language"""
        apple_news['language'] = 'en-AU' if article.get('language') == 'en' else article.get('language', 'en-AU')

    def _set_document_style(self, apple_news):
        """Set document style"""
        apple_news['documentStyle'] = {'backgroundColor': '#FFF'}

    def _set_article_document(self, apple_news, article):
        """Set article document"""
        self._set_language(apple_news, article)
        self._set_metadata(apple_news, article)
        apple_news['identifier'] = article['item_id']
        apple_news['title'] = article.get('headline')
        apple_news['version'] = self.APPLE_NEWS_VERSION
        self._set_layout(apple_news)
        self._set_advertising_settings(apple_news)
        self._set_component_layouts(apple_news)
        self._set_component_styles(apple_news)
        self._set_component(apple_news, article)

    def _set_metadata(self, apple_news, article):
        """Set metadata"""
        apple_news['metadata'] = {
            'dateCreated': self._format_datetime(article.get('firstcreated')),
            'datePublished': self._format_datetime(article.get('firstpublished')),
            'dateModified': self._format_datetime(article.get('versioncreated')),
            'excerpt': get_text(article.get('abstract', ''), content='html').strip()
        }
        if article.get('byline'):
            apple_news['metadata']['authors'] = [article.get('byline')]
        if self._is_featuremedia_exists(article):
            apple_news['metadata']['thumbnailURL'] = 'bundle://featuremedia'

    def _format_datetime(self, article_date, date_format=None):
        if date_format is None:
            aware_dt = article_date.astimezone()
            return aware_dt.isoformat(timespec='seconds')
        else:
            return datetime.strftime(utc_to_local(config.DEFAULT_TIMEZONE, article_date), date_format)

    def _set_layout(self, apple_news):
        """Set Layout"""
        apple_news['layout'] = {
            'columns': 7,
            'gutter': 20,
            'margin': 50,
            'width': 1024
        }

    def _set_component_layouts(self, apple_news):
        apple_news['componentLayouts'] = {
            "bodyLayout": {
                "columnSpan": 7,
                "columnStart": 0,
                "margin": {
                    "bottom": 15,
                    "top": 15
                }
            },
            "fixed_image_header_container": {
                "columnSpan": 7,
                "columnStart": 0,
                "ignoreDocumentMargin": True,
                "minimumHeight": "45vh"
            },
            "titleLayout": {
                "horizontalContentAlignment": "center",
                "columnSpan": 5,
                "columnStart": 1,
                "margin": {
                    "bottom": 5,
                    "top": 5
                }
            },
            "captionLayout": {
                "horizontalContentAlignment": "left",
                "columnSpan": 7,
                "columnStart": 0,
                "margin": {
                    "bottom": 5,
                    "top": 5
                }
            },
            "BodyCaptionLayout": {
                "horizontalContentAlignment": "left",
                "columnSpan": 5,
                "columnStart": 1,
                "margin": {
                    "bottom": 5,
                    "top": 5
                }
            },
            "bylineLayout": {
                "columnSpan": 5,
                "columnStart": 1,
                "margin": {
                    "bottom": 2,
                    "top": 5
                }
            },
            "dateLineLayout": {
                "columnSpan": 5,
                "columnStart": 1,
                "margin": {
                    "bottom": 5,
                    "top": 2
                }
            }
        }

    def _set_component_styles(self, apple_news):
        apple_news['componentStyles'] = {
            "headerContainerStyle": {
                "backgroundColor": "#000"
            }
        }
        apple_news['componentTextStyles'] = {
            "bodyStyle": {
                "fontName": "HelveticaNeue",
                "fontSize": 16,
                "lineHeight": 26,
                "linkStyle": {
                    "textColor": "#000",
                    "underline": {
                        "color": "#000"
                    }
                },
                "textAlignment": "left",
                "textColor": "#000"
            },
            "bylineStyle": {
                "fontName": "HelveticaNeue-Bold",
                "fontSize": 18,
                "lineHeight": 18,
                "textAlignment": "center",
                "textColor": "#000"
            },
            "dateLineStyle": {
                "fontName": "HelveticaNeue-Bold",
                "fontSize": 18,
                "lineHeight": 18,
                "textAlignment": "center",
                "textColor": "#000"
            },
            "titleStyle": {
                "fontName": "HelveticaNeue-CondensedBlack",
                "fontSize": 40,
                "lineHeight": 50,
                "textAlignment": "center",
                "textColor": "#000"
            },
            "captionStyle": {
                "fontName": "HelveticaNeue-Italic",
                "fontSize": 12,
                "hyphenation": False,
                "lineHeight": 15,
                "textAlignment": "left",
                "textColor": "#000"
            }
        }

    def _set_component(self, apple_news, article):
        components = []
        components.extend(self._set_header_component(article))
        components.extend(self._set_story_component(article))
        apple_news['components'] = components

    def _set_header_component(self, article):
        header = [{
            'behaviour': {'type': 'background_parallax'},
            'layout': 'fixed_image_header_container',
            'role': 'container',
            'style': {
                'fill': {
                    'URL': 'bundle://featuremedia',
                    'type': 'image'
                }
            }
        },
            {
                "layout": "captionLayout",
                "role": "caption",
                "text": "{} - {}".format(
                    article.get('associations', {}).get('featuremedia', {}).get('description_text', ''),
                    article.get('associations', {}).get('featuremedia', {}).get('byline', '')),
                "textStyle": 'captionStyle'
        }
        ]

        if not self._is_featuremedia_exists(article):
            return []

        return header

    def _add_pieces(self, body, pieces, role, embed_url):
        """
        Adds the content so far to the body content, then adds the embed, and clears the pieces
        :param body: the body built so far
        :param pieces: the pieces accumulated
        :param role:
        :param embed_url:
        :return:
        """
        body.extend([{
            'format': 'html',
            'layout': 'bodyLayout',
            'role': 'body',
            'text': ''.join(pieces),
            'textStyle': 'bodyStyle'
        }, {
            "role": role,
            "layout": "bodyLayout",
            "URL": embed_url
        }])
        pieces.clear()
        return

    def generate_article_content(self, article):

        fragments = lxml_html.fragments_fromstring(article.get('body_html', '<p></p>'))
        par_pieces = []
        body_content = []

        for elem in fragments:
            if elem.tag == 'figure':
                key = elem.find('./img').attrib['id']
                body_content.extend([
                    {
                        'format': 'html',
                        'layout': 'bodyLayout',
                        'role': 'body',
                        'text': ''.join(par_pieces),
                        'textStyle': 'bodyStyle'
                    },
                    {
                        'role': 'figure',
                        'URL': 'bundle://{}'.format(key),
                        'identifier': key,
                        'accessibilityCaption': elem.find('./img').attrib['alt'],
                        'caption': elem.find('./figcaption').text,
                        'layout': 'bodyLayout'
                    },
                    {
                        "layout": "BodyCaptionLayout",
                        "role": "caption",
                        "text": elem.find('./figcaption').text,
                        "textStyle": 'captionStyle'
                    }
                ])
                par_pieces.clear()
            elif elem.tag == 'div' and 'embed-block' in elem.attrib.get('class', ''):
                bq = elem.find('./blockquote')
                if bq is not None:
                    if bq.attrib.get('class') == 'twitter-tweet':
                        tweet = bq.find('./a').attrib.get('href', '')
                        if 'twitter' in tweet:
                            self._add_pieces(body_content, par_pieces, "tweet", tweet)
                    elif bq.attrib.get('class') == 'instagram-media':
                        insta_link = bq.attrib.get('data-instgrm-permalink')
                        if insta_link:
                            self._add_pieces(body_content, par_pieces, "instagram", insta_link)
                    elif bq.attrib.get('class') == 'tiktok-embed':
                        tiktok = bq.attrib.get('cite')
                        if tiktok:
                            self._add_pieces(body_content, par_pieces, "tiktok", tiktok)
                else:
                    iframe = elem.find("./iframe")
                    if iframe is not None:
                        src = iframe.attrib.get('src')
                        if src:
                            url = urlparse(src)
                            query = unquote(url.query)
                            if query.startswith('href='):
                                fburl = query[len('href='):]
                                self._add_pieces(body_content, par_pieces, 'facebook_post', fburl)
            else:
                par_pieces.append(render_fragment(elem))
        # Add what is left over
        body_content.append({
            'format': 'html',
            'layout': 'bodyLayout',
            'role': 'body',
            'text': ''.join(par_pieces),
            'textStyle': 'bodyStyle'
        })

        if article.get('body_footer', '') != '':
            body_content.append({
                'format': 'html',
                'layout': 'bodyLayout',
                'role': 'body',
                'text': article.get('body_footer', ''),
                'textStyle': 'bodyStyle'}
            )

        return body_content

    def _set_story_component(self, article):

        article_body = self.generate_article_content(article)

        story_component = [
            {
                "layout": "titleLayout",
                "role": "title",
                "text": article.get('headline'),
                "textStyle": "titleStyle",
                "format": "html"
            },
            {
                'role': 'divider',
                'layout': {
                    'columnStart': 2,
                    'columnSpan': 3,
                    'margin': {
                        'top': 5,
                        'bottom': 5
                    }
                },
                'stroke': {
                    'color': '#063c7f',
                    'style': 'solid',
                    'width': 1
                }
            },
            {
                'role': 'byline',
                'text': 'By {}'.format(article.get('byline')),
                'layout': 'bylineLayout',
                'textStyle': 'bylineStyle'
            },
            {
                'role': 'byline',
                'text': self.format_dateline(article.get('dateline', {}).get('located'),
                                             get_date(article.get('versioncreated'))),
                'layout': 'dateLineLayout',
                'textStyle': 'dateLineStyle'
            }
        ]
        story_component.extend(article_body)
        return story_component


class AppleExporter(DraftJSHTMLExporter):
    """
    Exporter class that manipulates the html to inject the required src for the images and
     also to inject the figcaption
    """

    def render_media(self, props):
        embed_key = next(
            k for k, v in self.content_state["entityMap"].items() if v["data"].get("media") == props["media"]
        )
        media_props = props["media"]
        media_type = media_props.get("type", "picture")

        alt_text = media_props.get("alt_text") or ""
        desc = "{} - {}".format(media_props.get("description_text"), media_props.get('byline'))
        if media_type == "picture":
            src = 'bundle:\\editor_{}'.format(embed_key)

            embed_type = "Image"
            elt = DOM.create_element(
                "img",
                {"src": src, "alt": alt_text, "id": "editor_{}".format(embed_key)},
                props["children"],
            )
        content = DOM.render(elt)

        if desc:
            content += "<figcaption>{}</figcaption>".format(desc)

        # <dummy_tag> is needed for the comments, because a root node is necessary
        # it will be removed during rendering.
        embed = DOM.parse_html(
            dedent(
                """\
            <dummy_tag><!-- EMBED START {embed_type} {{id: "editor_{key}"}} -->
            <figure>{content}</figure>
            <!-- EMBED END {embed_type} {{id: "editor_{key}"}} --></dummy_tag>"""
            ).format(embed_type=embed_type, key=embed_key, content=content)
        )

        return embed
