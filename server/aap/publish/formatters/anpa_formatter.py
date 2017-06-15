# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from copy import deepcopy
from superdesk.publish.formatters import Formatter
from .aap_formatter_common import map_priority, get_service_level
import superdesk
from superdesk.errors import FormatterError
import datetime
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, BYLINE, FORMAT, FORMATS
from .field_mappers.locator_mapper import LocatorMapper
from .field_mappers.slugline_mapper import SluglineMapper
from eve.utils import config
from .unicodetoascii import to_ascii
from .category_list_map import get_aap_category_list
import re
from superdesk.etree import parse_html, to_string, etree, get_text


class AAPAnpaFormatter(Formatter):
    def format(self, article, subscriber, codes=None):
        try:
            docs = []
            formatted_article = deepcopy(article)
            for category in self._get_category_list(formatted_article.get('anpa_category')):
                mapped_source = self._get_mapped_source(formatted_article)
                formatted_article[config.ID_FIELD] = formatted_article.get('item_id',
                                                                           formatted_article.get(config.ID_FIELD))
                pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)
                anpa = []

                if codes:
                    anpa.append(b'\x05')
                    anpa.append(' '.join(codes).encode('ascii'))
                    anpa.append(b'\x0D\x0A')

                # start of message header (syn syn soh)
                anpa.append(b'\x16\x16\x01')
                anpa.append(get_service_level(category, formatted_article).encode('ascii'))

                # story number
                anpa.append(str(pub_seq_num).zfill(4).encode('ascii'))

                # field seperator
                anpa.append(b'\x0A')  # -LF
                anpa.append(map_priority(formatted_article.get('priority')).encode('ascii'))
                anpa.append(b'\x20')

                anpa.append(category['qcode'].lower().encode('ascii'))

                anpa.append(b'\x13')
                # format identifier
                if formatted_article.get(FORMAT, FORMATS.HTML) == FORMATS.PRESERVED:
                    anpa.append(b'\x12')
                else:
                    anpa.append(b'\x11')
                anpa.append(b'\x20')

                # keyword
                keyword = 'bc-{}'.format(self.append_legal(article=formatted_article, truncate=True)).replace(' ', '-')
                keyword = keyword[:24] if len(keyword) > 24 else keyword
                anpa.append(keyword.encode('ascii'))
                anpa.append(b'\x20')

                # version field
                anpa.append(b'\x20')

                # reference field
                anpa.append(b'\x20')

                # filing date
                anpa.append('{}-{}'.format(formatted_article['_updated'].strftime('%m'),
                                           formatted_article['_updated'].strftime('%d')).encode('ascii'))
                anpa.append(b'\x20')

                # add the word count
                anpa.append(str(formatted_article.get('word_count', '0000')).zfill(4).encode('ascii'))
                anpa.append(b'\x0D\x0A')

                anpa.append(b'\x02')  # STX

                self._process_headline(anpa, formatted_article, category['qcode'].encode('ascii'))

                keyword = SluglineMapper().map(article=formatted_article, category=category['qcode'].upper(),
                                               truncate=True).encode('ascii', 'ignore')
                anpa.append(keyword)
                take_key = (formatted_article.get('anpa_take_key', '') or '').encode('ascii', 'ignore')
                anpa.append((b'\x20' + take_key) if len(take_key) > 0 else b'')
                anpa.append(b'\x0D\x0A')

                if formatted_article.get('ednote', '') != '':
                    ednote = '{}\r\n'.format(to_ascii(formatted_article.get('ednote')))
                    anpa.append(ednote.encode('ascii', 'replace'))

                if formatted_article.get(BYLINE):
                    anpa.append(get_text(formatted_article.get(BYLINE)).encode('ascii', 'replace'))
                    anpa.append(b'\x0D\x0A')

                if formatted_article.get(FORMAT) == FORMATS.PRESERVED:
                    anpa.append(get_text(self.append_body_footer(formatted_article),
                                         content='html').encode('ascii', 'replace'))
                else:
                    body = to_ascii(formatted_article.get('body_html', ''))
                    # we need to inject the dateline
                    if formatted_article.get('dateline', {}).get('text') and not article.get('auto_publish', False):
                        body_html_elem = parse_html(formatted_article.get('body_html'))
                        ptag = body_html_elem.find('.//p')
                        if ptag is not None:
                            ptag.text = formatted_article['dateline']['text'] + ' ' + (ptag.text or '')
                            body = to_string(body_html_elem)
                    anpa.append(self.get_text_content(body))
                    if formatted_article.get('body_footer'):
                        anpa.append(self.get_text_content(to_ascii(formatted_article.get('body_footer', ''))))

                anpa.append(b'\x0D\x0A')
                anpa.append(mapped_source.encode('ascii'))
                sign_off = (formatted_article.get('sign_off', '') or '').encode('ascii')
                anpa.append((b'\x20' + sign_off) if len(sign_off) > 0 else b'')
                anpa.append(b'\x0D\x0A')

                anpa.append(b'\x03')  # ETX

                # time and date
                anpa.append(datetime.datetime.now().strftime('%d-%m-%y %H-%M-%S').encode('ascii'))

                anpa.append(b'\x04')  # EOT
                anpa.append(b'\x0D\x0A\x0D\x0A\x0D\x0A\x0D\x0A\x0D\x0A\x0D\x0A\x0D\x0A\x0D\x0A')

                docs.append({'published_seq_num': pub_seq_num, 'encoded_item': b''.join(anpa),
                             'formatted_item': b''.join(anpa).decode('ascii')})

            return docs
        except Exception as ex:
            raise FormatterError.AnpaFormatterError(ex, subscriber)

    def get_text_content(self, content):
        content = content.replace('<br>', '<br/>').replace('</br>', '')
        content = re.sub('[\x00-\x09\x0b\x0c\x0e-\x1f]', '', content)
        content = content.replace('\xA0', ' ')

        parsed = parse_html(content, content='html')

        for br in parsed.xpath('//br'):
            br.tail = '\r\n' + br.tail if br.tail else '\r\n'
        etree.strip_elements(parsed, 'br', with_tail=False)

        for tag in parsed.xpath('/html/div/child::*'):
            if tag.tag not in ('br') and tag.text is not None and tag.text.strip() != '':
                tag.text = '   ' + re.sub(' +', ' ', re.sub('(?<!\r)\n+', ' ', tag.text)) if tag.text else ''
                tag.tail = '\r\n' + tag.tail if tag.tail else '\r\n'

        para_text = "".join(x for x in parsed.itertext())
        para_text = para_text.replace('\xA0', ' ')
        return para_text.encode('ascii', 'replace')

    def _process_headline(self, anpa, article, category):
        # prepend the locator to the headline if required
        article['headline'] = get_text(article.get('headline', ''))
        headline = to_ascii(LocatorMapper().get_formatted_headline(article, category.decode('UTF-8').upper()))

        # Set the maximum size to 64 including the sequence number if any
        if len(headline) > 64:
            if article.get('sequence'):
                digits = len(str(article['sequence'])) + 1
                shortened_headline = '{}={}'.format(headline[:-digits][:(64 - digits)], article['sequence'])
                anpa.append(shortened_headline.encode('ascii', 'replace'))
            else:
                anpa.append(headline[:64].encode('ascii', 'replace'))
        else:
            anpa.append(headline.encode('ascii', 'replace'))
        anpa.append(b'\x0D\x0A')

    def _get_category_list(self, category_list):
        return get_aap_category_list(category_list)

    def _get_mapped_source(self, article):
        return article.get('source', '') if article.get('source', '') != 'NZN' else 'AAP'

    def can_format(self, format_type, article):
        return format_type == 'AAP ANPA' and article[ITEM_TYPE] in [CONTENT_TYPE.TEXT, CONTENT_TYPE.PREFORMATTED]
