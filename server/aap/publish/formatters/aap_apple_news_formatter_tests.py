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
from mock import patch, MagicMock


def get_data(resource):
    service_mock = MagicMock()
    service_mock.get = MagicMock()
    service_mock.get.return_value = [
        {
            'state': 'published',
            'firstpublished': datetime(year=2018, month=2, day=15, hour=12, minute=30, second=0, tzinfo=pytz.UTC),
            'item_id': '1'
        },
        {
            'state': 'corrected',
            'versioncreated': datetime(year=2018, month=2, day=15, hour=13, minute=45, second=0, tzinfo=pytz.UTC),
            'item_id': '1'
        }
    ]
    return service_mock


class AAPAppleNewsFormatterTest(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.formatter = AAPAppleNewsFormatter()
        self.app.config['DEFAULT_TIMEZONE'] = 'Australia/Sydney'

    def _get_article(self):
        return {
            'type': 'text',
            'genre': [{'qcode': 'Fact Check'}],
            'format': 'HTML',
            'item_id': '1',
            'firstcreated': datetime(year=2018, month=2, day=15, hour=11, minute=30, second=0, tzinfo=pytz.UTC),
            'firstpublished': datetime(year=2018, month=2, day=15, hour=12, minute=30, second=0, tzinfo=pytz.UTC),
            'versioncreated': datetime(year=2018, month=2, day=15, hour=13, minute=45, second=0, tzinfo=pytz.UTC),
            'abstract': 'This is abstract',
            'body_html': '<p>The Statement</p>'
                         '<p>This is statement first line</p>'
                         '<p>This is statement second line</p>'
                         '<p></p>'
                         '<p>The Analysis</p>'
                         '<p>This is analysis first line</p>'
                         '<p>This is analysis second line</p>'
                         '<p></p>'
                         '<p>The Verdict</p>'
                         '<p>This is verdict first line</p>'
                         '<p>This is verdict second line</p>'
                         '<p></p>'
                         '<p>The References</p>'
                         '<p>1. This is references http://test.com</p>'
                         '<p>2. This is references second line</p>'
                         '<p></p>'

        }

    def test_can_format_fact_check(self):
        self.assertTrue(
            self.formatter.can_format(
                self.formatter.format_type,
                {
                    'type': 'text',
                    'genre': [{'qcode': 'Fact Check'}],
                    'format': 'HTML'
                }
            )
        )

        self.assertFalse(
            self.formatter.can_format(
                self.formatter.format_type,
                {
                    'type': 'text',
                    'genre': [{'qcode': 'Article'}],
                    'format': 'HTML'
                }
            )
        )

    def test_parse_statement(self):
        article = self._get_article()
        self.formatter._parse_content(article)
        self.assertEqual(article.get('_statement'), 'This is statement first line')
        self.assertEqual(article.get('_statement_attribution'), 'This is statement second line')
        self.assertEqual(
            article.get('_analysis'),
            '<p>This is analysis first line</p>'
            '<p>This is analysis second line</p>'
        )
        self.assertEqual(
            article.get('_verdict'),
            '<p>This is verdict first line</p>'
            '<p>This is verdict second line</p>'
        )
        self.assertEqual(
            article.get('_references'),
            '<ol><li>This is references <a href="http://test.com">http://test.com</a></li>'
            '<li>This is references second line</li></ol>'
        )
        self.assertEqual(article.get('_revision_history'), '')

    @patch('aap.publish.formatters.aap_apple_news_formatter.get_resource_service', get_data)
    def test_revision_history(self):
        article = self._get_article()
        self.formatter._set_revision_history(article)
        self.assertEqual(
            article.get('_revision_history'),
            '<ul><li>First published Feb 15, 2018 23:30 AEDT</li>'
            '<li>Revision published Feb 16, 2018 00:45 AEDT</li></ul>'
        )

    def test_format_article_raises_exception_if_abstract_missing(self):
        article = self._get_article()
        article['abstract'] = ''
        with self.assertRaises(Exception) as ex_context:
            self.formatter._format(article)
            self.assertIn('Cannot format the article for Apple News', ex_context.exception)

    def test_format_article_raises_exception_if_statement_missing(self):
        article = self._get_article()
        article['body_html'] = '<p>The Statement</p>'\
                               '<p>This is statement first line</p>' \
                               '<p></p>'\
                               '<p>The Analysis</p>'\
                               '<p>This is analysis first line</p>'\
                               '<p>This is analysis second line</p>'\
                               '<p></p>'\
                               '<p>The Verdict</p>'\
                               '<p>This is verdict first line</p>'\
                               '<p>This is verdict second line</p>'\
                               '<p></p>'\
                               '<p>The References</p>'\
                               '<p>1. This is references http://test.com</p>'\
                               '<p>2. This is references second line</p>'\
                               '<p></p>'
        with self.assertRaises(Exception) as ex_context:
            self.formatter._format(article)
            self.assertIn('Cannot format the article for Apple News', ex_context.exception)

    def test_format_article_raises_exception_if_analysis_missing(self):
        article = self._get_article()
        article['body_html'] = '<p>The Statement</p>'\
                               '<p>This is statement first line</p>'\
                               '<p></p>'\
                               '<p>The Verdict</p>'\
                               '<p>This is verdict first line</p>'\
                               '<p>This is verdict second line</p>'\
                               '<p></p>'\
                               '<p>The References</p>'\
                               '<p>1. This is references http://test.com</p>'\
                               '<p>2. This is references second line</p>'\
                               '<p></p>'
        with self.assertRaises(Exception) as ex_context:
            self.formatter._format(article)
            self.assertIn('Cannot format the article for Apple News', ex_context.exception)

    def test_format_article_raises_exception_if_verdict_missing(self):
        article = self._get_article()
        article['body_html'] = '<p>The Statement</p>'\
                               '<p>This is statement first line</p>' \
                               '<p>This is statement second line</p>' \
                               '<p></p>'\
                               '<p>The Analysis</p>'\
                               '<p>This is analysis first line</p>'\
                               '<p>This is analysis second line</p>'\
                               '<p></p>'\
                               '<p>The References</p>'\
                               '<p>1. This is references http://test.com</p>'\
                               '<p>2. This is references second line</p>'\
                               '<p></p>'
        with self.assertRaises(Exception) as ex_context:
            self.formatter._format(article)
            self.assertIn('Cannot format the article for Apple News', ex_context.exception)

    def test_format_article_raises_exception_if_references_missing(self):
        article = self._get_article()
        article['body_html'] = '<p>The Statement</p>'\
                               '<p>This is statement first line</p>' \
                               '<p>This is statement second line</p>' \
                               '<p></p>'\
                               '<p>The Analysis</p>'\
                               '<p>This is analysis first line</p>'\
                               '<p>This is analysis second line</p>'\
                               '<p></p>'\
                               '<p>The Verdict</p>'\
                               '<p>This is verdict first line</p>'\
                               '<p>This is verdict second line</p>'\
                               '<p></p>'
        with self.assertRaises(Exception) as ex_context:
            self.formatter._format(article)
            self.assertIn('Cannot format the article for Apple News', ex_context.exception)

    def test_format_title(self):
        article = self._get_article()
        apple_news = self.formatter._format(article)
        self.assertEqual(apple_news.get('identifier'), '1')
        self.assertEqual(apple_news.get('title'), 'This is abstract')
        self.assertEqual(apple_news.get('subtitle'), 'This is analysis first line')
        self.assertEqual(apple_news.get('components'),
                         [
                             {
                                 'behaviour': {
                                     'type': 'background_parallax'
                                 },
                                 'components': [{
                                     'anchor': {
                                         'originAnchorPosition': 'bottom',
                                         'targetAnchorPosition': 'bottom'
                                     },
                                     'components': [{
                                         'layout': 'titleLayout',
                                         'role': 'title',
                                         'text': 'This is abstract',
                                         'textStyle': 'titleStyle'
                                     }],
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
                                 }],
                                 'layout': 'fixed_image_header_container',
                                 'role': 'container',
                                 'style': {
                                     'fill': {
                                         'URL': 'bundle://header.jpg',
                                         'type': 'image'
                                     }
                                 }
                             },
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
                                 'text': 'This is statement first line',
                                 'textStyle': 'statementStyle'
                             },
                             {
                                 'layout': 'statementAttributionLayout',
                                 'role': 'body',
                                 'text': 'This is statement second line',
                                 'textStyle': 'statementAttributionStyle'
                             },
                             {
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
                             },
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
                                 'text': '<p>This is analysis first line</p>'
                                         '<p>This is analysis second line</p>',
                                 'textStyle': 'bodyStyle'
                             },
                             {
                                 'animation': {
                                     'preferredStartingPosition': 'left',
                                     'type': 'move_in'
                                 },
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
                                         'text': '<p>This is verdict first line</p>'
                                                 '<p>This is verdict second line</p>',
                                         'textStyle': 'verdictStyle'
                                     }
                                 ],
                                 'layout': 'verdictContainerLayout',
                                 'role': 'container',
                                 'style': {
                                     'backgroundColor': '#e7ebf1'
                                 }
                             },
                             {
                                 'layout': 'subHeaderLayout',
                                 'role': 'heading',
                                 'text': 'The References',
                                 'textStyle': 'subHeaderStyle'
                             },
                             {
                                 'format': 'html',
                                 'layout': 'bodyLayout',
                                 'role': 'body',
                                 'text': '<ol><li>This is references <a href="http://test.com">http://test.com</a>'
                                         '</li><li>This is references second line</li></ol>',
                                 'textStyle': 'bodyStyle'
                             }]
                         )

    def test_format_killed_article(self):
        article = self._get_article()
        article['state'] = 'killed'
        apple_news = self.formatter._format(article)
        self.assertEqual(apple_news.get('title'), 'This article has been removed.')
        self.assertEqual(apple_news.get('subtitle'), 'This article has been removed.')
