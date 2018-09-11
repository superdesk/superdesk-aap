# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
import re
import superdesk
from superdesk.etree import parse_html, to_string
from superdesk.publish.formatters.nitf_formatter import NITFFormatter
from superdesk.errors import FormatterError
from superdesk.utc import utcnow, utc_to_local
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMATS, FORMAT, BYLINE
from .aap_formatter_common import get_service_level, get_first_anpa_category, \
    get_first_anpa_category_code, get_copyrights_info
from lxml import etree as etree
from lxml.etree import SubElement, strip_elements
from eve.utils import config
from superdesk.text_utils import get_text
from .field_mappers.locator_mapper import LocatorMapper
from .field_mappers.slugline_mapper import SluglineMapper


class IRESSNITFFormatter(NITFFormatter):
    line_ender = b'\x19\x0D\x0A'.decode()
    line_feed = b'\x0D\x0A'.decode()
    line_prefix = '   '
    _message_attrib = {}

    def format(self, article, subscriber, codes=None):
        try:
            pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)
            nitf = self.get_nitf(article, subscriber, pub_seq_num)
            strip_elements(nitf, 'body.end')
            nitf_string = etree.tostring(nitf, encoding='utf-8').decode()
            headers = ['<?xml version=\"1.0\" encoding=\"UTF-8\"?>',
                       '<!-- <!DOCTYPE nitf SYSTEM \"./nitf-3-3.dtd\"> -->']
            return [{
                'published_seq_num': pub_seq_num,
                'formatted_item': '{}\r\n{}'.format("\r\n".join(headers), nitf_string).
                    replace('&#13;\n', self.line_ender)}]
        except Exception as ex:
            raise FormatterError.nitfFormatterError(ex, subscriber)

    def can_format(self, format_type, article):
        return format_type == 'iress_nitf' and \
            article[ITEM_TYPE] in (CONTENT_TYPE.TEXT, CONTENT_TYPE.PREFORMATTED)

    def _format_meta(self, article, head, destination, pub_seq_num):
        """
        Appends <meta> elements to <head>
        """
        category = get_first_anpa_category(article)
        category_code = get_first_anpa_category_code(article)

        SubElement(head, 'meta', {'name': 'anpa-sequence', 'content': str(pub_seq_num).zfill(4)})
        SubElement(head, 'meta', {'name': 'anpa-category', 'content': category_code})

        SubElement(head, 'meta',
                   {
                       'name': 'anpa-service',
                       'content': get_service_level(category, article)
                   })
        # content is marked as <pre>
        SubElement(head, 'meta', {
            'name': 'anpa-format',
            'content': 'x' if FORMATS.HTML == article.get(FORMAT) else 't'
        })

        if article.get('word_count'):
            SubElement(head, 'meta', {'name': 'anpa-wordcount', 'content': str(article.get('word_count')).zfill(4)})

        SubElement(head, 'meta', {'name': 'anpa-keyword', 'content': SluglineMapper().map(article, category_code)})
        if article.get('anpa_take_key'):
            SubElement(head, 'meta', {'name': 'anpa-takekey', 'content': article.get('anpa_take_key', '')})

        self._format_company_codes(article, head)

    def _format_title(self, article, head):
        title = SubElement(head, 'title')
        title.text = LocatorMapper().get_formatted_headline(article, get_first_anpa_category_code(article).upper())

    def _format_meta_priority(self, article, head):
        pass

    def _format_company_codes(self, article, head):
        codes = [company.get('qcode') for company in (article.get('company_codes') or []) if company.get('qcode')]
        if codes:
            SubElement(head, 'meta', {'name': 'asx-codes', 'content': " ".join(codes)})

    def _format_line(self, line_text):
            return '{}{}{}'.format(self.line_prefix, line_text, self.line_feed)

    def _format_body_content(self, article, body_content):
        nitf_body = []

        if article.get('ednote'):
            nitf_body.append(self._format_line(article.get('ednote')))

        if article.get(BYLINE):
            nitf_body.append(self._format_line(get_text(article.get(BYLINE))))

        if article.get(FORMAT) == FORMATS.PRESERVED:
            nitf_body.append(get_text(self.append_body_footer(article), content='html'))
        else:
            body = article.get('body_html', '')
            # we need to inject the dateline
            if article.get('dateline', {}).get('text') and not article.get('auto_publish', False):
                body_html_elem = parse_html(article.get('body_html'))
                ptag = body_html_elem.find('.//p')
                if ptag is not None:
                    ptag.text = article['dateline']['text'] + ' ' + (ptag.text or '')
                    body = to_string(body_html_elem)

            nitf_body.append(self.get_text_content(body))
            if article.get('body_footer'):
                nitf_body.append(self.get_text_content(article.get('body_footer', '')))

        sign_off = '{} {}'.format(article.get('source') or '', (article.get('sign_off') or '')).strip()
        if sign_off:
            nitf_body.append(self._format_line(sign_off))

        SubElement(body_content, 'pre').text = ''.join(nitf_body)

    def get_text_content(self, content):
        content = content.replace('<br>', '<br/>').replace('</br>', '')
        content = re.sub('[\x00-\x09\x0b\x0c\x0e-\x1f]', '', content)
        content = content.replace('\xA0', ' ')

        parsed = parse_html(content, content='html')

        for br in parsed.xpath('//br'):
            br.tail = '\r\n' + br.tail if br.tail else '\r\n'
        etree.strip_elements(parsed, 'br', with_tail=False)

        for tag in parsed.xpath('/html/div/child::*'):
            if tag.tag != 'br' and tag.text is not None and tag.text.strip() != '':
                tag.text = self.line_prefix + re.sub(' +', ' ', re.sub('(?<!\r)\n+', ' ', tag.text))
                tag.tail = '\r\n' + tag.tail if tag.tail else '\r\n'

        para_text = "".join(x for x in parsed.itertext())
        # multiple line breaks to one line break
        para_text = re.sub('[{}]+'.format(self.line_feed), self.line_feed, para_text)
        return para_text

    def _format_head(self, article, head):
        tobject = self._format_tobject(article, head)
        self._format_genre(article, tobject)
        self._format_subjects(article, tobject)
        docdata = SubElement(head, 'docdata')
        self._format_docdata(article, docdata)

    def _format_body_head(self, article, body_head):
        hedline = SubElement(body_head, 'hedline')
        hl1 = SubElement(hedline, 'hl1')
        hl1.text = LocatorMapper().get_formatted_headline(article, get_first_anpa_category_code(article).upper())

    def _format_docdata(self, article, docdata):
        self._format_docdata_doc_id(article, docdata)
        SubElement(docdata, 'urgency', {'ed-urg': str(article.get('urgency', ''))})
        self._format_docdata_date(article, docdata, 'date.issue', 'versioncreated')
        self._format_docdata_date(article, docdata, 'date.release', 'versioncreated')
        copyrights = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='rightsinfo')
        rights = get_copyrights_info(article, copyrights.get('items') or []) or {}

        SubElement(docdata, 'doc.copyright', {
            'year': str((self._get_date(article, 'versioncreated')).year),
            'holder': rights.get('copyrightHolder') or 'Australian Associated Press'
        })

    def _format_docdata_doc_id(self, article, docdata):
        SubElement(docdata, 'doc-id',
                   {'id-string': 'AAP.{}.{}'.format(
                       self._get_date(article, 'versioncreated').strftime('%Y%m%d'),
                       str(article.get('unique_id')))})

    def _format_subjects(self, article, tobject):
        subject = article.get('subject')[0] or {} if article.get('subject') else {}
        if subject:
            SubElement(tobject, 'tobject.subject',
                       {
                           'tobject.subject.refnum': subject.get('qcode', ''),
                           'tobject.subject.ipr': 'IPTC'
                       })

    def _format_tobject(self, article, head):
        category_code = get_first_anpa_category_code(article)
        news_item_type = 'News'
        if category_code:
            if category_code.lower() == 'v':
                news_item_type = 'Advisory'
            else:
                if article.get('priority') == 1:
                    news_item_type = 'Alert'

        return SubElement(head, 'tobject', {'tobject.type': news_item_type})

    def _format_genre(self, article, tobject):
        category_code = get_first_anpa_category_code(article)
        category_map = {
            'j': 'Press Release',
            'c': 'Feature',
            'e': 'Feature'
        }
        genre = category_map.get(category_code.lower())
        if not genre:
            if 'highlights' in (article.get('slugline') or '').lower():
                genre = 'Summary'
            else:
                genre = 'Current'
        SubElement(tobject, 'tobject.property', {'tobject.property.type': genre})

    def _format_newsitem_type(self, article, tobject):
        pass

    def _format_docdata_date(self, article, docdata, tag, field):
        SubElement(docdata, tag, {'norm': self._get_date(article, field).strftime('%Y%m%dT%H%M%S')})

    def _get_date(self, article, field):
        return utc_to_local(config.DEFAULT_TIMEZONE or 'UTC', article.get(field) or utcnow())

    def _format_date_expire(self, article, head):
        pass

    def _format_body_end(self, article, body_end):
        pass
