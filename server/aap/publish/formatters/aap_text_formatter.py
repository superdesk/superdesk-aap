# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


from bs4 import BeautifulSoup
from .aap_ipnews_formatter import AAPIpNewsFormatter
from superdesk.errors import FormatterError
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
import json
from .unicodetoascii import to_ascii


class AAPTextFormatter(AAPIpNewsFormatter):
    def __int__(self):
        self.can_preview = True
        self.can_export = True
        self.output_field = 'article_text'

    def format(self, article, subscriber, codes=None):
        try:
            formatted_doc = {}
            formatted_doc['headline'] = BeautifulSoup(article.get('headline', ''), 'html.parser').text
            formatted_doc['headline'] = formatted_doc['headline'].replace('\'', '\'\'').replace('\xA0', ' ')
            formatted_doc['keyword'] = article.get('slugline', '').replace('\'', '\'\'')

            # body formatting
            is_last_take = self.is_last_take(article)
            if article.get(FORMAT) == FORMATS.PRESERVED:
                soup = BeautifulSoup(
                    self.append_body_footer(article) if is_last_take else
                    article.get('body_html', ''),
                    "html.parser")
                formatted_doc['article_text'] = soup.get_text().replace('\'', '\'\'')
            elif article.get(FORMAT, FORMATS.HTML) == FORMATS.HTML:
                body = self.get_wrapped_text_content(
                    to_ascii(self.append_body_footer(article) if is_last_take
                             else article.get('body_html', ''))).replace('\'', '\'\'')
                formatted_doc['article_text'] = body

            self.refine_article_body(formatted_doc, article)

            # Frame the text output according to AAP requirement
            formatted_output = 'KEYWORD: ' + formatted_doc.get('keyword', '') + '\r\n'
            formatted_output += 'HEADLINE: ' + formatted_doc.get('headline', '') + '\r\n'
            formatted_output += '   ' + formatted_doc.get('article_text', '')

            return [(0, json.dumps({'article_text': formatted_output}))]
        except Exception as ex:
            raise FormatterError.AAPTextFormatterError(ex, subscriber)

    def can_format(self, format_type, article):
        return article[ITEM_TYPE] in [CONTENT_TYPE.TEXT]

    def refine_article_body(self, formatted_doc, article):
        body = formatted_doc.get('article_text').lstrip().replace('\r\n', '\r\n   ')

        if 'dateline' in article and 'text' in article.get('dateline', {}):
            if body.startswith('   '):
                body = '{} {} - {}'.format(article.get('dateline').get('text').replace('\'', '\'\'').replace('-', '')
                                           .rstrip(),
                                           article.get('source', ''),
                                           body[3:])

        sign_off = article.get('sign_off', '')
        if len(sign_off) > 0:
            body += '\r\n   ' + article.get('source', '') + ' ' + sign_off

        formatted_doc['article_text'] = body
