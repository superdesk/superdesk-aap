# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
import superdesk
from superdesk.publish.formatters.nitf_formatter import NITFFormatter
from superdesk.errors import FormatterError
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, SIGN_OFF
from lxml import etree as etree
from lxml.etree import SubElement
import re
from .unicodetoascii import to_ascii
from superdesk.etree import parse_html, get_text, to_string


class AAPNITFFormatter(NITFFormatter):

    def format(self, article, subscriber, codes=None):
        try:
            pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)

            nitf = self.get_nitf(article, subscriber, pub_seq_num)
            return [{'published_seq_num': pub_seq_num,
                     'formatted_item': etree.tostring(nitf, encoding='ascii').decode('ascii'),
                    'item_encoding': 'ascii'}]
        except Exception as ex:
            raise FormatterError.nitfFormatterError(ex, subscriber)

    def can_format(self, format_type, article):
        return format_type == 'aap_nitf' and \
            article[ITEM_TYPE] in (CONTENT_TYPE.TEXT, CONTENT_TYPE.PREFORMATTED)

    def _format_meta(self, article, head, destination, pub_seq_num):
        """
        Appends <meta> elements to <head>
        """
        super()._format_meta(article, head, destination, pub_seq_num)

        if 'anpa_category' in article and article['anpa_category'] is not None and len(
                article.get('anpa_category')) > 0:
            SubElement(head, 'meta',
                       {'name': 'anpa-category', 'content': article.get('anpa_category')[0].get('qcode', '')})
        SubElement(head, 'meta', {'name': 'anpa-sequence', 'content': str(pub_seq_num)})
        SubElement(head, 'meta', {'name': 'anpa-keyword', 'content': self.append_legal(article)})
        if article.get('anpa_take_key'):
            SubElement(head, 'meta', {'name': 'anpa-takekey', 'content': article.get('anpa_take_key', '')})

        original_creator = superdesk.get_resource_service('users').find_one(req=None,
                                                                            _id=article.get('original_creator', ''))
        if original_creator:
            SubElement(head, 'meta', {'name': 'aap-original-creator', 'content': original_creator.get('username')})
        version_creator = superdesk.get_resource_service('users').find_one(req=None,
                                                                           _id=article.get('version_creator', ''))
        if version_creator:
            SubElement(head, 'meta', {'name': 'aap-version-creator', 'content': version_creator.get('username')})

        if article.get('task', {}).get('desk') is not None:
            desk = superdesk.get_resource_service('desks').find_one(_id=article.get('task', {}).get('desk'), req=None)
            SubElement(head, 'meta', {'name': 'aap-desk', 'content': desk.get('name', '')})
        if article.get('task', {}).get('stage') is not None:
            stage = superdesk.get_resource_service('stages').find_one(_id=article.get('task', {}).get('stage'),
                                                                      req=None)
            if stage is not None:
                SubElement(head, 'meta', {'name': 'aap-stage', 'content': stage.get('name', '')})

        SubElement(head, 'meta', {'name': 'aap-source', 'content': article.get('source', '')})
        SubElement(head, 'meta', {'name': 'aap-original-source', 'content': article.get('original_source', '')})

        if 'place' in article and article['place'] is not None and len(article.get('place', [])) > 0:
            SubElement(head, 'meta', {'name': 'aap-place', 'content': article.get('place')[0]['qcode']})
        if SIGN_OFF in article:
            SubElement(head, 'meta', {'name': 'aap-signoff', 'content': article.get(SIGN_OFF, '') or ''})

    def _format_meta_priority(self, article, head):
        if 'priority' in article:
            SubElement(head, 'meta', {'name': 'aap-priority', 'content': str(article['priority'])})

    def map_html_to_xml(self, element, html):
        """
        Map the html text tags to xml
        :param element: The xml element to populate
        :param html: the html to parse the text from
        :return:
        """
        html = html.replace('<br>', '<br/>').replace('</br>', '')
        html = re.sub('[\x00-\x09\x0b\x0c\x0e-\x1f]', '', html)
        html = html.replace('\n', ' ')
        html = re.sub(r'\s\s+', ' ', html)
        parsed = parse_html(html, content='html')
        for tag in parsed.xpath('/html/div/child::*'):
            p = etree.Element('p')
            p.text = to_ascii(get_text(to_string(tag, method='html'), content='html'))
            element.append(p)
