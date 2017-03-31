# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


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
from superdesk.etree import parse_html, etree, get_text


class AAPIpNewsFormatter(Formatter, AAPODBCFormatter):
    def __init__(self):
        self.format_type = 'AAP IPNEWS'
        self.output_field = 'article_text'
        self.can_preview = True
        self.can_export = True

    def format(self, article, subscriber, codes=None):
        formatted_article = deepcopy(article)
        # Anyhting sourced as NZN is passed off as AAP
        mapped_source = formatted_article.get('source', '') if formatted_article.get('source', '') != 'NZN' else 'AAP'

        return self.format_for_source(formatted_article, subscriber, mapped_source, codes)

    def format_for_source(self, article, subscriber, source, codes=None):
        """Constructs a dictionary that represents the parameters passed to the IPNews InsertNews stored procedure
        :type article: object
        :return: returns the sequence number of the subscriber and the constructed parameter dictionary
        """
        pass_through = article.get('auto_publish', False)
        try:
            docs = []
            for category in self._get_category_list(article.get('anpa_category')):
                # All NZN sourced content is AAP content for the AAP output formatted
                article['source'] = source
                pub_seq_num, odbc_item = self.get_odbc_item(article, subscriber, category, codes, pass_through)
                # determine if this is the last take
                is_last_take = self.is_last_take(article)

                if article.get(FORMAT) == FORMATS.PRESERVED:  # @article_text
                    body = get_text(
                        self.append_body_footer(article) if is_last_take else
                        article.get('body_html', ''), content='html')
                    odbc_item['article_text'] = body.replace('\'', '\'\'')
                    odbc_item['texttab'] = 't'
                elif article.get(FORMAT, FORMATS.HTML) == FORMATS.HTML:
                    body = self.get_wrapped_text_content(
                        to_ascii(self.append_body_footer(article) if is_last_take
                                 else article.get('body_html', ''))).replace('\'', '\'\'')
                    # if this is the first take and we have a dateline inject it
                    if self.is_first_part(article) and 'dateline' in article and 'text' in article.get('dateline', {})\
                            and not pass_through:
                        if body.startswith('   '):
                            body = '   {} {}'.format(article.get('dateline')
                                                     .get('text').replace('\'', '\'\''),
                                                     body[3:])

                    odbc_item['article_text'] = body
                    odbc_item['texttab'] = 'x'

                if self.is_first_part(article) and not pass_through:
                    self.add_ednote(odbc_item, article)
                    self.add_byline(odbc_item, article)

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
        """Get a version of the body text that is wrapped
        :param content:
        :return:
        """
        text = ''
        content = content.replace('<br>', '<br/>').replace('</br>', '')
        # remove control chars except \r and \n
        content = re.sub('[\x00-\x09\x0b\x0c\x0f-\x1f]', '', content)
        # Special case x0e denotes a line break
        content = re.sub('\x0e', '\r\n', content)
        # remove runs of spaces and stray line feeds
        content = re.sub(r' +', ' ', re.sub(r'(?<!\r)\n+', ' ', content).strip())

        parsed = parse_html(content, content='html')

        for br in parsed.xpath('//br'):
            br.tail = '\r\n' + br.tail if br.tail else '\r\n'
        etree.strip_elements(parsed, 'br', with_tail=False)

        for tag in parsed.xpath('//*'):
            if tag.getparent() is not None and tag.getparent().tag == 'body':
                ptext = ''
                for x in tag.itertext():
                    ptext += x
                text += self.format_wrapped_text_content(ptext)

        return text

    def format_wrapped_text_content(self, para_text):
        if para_text is None:
            return ''
        if para_text == '\r\n':
            return '\r\n'

        wrapped_text = ''
        # for each line in the paragraph we may need to wrap
        for line in para_text.split('\n'):
            # Wrap line if to long
            if len(line) > 80:
                line = textwrap.fill(line, 80)
                wrapped_text += line.replace('\n', ' \r\n')
            else:
                wrapped_text += '{}\n'.format(line) if line.endswith('\r') else line

        wrapped_text = wrapped_text.strip()
        # inject the paragarph mark
        if wrapped_text != '':
            text = '   {}\x19\r\n'.format(wrapped_text)
        else:
            text = ''
        text = text.replace('\xA0', ' ')
        return text

    def _get_category_list(self, category_list):
        return get_aap_category_list(category_list)

    def can_format(self, format_type, article):
        return format_type == self.format_type and article[ITEM_TYPE] in [CONTENT_TYPE.TEXT]

    def export(self, item):
        if self.can_format(self.format_type, item):
            sequence, formatted_doc = self.format(item, {'_id': '0'}, None)[0]
            formatted_doc = json.loads(formatted_doc)
            return formatted_doc.get(self.output_field, '').replace('\'\'', '\'')
        else:
            raise Exception()
