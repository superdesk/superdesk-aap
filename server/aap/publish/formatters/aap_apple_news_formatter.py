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
import re
from datetime import datetime
from copy import deepcopy
from eve.utils import ParsedRequest, config
from superdesk.publish.formatters import Formatter
from superdesk.metadata.item import FORMAT, FORMATS, ITEM_STATE, CONTENT_STATE
from superdesk import get_resource_service
from superdesk.utils import json_serialize_datetime_objectId
from superdesk.utc import utc_to_local
from superdesk.etree import parse_html, to_string
from superdesk.text_utils import get_text
from aap.text_utils import format_text_content
from aap.utils import is_fact_check
from aap.errors import AppleNewsError


logger = logging.getLogger(__name__)


class AAPAppleNewsFormatter(Formatter):
    APPLE_NEWS_VERSION = '1.8'
    URL_REGEX = re.compile(r'(?:(?:https|http)://)[\w/\-?=%.]+\.[\w/\-?=%#@.\+:]+', re.IGNORECASE)

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

    def _format(self, article):
        apple_news = {}
        self._parse_content(article)
        if not article.get('_title') or not article.get('_analysis_first_line') or not article.get('_analysis') \
            or not article.get('_statement') or not article.get('_statement_attribution') or \
                not article.get('_verdict1') or not article.get('_verdict2') or not article.get('_references'):
            missing_fields = {
                'title': True if article.get('_title') else False,
                'subtitle': True if article.get('_analysis_first_line') else False,
                'analysis': True if article.get('_analysis') else False,
                'statement': True if article.get('_statement') else False,
                'statement_attribution': True if article.get('_statement_attribution') else False,
                'verdict1': True if article.get('_verdict1') else False,
                'verdict2': True if article.get('_verdict2') else False,
                'references': True if article.get('_references') else False,
            }

            logger.warning('Failed to parse title for item: {}. '
                           'missing fields: {}'.format(article.get('item_id'), missing_fields))

            raise Exception('Cannot format the article for Apple News. '
                            'Failed to parse the item: {}.'.format(article.get('item_id')))
        self._set_article_document(apple_news, article)
        return apple_news

    def can_format(self, format_type, article):
        """Can format text article that are not preformatted"""
        return format_type == self.format_type and is_fact_check(article) \
            and article.get(FORMAT) == FORMATS.HTML

    def _set_advertising_settings(self, apple_news):
        """Function to set the adversiting settings"""
        apple_news['advertisingSettings'] = {
            'frequency': 5,
            'layout': {
                'margin': {
                    'bottom': 15,
                    'top': 15
                }
            }
        }

    def _is_featuremedia_exists(self, article):
        """Checks if the feature media exists"""
        return True if (article.get('associations') or {}).get('featuremedia') else False

    def _set_language(self, apple_news, article):
        """Set language"""
        apple_news['language'] = article.get('language') or 'en'

    def _set_document_style(self, apple_news):
        """Set document style"""
        apple_news['documentStyle'] = {'backgroundColor': '#FFF'}

    def _set_article_document(self, apple_news, article):
        """Set article document"""
        self._set_language(apple_news, article)
        self._set_metadata(apple_news, article)
        apple_news['identifier'] = article['item_id']
        apple_news['title'] = article.get('_title')
        apple_news['version'] = self.APPLE_NEWS_VERSION
        apple_news['subtitle'] = article.get('_analysis_first_line')
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
            'excerpt': article.get('_title')
        }
        if self._is_featuremedia_exists(article):
            apple_news['metadata']['thumbnailURL'] = 'bundle://header.jpg'

    def _format_datetime(self, article_date, date_format='%Y-%m-%dT%H:%M:%S%z'):
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
                "columnSpan": 6,
                "columnStart": 0,
                "margin": {
                    "bottom": 15,
                    "top": 15
                }
            },
            "claimTagLayout": {
                "columnSpan": 7,
                "columnStart": 0
            },
            "fixed_image_header_container": {
                "columnSpan": 7,
                "columnStart": 0,
                "ignoreDocumentMargin": True,
                "minimumHeight": "45vh"
            },
            "fixed_image_header_section": {
                "ignoreDocumentMargin": True,
                "margin": {
                    "bottom": 0,
                    "top": 40
                }
            },
            "header-top-spacer": {
                "minimumHeight": 30
            },
            "statementAttributionLayout": {
                "margin": {
                    "bottom": 10
                }
            },
            "statementLayout": {
                "contentInset": True,
                "margin": {
                    "bottom": 10,
                    "top": 10
                }
            },
            "subHeaderLayout": {
                "horizontalContentAlignment": "left",
                "margin": {
                    "bottom": 10,
                    "top": 15
                }
            },
            "titleLayout": {
                "columnSpan": 7,
                "columnStart": 0,
                "margin": {
                    "bottom": 15,
                    "top": 5
                }
            },
            "verdictContainerLayout": {
                "contentInset": True,
                "ignoreDocumentMargin": True,
                "margin": {
                    "bottom": 15,
                    "top": 5
                }
            },
            "verdictLayout": {
                "margin": {
                    "bottom": 20
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
                "fontName": "Merriweather-Regular",
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
            "claimTagStyle": {
                "fontName": "Merriweather-Bold",
                "fontSize": 18,
                "lineHeight": 17,
                "textAlignment": "left",
                "textColor": "#FFF",
                "textShadow": {
                    "color": "#000",
                    "offset": {
                        "x": 1,
                        "y": 1
                    },
                    "opacity": 0.5,
                    "radius": 2
                }
            },
            "statementAttributionStyle": {
                "fontName": "Merriweather-Italic",
                "fontSize": 14,
                "hyphenation": False,
                "lineHeight": 22,
                "textAlignment": "right",
                "textColor": "#000"
            },
            "statementStyle": {
                "fontName": "Merriweather-BoldItalic",
                "fontSize": 18,
                "hyphenation": False,
                "lineHeight": 26,
                "textColor": "#FFF"
            },
            "subHeaderStyle": {
                "fontName": "FiraSans-Bold",
                "fontSize": 30,
                "hyphenation": False,
                "lineHeight": 40,
                "textColor": "#063c7f"
            },
            "titleStyle": {
                "fontName": "Merriweather-Black",
                "fontSize": 40,
                "lineHeight": 50,
                "textAlignment": "left",
                "textColor": "#FFF"
            },
            "verdictStyle": {
                "fontName": "Merriweather-Regular",
                "fontSize": 18,
                "lineHeight": 26,
                "textAlignment": "left",
                "textColor": "#000"
            }
        }

    def _set_component(self, apple_news, article):
        components = []
        apple_news['components'] = components
        components.append(self._set_header_component(article))
        components.extend(self._set_statement_component(article))
        components.append({
            'layout': {
                'horizontalContentAlignment': 'right',
                'margin': {
                    'bottom': 5
                },
                'maximumContentWidth': 180
            },
            'role': 'divider',
            'stroke': {
                'color': '#063c7f',
                'style': 'dashed',
                'width': 1
            }
        })
        components.extend(self._set_verdict_component(article, '_verdict1'))
        components.extend(self._set_analysis_component(article))
        components.extend(self._set_verdict_component(article, '_verdict2'))
        components.extend(self._set_references_component(article))
        components.extend(self._set_revision_history_component(article))

    def _set_header_component(self, article):
        header = {
            'behaviour': {'type': 'background_parallax'},
            'layout': 'fixed_image_header_container',
            'role': 'container',
            'style': {
                'fill': {
                    'URL': 'bundle://header.jpg',
                    'type': 'image'
                }
            },
            'components': [
                {
                    'anchor': {
                        'originAnchorPosition': 'bottom',
                        'targetAnchorPosition': 'bottom'
                    },
                    'components': [
                        {
                            "layout": "titleLayout",
                            "role": "title",
                            "text": article.get('_title'),
                            "textStyle": "titleStyle"
                        }
                    ],
                    'layout': 'fixed_image_header_section',
                    'role': 'section',
                    'style': {
                        'fill': {
                            'angle': 180,
                            'colorStops': [
                                {'color': '#00000000'},
                                {'color': '#063c7f'}
                            ],
                            'type': 'linear_gradient'
                        }
                    }
                }
            ]
        }

        if not self._is_featuremedia_exists(article):
            header.pop('style', None)

        return header

    def _set_statement_component(self, article):
        """Set the statement component

        :param dict article:
        """
        if not article.get('_statement'):
            return []

        return [
            {
                'layout': 'subHeaderLayout',
                'role': 'heading',
                'text': 'The Statement',
                'textStyle': 'subHeaderStyle'
            },
            {
                'layout': 'statementLayout',
                'role': 'body',
                'style': {
                    'backgroundColor': '#063c7f'
                },
                'text': article.get('_statement'),
                'textStyle': 'statementStyle'
            },
            {
                'layout': 'statementAttributionLayout',
                'role': 'body',
                'text': article.get('_statement_attribution'),
                'textStyle': 'statementAttributionStyle'
            }
        ]

    def _set_analysis_component(self, article):
        """Set the analysis component

        :param dict article:
        """
        if not article.get('_analysis'):
            return []

        return [
            {
                'layout': 'subHeaderLayout',
                'role': 'heading',
                'text': 'The Analysis',
                'textStyle': 'subHeaderStyle'
            },
            {
                'format': 'html',
                'layout': 'bodyLayout',
                'role': 'body',
                'text': article.get('_analysis'),
                'textStyle': 'bodyStyle'
            }
        ]

    def _set_verdict_component(self, article, field_name):
        """Set the verdict component

        :param dict article:
        """
        if not article.get(field_name):
            return []

        return [
            {
                'components': [
                    {
                        'layout': 'subHeaderLayout',
                        'role': 'heading',
                        'text': 'The Verdict',
                        'textStyle': 'subHeaderStyle'
                    },
                    {
                        'format': 'html',
                        'layout': 'verdictLayout',
                        'role': 'body',
                        'text': article.get(field_name),
                        'textStyle': 'verdictStyle'
                    }
                ],
                'layout': 'verdictContainerLayout',
                'role': 'container',
                'animation': {
                    'type': 'move_in',
                    'preferredStartingPosition': 'left'
                },
                'style': {
                    'backgroundColor': '#e7ebf1'
                }
            }
        ]

    def _set_references_component(self, article):
        """Set the references component

        :param dict article:
        """
        if not article.get('_references'):
            return []

        return [
            {
                "layout": "subHeaderLayout",
                "role": "heading",
                "text": "The References",
                "textStyle": "subHeaderStyle"
            },
            {
                "format": "html",
                "layout": "bodyLayout",
                "role": "body",
                "text": article.get('_references'),
                "textStyle": "bodyStyle"
            }
        ]

    def _set_revision_history_component(self, article):
        """Set the revision history component

        :param dict article:
        """
        if not article.get('_revision_history'):
            return []

        return [
            {
                "layout": "subHeaderLayout",
                "role": "heading",
                "text": "Revision History",
                "textStyle": "subHeaderStyle"
            },
            {
                "format": "html",
                "layout": "bodyLayout",
                "role": "body",
                "text": article.get('_revision_history'),
                "textStyle": "bodyStyle"
            }
        ]

    def _parse_content(self, article):
        """Parse body_html and mapping to fields required for apple news format

        :param article:
        """
        statement_regex = re.compile(r'^The Statement$', re.IGNORECASE)
        analysis_regex = re.compile(r'^The Analysis$', re.IGNORECASE)
        verdict_regex = re.compile(r'^The Verdict$', re.IGNORECASE)
        references_regex = re.compile(r'^The References$', re.IGNORECASE)
        abstract = get_text(article.get('abstract'), content='html').strip()

        article['_title'] = abstract
        body_html = article.get('body_html')
        article['_analysis_first_line'] = ''
        article['_analysis'] = ''
        article['_statement'] = ''
        article['_statement_attribution'] = ''
        article['_verdict1'] = ''
        article['_verdict2'] = ''
        article['_references'] = ''
        article['_revision_history'] = ''

        if article.get(ITEM_STATE) == CONTENT_STATE.KILLED or article.get(ITEM_STATE) == CONTENT_STATE.RECALLED:
            article['_title'] = 'This article has been removed.'
            article['_analysis_first_line'] = 'This article has been removed.'
            article['_analysis'] = 'This article has been removed.'
            article['_statement'] = 'This article has been removed.'
            article['_statement_attribution'] = 'This article has been removed.'
            article['_verdict1'] = 'This article has been removed.'
            article['_verdict2'] = 'This article has been removed.'
            article['_references'] = 'This article has been removed.'
            self._set_revision_history(article)
            return

        parsed_content = parse_html(body_html, content='html')
        statement_found = False
        analysis_found = False
        analysis_first_line = False
        verdict1_found = False
        verdict2_found = False
        references_found = False
        statement_elements = []

        for top_level_tag in parsed_content.xpath('/div/child::*'):
            tag_text = format_text_content(top_level_tag).strip()
            if not tag_text:
                continue

            if not verdict1_found:
                if not statement_found:
                    match = statement_regex.search(tag_text)
                    if match:
                        statement_found = True
                    continue
                else:
                    # statement found
                    match = verdict_regex.search(tag_text)
                    if match:
                        verdict1_found = True
                        if len(statement_elements) > 1:
                            statement_length = len(statement_elements) - 1
                            for i in range(statement_length):
                                article['_statement'] += get_text(
                                    to_string(statement_elements[i], remove_root_div=False),
                                    content='html'
                                ).strip()
                                if statement_length > 1 and i != statement_length - 1:
                                    article['_statement'] += '\r\n'

                            article['_statement_attribution'] = get_text(
                                to_string(statement_elements[-1:][0], remove_root_div=False),
                                content='html'
                            ).strip()
                        elif len(statement_elements) == 1:
                            article['_statement'] = to_string(
                                statement_elements[0],
                                remove_root_div=False
                            )
                        continue

                    statement_elements.append(top_level_tag)
                    continue

            if verdict1_found and not analysis_found:
                match = analysis_regex.search(tag_text)
                if match:
                    analysis_found = True
                else:
                    article['_verdict1'] += to_string(top_level_tag, remove_root_div=False)
                continue

            if analysis_found and not verdict2_found:
                if not analysis_first_line:
                    article['_analysis_first_line'] = tag_text
                    analysis_first_line = True

                match = verdict_regex.search(tag_text)
                if match:
                    verdict2_found = True
                else:
                    article['_analysis'] += to_string(top_level_tag, remove_root_div=False)
                continue

            if verdict2_found and not references_found:
                match = references_regex.search(tag_text)
                if match:
                    references_found = True
                else:
                    article['_verdict2'] += to_string(top_level_tag, remove_root_div=False)
                continue

            if references_found:
                tag_text = re.sub(r'^\d*\s*[.):]?', '', tag_text).strip()

                article['_references'] += '<li>{}</li>'.format(
                    self._format_url_to_anchor_tag(tag_text)
                )

        if len(article['_references']):
            article['_references'] = '<ol>{}</ol>'.format(article['_references'])

        if not article.get('_statement') and article.get('_statement_attribution'):
            # if statement is not as per the format
            article['_statement'] = article.get('_statement_attribution')
            article['_statement_attribution'] = ''

        self._set_revision_history(article)

        # append footer to the analysis section
        if article.get('_analysis') and article.get('body_footer'):
            article['_analysis'] += article.get('body_footer')

    def _format_url_to_anchor_tag(self, tag_text):
        def replacement(match_object):
            value = match_object.group(0)
            if value:
                return '<a href="{0}">{0}</a>'.format(value)
            return ''

        return re.sub(self.URL_REGEX, replacement, tag_text)

    def _set_revision_history(self, article):
        """Get revision history of published article

        :param dict article:
        """
        query = {
            'query': {
                'filtered': {
                    'filter': {
                        'bool': {
                            'must': {
                                'term': {'item_id': article.get('item_id')}
                            }
                        }
                    }
                }
            },
            'sort': [
                {'versioncreated': {'order': 'asc'}}
            ]
        }

        req = ParsedRequest()
        repos = 'published,archived'
        req.args = {'source': json.dumps(query), 'repo': repos, 'aggregations': 0}
        revisions = list(get_resource_service('search').get(req=req, lookup=None))
        revisions_tag = []

        for rev in revisions:
            local_date = utc_to_local(
                config.DEFAULT_TIMEZONE,
                rev.get('firstpublished') if rev.get(ITEM_STATE) == CONTENT_STATE.PUBLISHED
                else rev.get('versioncreated')
            )
            date_string = datetime.strftime(local_date, '%b XXX, %Y %H:%M %Z').replace('XXX', str(local_date.day))
            if rev.get(ITEM_STATE) == CONTENT_STATE.PUBLISHED:
                revisions_tag.append('<li>{} {}</li>'.format('First published', date_string))
            else:
                revision_markup = '{} {}'.format('Revision published', date_string)
                ednote = get_text(rev.get('ednote') or '', content='html').strip()
                if rev.get(ITEM_STATE) == CONTENT_STATE.CORRECTED and ednote:
                    revision_markup += '<br><i>{}</i>'.format(ednote)
                revisions_tag.append('<li>{}</li>'.format(revision_markup))

        article['_revision_history'] = '<ul>{}</ul>' .format(''.join(revisions_tag)) if revisions_tag else ''
