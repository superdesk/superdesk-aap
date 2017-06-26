# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from superdesk.publish.formatters import Formatter
from superdesk.errors import FormatterError
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
from .aap_odbc_formatter import AAPODBCFormatter
import re
import json
from .unicodetoascii import to_ascii
from copy import deepcopy
from .category_list_map import get_aap_category_list
from superdesk.etree import parse_html, etree, get_text


class AAPNewscentreFormatter(Formatter, AAPODBCFormatter):
    def format(self, article, subscriber, codes=None):
        """
        Constructs a dictionary that represents the parameters passed to the IPNews InsertNews stored procedure
        :return: returns the sequence number of the subscriber and the constructed parameter dictionary
        """
        formatted_article = deepcopy(article)
        mapped_source = formatted_article.get('source', '') if formatted_article.get('source', '') != 'NZN' else 'AAP'

        return self.format_for_source(formatted_article, subscriber, mapped_source, codes)

    def format_for_source(self, article, subscriber, source, codes=None):
        try:
            pass_through = article.get('auto_publish', False)
            docs = []
            for category in self._get_category_list(article.get('anpa_category')):
                article['source'] = source
                pub_seq_num, odbc_item = self.get_odbc_item(article, subscriber, category, codes, pass_through)
                if article.get(FORMAT) == FORMATS.PRESERVED:  # @article_text
                    body = get_text(self.append_body_footer(article), content='html')
                    odbc_item['article_text'] = body.replace('\'', '\'\'')
                else:
                    body = self.get_text_content(
                        to_ascii(self.append_body_footer(article)))

                    if 'dateline' in article \
                            and 'text' in article.get('dateline', {}) and not pass_through:
                        if body.startswith('   '):
                            body = '   {} {}'.format(article.get('dateline').get('text'), body[3:])
                    odbc_item['article_text'] = body.replace('\'', '\'\'')

                if not pass_through:
                    self.add_ednote(odbc_item, article)
                    self.add_byline(odbc_item, article)

                odbc_item['article_text'] += '\r\n' + source
                sign_off = article.get('sign_off', '') or ''
                if len(sign_off) > 0:
                    odbc_item['article_text'] += ' ' + sign_off

                odbc_item['category'] = odbc_item.get('category', '').upper()
                odbc_item['selector_codes'] = odbc_item.get('selector_codes', '').upper()

                docs.append((pub_seq_num, json.dumps(odbc_item)))

            return docs
        except Exception as ex:
            raise FormatterError.AAPNewscentreFormatterError(ex, subscriber)

    def add_byline(self, odbc_item, article):
        """
        Add the byline to the article text
        :param odbc_item:
        :param article:
        :return:
        """
        if article.get('byline') and article.get('byline') != '':
            byline = get_text(article.get('byline', ''), content='html')
            if len(byline) >= 3 and byline[:2].upper() != 'BY':
                byline = 'By ' + byline
            byline = '   {}\r\n\r\n'.format(byline).replace('\'', '\'\'')
            odbc_item['article_text'] = byline + odbc_item['article_text']

    def _get_category_list(self, category_list):
        return get_aap_category_list(category_list)

    def get_text_content(self, content):
        text = ''
        content = content.replace('<br>', '<br/>').replace('</br>', '')
        content = re.sub(' +', ' ', re.sub('(?<!\r)\n+', ' ', content).strip())
        content = re.sub('[\x00-\x09\x0b\x0c\x0e-\x1f]', '', content)

        parsed = parse_html(content, content='html')

        for br in parsed.xpath('//br'):
            br.tail = '\r\n' + br.tail if br.tail else '\r\n'
        etree.strip_elements(parsed, 'br', with_tail=False)

        for tag in parsed.xpath('/html/div/child::*'):
            ptext = ''
            for x in tag.itertext():
                ptext += x
            text += self.format_text_content(ptext)

        return text

    def format_text_content(self, para_text):

        if para_text != '':
            para_text = '   {}\r\n\r\n'.format(para_text)
        else:
            para_text = ''
        para_text = para_text.replace('\xA0', ' ')
        return para_text

    def can_format(self, format_type, article):
        return format_type == 'AAP NEWSCENTRE' and article[ITEM_TYPE] in [CONTENT_TYPE.TEXT]
