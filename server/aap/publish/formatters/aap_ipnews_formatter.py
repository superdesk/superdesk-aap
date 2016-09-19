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
from .aap_odbc_formatter import AAPODBCFormatter
from .aap_formatter_common import map_priority
from superdesk.publish.formatters import Formatter
from superdesk.errors import FormatterError
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
import json
from .unicodetoascii import to_ascii
from copy import deepcopy
from .category_list_map import get_aap_category_list
from .aap_formatter_common import get_service_level
import re
import textwrap


class AAPIpNewsFormatter(Formatter, AAPODBCFormatter):
    def format(self, article, subscriber, codes=None):
        formatted_article = deepcopy(article)
        # Anyhting sourced as NZN is passed off as AAP
        mapped_source = formatted_article.get('source', '') if formatted_article.get('source', '') != 'NZN' else 'AAP'

        return self.format_for_source(formatted_article, subscriber, mapped_source, codes)

    def format_for_source(self, article, subscriber, source, codes=None):
        """
        Constructs a dictionary that represents the parameters passed to the IPNews InsertNews stored procedure
        :return: returns the sequence number of the subscriber and the constructed parameter dictionary
        """
        try:
            docs = []
            for category in self._get_category_list(article.get('anpa_category')):
                # All NZN sourced content is AAP content for the AAP output formatted
                article['source'] = source
                pub_seq_num, odbc_item = self.get_odbc_item(article, subscriber, category, codes)
                # determine if this is the last take
                is_last_take = self.is_last_take(article)

                if article.get(FORMAT) == FORMATS.PRESERVED:  # @article_text
                    soup = BeautifulSoup(
                        self.append_body_footer(article) if is_last_take else
                        article.get('body_html', ''),
                        "html.parser")
                    odbc_item['article_text'] = soup.get_text().replace('\'', '\'\'')
                    odbc_item['texttab'] = 't'
                elif article.get(FORMAT, FORMATS.HTML) == FORMATS.HTML:
                    body = self.get_wrapped_text_content(
                        to_ascii(self.append_body_footer(article) if is_last_take
                                 else article.get('body_html', ''))).replace('\'', '\'\'')
                    # if this is the first take and we have a dateline inject it
                    if self.is_first_part(article) and 'dateline' in article and 'text' in article.get('dateline', {}):
                        if body.startswith('   '):
                            body = '   {} {}'.format(article.get('dateline')
                                                     .get('text').replace('\'', '\'\''),
                                                     body[3:])

                    odbc_item['article_text'] = body
                    odbc_item['texttab'] = 'x'

                if self.is_first_part(article):
                    self.add_ednote(odbc_item, article)
                    self.add_embargo(odbc_item, article)

                if not is_last_take:
                    odbc_item['article_text'] += '\r\nMORE'
                else:
                    odbc_item['article_text'] += '\r\n' + article.get('source', '')
                sign_off = article.get('sign_off', '') or ''
                if len(sign_off) > 0:
                    odbc_item['article_text'] += ' ' + sign_off

                odbc_item['service_level'] = get_service_level(category, article)  # @service_level
                odbc_item['wordcount'] = article.get('word_count') or 0   # @wordcount
                odbc_item['priority'] = map_priority(article.get('priority'))  # @priority

                docs.append((pub_seq_num, json.dumps(odbc_item)))
            return docs
        except Exception as ex:
            raise FormatterError.AAPIpNewsFormatterError(ex, subscriber)

    def get_wrapped_text_content(self, content):
        """
        get a version of the body text that is warapped
        :param content:
        :return:
        """
        content = content.replace('<br>', '<br/>').replace('</br>', '')
        soup = BeautifulSoup(content, 'html.parser')

        for top_level_tag in soup.find_all(recursive=False):
            self.format_wrapped_text_content(top_level_tag)

        return soup.get_text()

    def format_wrapped_text_content(self, tag):
        for child_tag in tag.find_all():
            if child_tag.name == 'br':
                child_tag.replace_with('\r\n{}'.format(child_tag.get_text()))

        # remove runs os spaces and stray line feeds
        para_text = re.sub(r' +', ' ', re.sub(r'(?<!\r)\n+', ' ', tag.get_text()).strip().replace('\xA0', ' '))
        # remove control chars except \r and \n
        para_text = re.sub('[\x00-\x09\x0b\x0c\x0e-\x1f]', '', para_text)
        if len(para_text) > 80:
            para_text = textwrap.fill(para_text, 80).replace('\n', ' \r\n')
        if para_text != '':
            tag.replace_with('   {}\x19\r\n'.format(para_text))
        else:
            tag.replace_with('')

    def _get_category_list(self, category_list):
        return get_aap_category_list(category_list)

    def can_format(self, format_type, article):
        return format_type == 'AAP IPNEWS' and article[ITEM_TYPE] in [CONTENT_TYPE.TEXT]
