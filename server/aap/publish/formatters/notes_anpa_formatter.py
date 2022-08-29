from .aap_formatter_common import map_priority, get_service_level
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, BYLINE, FORMAT, FORMATS
from .field_mappers.slugline_mapper import SluglineMapper
from eve.utils import config
import datetime
import superdesk
from copy import deepcopy
from .unicodetoascii import to_ascii
from superdesk.etree import parse_html, to_string
from superdesk.text_utils import get_text
from superdesk.utc import utc_to_local
from aap.publish.formatters.anpa_formatter import AAPAnpaFormatter
from superdesk.errors import FormatterError


class NotesAnpaFormatter(AAPAnpaFormatter):

    name = 'Notes ANPA'

    type = 'NOTES ANPA'

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
                self._append_filling_date(anpa, formatted_article)
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
                self._append_footer_time(anpa)

                anpa.append(b'\x04')  # EOT
                anpa.append(b'\x0D\x0A')

                docs.append({'published_seq_num': pub_seq_num, 'encoded_item': b''.join(anpa),
                             'formatted_item': b''.join(anpa).decode('ascii')})

            return docs
        except Exception as ex:
            raise FormatterError.AnpaFormatterError(ex, subscriber)

    def _append_filling_date(self, anpa, formatted_article):
        local_time = utc_to_local(config.DEFAULT_TIMEZONE or 'UTC', formatted_article['_updated'])
        anpa.append(local_time.strftime('%d-%m-%y').encode('ascii'))

    def _append_footer_time(self, anpa):
        anpa.append(datetime.datetime.now().strftime('%m-%d %H%M').encode('ascii'))

    def can_format(self, format_type, article):
        return format_type == 'NOTES ANPA' and article[ITEM_TYPE] in [CONTENT_TYPE.TEXT, CONTENT_TYPE.PREFORMATTED]
