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
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import SubElement
import re
from bs4 import BeautifulSoup
from .unicodetoascii import to_ascii


class AAPNITFFormatter(NITFFormatter):

    def format(self, article, subscriber, codes=None):
        try:
            pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)

            nitf = self.get_nitf(article, subscriber, pub_seq_num)
            return [(pub_seq_num, etree.tostring(nitf, encoding='ascii').decode('ASCII'))]
        except Exception as ex:
            raise FormatterError.nitfFormatterError(ex, subscriber)

    def can_format(self, format_type, article):
        return format_type == 'aap_nitf' and \
            article[ITEM_TYPE] in (CONTENT_TYPE.TEXT, CONTENT_TYPE.PREFORMATTED)

    def _append_meta(self, article, head, destination, pub_seq_num):
        """
        Appends <meta> elements to <head>
        """

        SubElement(head, 'meta', {'name': 'anpa-sequence', 'content': str(pub_seq_num)})
        SubElement(head, 'meta', {'name': 'anpa-keyword', 'content': self.append_legal(article)})
        SubElement(head, 'meta', {'name': 'anpa-takekey', 'content': article.get('anpa_take_key', '')})
        if 'anpa_category' in article and article['anpa_category'] is not None and len(
                article.get('anpa_category')) > 0:
            SubElement(head, 'meta',
                       {'name': 'anpa-category', 'content': article.get('anpa_category')[0].get('qcode', '')})

        self._append_meta_priority(article, head)
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
            SubElement(head, 'meta', {'name': 'aap-signoff', 'content': article.get(SIGN_OFF, '')})

    def map_html_to_xml(self, element, html):
        """
        Map the html text tags to xml
        :param element: The xml element to populate
        :param html: the html to parse the text from
        :return:
        """
        html = html.replace('<br>', '<br/>').replace('</br>', '')
        soup = BeautifulSoup(html, 'html.parser')
        for top_level_tag in soup.find_all(recursive=False):
            para_text = top_level_tag.get_text().strip().replace('\n', ' ')
            para_text = re.sub('[\x00-\x09\x0b\x0c\x0e-\x1f]', '', para_text)
            para_text.sub(' +', ' ', para_text)
            SubElement(element, 'p').text = to_ascii(para_text)
