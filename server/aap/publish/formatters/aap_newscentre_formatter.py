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
from io import StringIO
import json


class AAPNewscentreFormatter(Formatter, AAPODBCFormatter):
    def format(self, article, subscriber, codes=None):
        """
        Constructs a dictionary that represents the parameters passed to the IPNews InsertNews stored procedure
        :return: returns the sequence number of the subscriber and the constructed parameter dictionary
        """
        try:
            docs = []
            for category in article.get('anpa_category'):
                pub_seq_num, odbc_item = self.get_odbc_item(article, subscriber, category, codes)
                is_last_take = self.is_last_take(article)
                soup = BeautifulSoup(self.append_body_footer(article) if is_last_take else article.get('body_html', ''),
                                     "html.parser")

                if article.get(FORMAT) == FORMATS.PRESERVED:  # @article_text
                    odbc_item['article_text'] = soup.get_text().replace('\'', '\'\'')
                else:
                    text = StringIO()
                    for p in soup.findAll('p'):
                        text.write('   \r\n')
                        ptext = p.get_text('\n')
                        for l in ptext.split('\n'):
                            text.write(l + ' \r\n')
                    body = text.getvalue().replace('\'', '\'\'')
                    if self.is_first_part(article) and 'dateline' in article and 'text' in article.get('dateline', {}):
                        if body.startswith('   \r\n'):
                            body = '   \r\n{} {}'.format(article.get('dateline').get('text').replace('\'', '\'\''),
                                                         body[5:])
                    odbc_item['article_text'] = body

                if self.is_first_part(article):
                    self.add_ednote(odbc_item, article)
                    self.add_embargo(odbc_item, article)

                if not is_last_take:
                    odbc_item['article_text'] += '\r\nMORE'
                else:
                    odbc_item['article_text'] += '\r\n' + article.get('source', '')
                sign_off = article.get('sign_off', '')
                if len(sign_off) > 0:
                    odbc_item['article_text'] += ' ' + sign_off

                odbc_item['category'] = odbc_item.get('category', '').upper()
                odbc_item['selector_codes'] = odbc_item.get('selector_codes', '').upper()

                docs.append((pub_seq_num, json.dumps(odbc_item)))

            return docs
        except Exception as ex:
            raise FormatterError.AAPNewscentreFormatterError(ex, subscriber)

    def can_format(self, format_type, article):
        return format_type == 'AAP NEWSCENTRE' and article[ITEM_TYPE] in [CONTENT_TYPE.TEXT, CONTENT_TYPE.PREFORMATTED]
