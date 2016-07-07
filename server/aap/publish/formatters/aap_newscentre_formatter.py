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
from bs4 import BeautifulSoup
from superdesk.errors import FormatterError
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
from .aap_odbc_formatter import AAPODBCFormatter
import re
import json
from .unicodetoascii import to_ascii
from copy import deepcopy


class AAPNewscentreFormatter(Formatter, AAPODBCFormatter):
    def format(self, article, subscriber, codes=None):
        """
        Constructs a dictionary that represents the parameters passed to the IPNews InsertNews stored procedure
        :return: returns the sequence number of the subscriber and the constructed parameter dictionary
        """
        try:
            docs = []
            for category in article.get('anpa_category'):
                formatted_article = deepcopy(article)
                pub_seq_num, odbc_item = self.get_odbc_item(formatted_article, subscriber, category, codes)
                is_last_take = self.is_last_take(formatted_article)
                if formatted_article.get(FORMAT) == FORMATS.PRESERVED:  # @article_text
                    soup = BeautifulSoup(self.append_body_footer(formatted_article) if is_last_take else
                                         formatted_article.get('body_html', ''), "html.parser")
                    odbc_item['article_text'] = soup.get_text().replace('\'', '\'\'')
                else:
                    body = self.get_text_content(
                        to_ascii(self.append_body_footer(formatted_article) if is_last_take else
                                 formatted_article.get('body_html', '')))

                    if self.is_first_part(formatted_article) and 'dateline' in formatted_article \
                            and 'text' in formatted_article.get('dateline', {}):
                        if body.startswith('   '):
                            body = '   {} {}'.format(formatted_article.get('dateline').get('text'), body[3:])
                    odbc_item['article_text'] = body.replace('\'', '\'\'')

                if self.is_first_part(formatted_article):
                    self.add_ednote(odbc_item, formatted_article)
                    self.add_embargo(odbc_item, formatted_article)

                if not is_last_take:
                    odbc_item['article_text'] += '\r\nMORE'
                else:
                    odbc_item['article_text'] += '\r\n' + formatted_article.get('source', '')
                sign_off = formatted_article.get('sign_off', '')
                if len(sign_off) > 0:
                    odbc_item['article_text'] += ' ' + sign_off

                odbc_item['category'] = odbc_item.get('category', '').upper()
                odbc_item['selector_codes'] = odbc_item.get('selector_codes', '').upper()

                docs.append((pub_seq_num, json.dumps(odbc_item)))

            return docs
        except Exception as ex:
            raise FormatterError.AAPNewscentreFormatterError(ex, subscriber)

    def get_text_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')

        for top_level_tag in soup.find_all(recursive=False):
            self.format_text_content(top_level_tag)

        return soup.get_text()

    def format_text_content(self, tag):
        for child_tag in tag.find_all():
            if child_tag.name == 'br':
                child_tag.replace_with('\r\n{}'.format(child_tag.get_text()))
            else:
                child_tag.replace_with(' {}'.format(child_tag.get_text()))

        para_text = re.sub(' +', ' ', tag.get_text().strip().replace('\n\n', ' ').replace('\xA0', ' '))
        if para_text != '':
            tag.replace_with('   {}\r\n\r\n'.format(para_text))
        else:
            tag.replace_with('')

    def can_format(self, format_type, article):
        return format_type == 'AAP NEWSCENTRE' and article[ITEM_TYPE] in [CONTENT_TYPE.TEXT, CONTENT_TYPE.PREFORMATTED]
