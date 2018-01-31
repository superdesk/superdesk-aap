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
from superdesk.publish.formatters.newsml_1_2_formatter import NewsML12Formatter
from superdesk.publish.formatters.newsml_g2_formatter import XML_LANG
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, SIGN_OFF, FORMAT, FORMATS
from lxml import etree
from lxml.etree import SubElement
from superdesk.errors import FormatterError
from superdesk.metadata.item import EMBARGO
from apps.archive.common import get_utc_schedule
from flask import current_app as app
from apps.prepopulate.app_initialize import get_filepath
from superdesk import etree as sd_etree
from copy import deepcopy
from superdesk.utc import utcnow


class ReutersNewsML12Formatter(NewsML12Formatter):
    XML_ROOT = '<?xml version="1.0"?><!DOCTYPE NewsML SYSTEM "NewsML_xhtml.dtd">'

    def format(self, article, subscriber, codes=None):
        """
        Create article in NewsML1.2 format

        :param dict article:
        :param dict subscriber:
        :param list codes:
        :return [(int, str)]: return a List of tuples. A tuple consist of
            publish sequence number and formatted article string.
        :raises FormatterError: if the formatter fails to format an article
        """
        try:
            formatted_article = deepcopy(article)
            pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)
            self.now = utcnow()
            self.string_now = self.now.strftime('%Y%m%dT%H%M%S+0000')

            newsml = etree.Element("NewsML", {'Version': '1.2'})
            SubElement(newsml, "Catalog", {
                'Href': 'http://about.reuters.com/newsml/vocabulary/catalog-reuters-3rdParty-master_catalog.xml'})
            news_envelope = SubElement(newsml, "NewsEnvelope")
            news_item = SubElement(newsml, "NewsItem")

            self._format_news_envelope(formatted_article, news_envelope, pub_seq_num)
            self._format_identification(formatted_article, news_item)
            self._format_news_management(formatted_article, news_item)
            self._format_news_component(formatted_article, news_item)

            return [(pub_seq_num, self.XML_ROOT + etree.tostring(newsml).decode('utf-8'))]
        except Exception as ex:
            raise FormatterError.newml12FormatterError(ex, subscriber)

    def _format_news_management(self, formatted_article, news_item):
        """
        Create a NewsManagement element

        :param dict formatted_article:
        :param Element news_item:
        """
        news_management = SubElement(news_item, "NewsManagement")
        SubElement(news_management, 'NewsItemType', {'FormalName': 'News'})
        SubElement(news_management, 'FirstCreated').text = \
            formatted_article['firstcreated'].strftime('%Y%m%dT%H%M%S+0000')
        SubElement(news_management, 'ThisRevisionCreated').text = \
            formatted_article['versioncreated'].strftime('%Y%m%dT%H%M%S+0000')

        if formatted_article.get(EMBARGO):
            SubElement(news_management, 'Status', {'FormalName': 'Embargoed'})
            status_will_change = SubElement(news_management, 'StatusWillChange')
            SubElement(status_will_change, 'FutureStatus', {'FormalName': formatted_article['pubstatus']})
            SubElement(status_will_change, 'DateAndTime').text = \
                get_utc_schedule(formatted_article, EMBARGO).isoformat()
        else:
            SubElement(news_management, 'Status', {'FormalName': formatted_article['pubstatus']})

        if formatted_article.get('urgency'):
            SubElement(news_management, 'Urgency', {'FormalName': str(formatted_article['urgency'])})

        if formatted_article['state'] == 'corrected':
            SubElement(news_management, 'Instruction', {'FormalName': 'Correction'})
        else:
            SubElement(news_management, 'Instruction', {'FormalName': 'Update'})

        SubElement(news_management, 'Property', {'FormalName': 'reuters.3rdPartyStyleGuideVersion', 'Value': '2.1'})
        SubElement(news_management, 'Property',
                   {'FormalName': 'USN', 'Value': 'AAP' + str(formatted_article.get('unique_id')) + 'a'})

    def _format_news_component(self, formatted_article, news_item):
        """
        Create a main NewsComponent element

        :param dict formatted_article:
        :param Element news_item:
        """
        news_component = SubElement(news_item, "NewsComponent",
                                    attrib={XML_LANG: formatted_article.get('language', 'en'),
                                            'Essential': 'no', 'EquivalentsList': 'no',
                                            'Duid': 'NC00001'})
        SubElement(news_component, 'Role', attrib={'FormalName': 'Main'})
        admin_metadata = SubElement(news_component, 'AdministrativeMetadata')
        admin_metadata_provider = SubElement(admin_metadata, 'Provider')
        SubElement(admin_metadata_provider, 'Party', attrib={'FormalName': app.config['ORGANIZATION_NAME']})
        SubElement(SubElement(news_component, 'DescriptiveMetadata'), 'Language',
                   attrib={'Language': formatted_article.get('language', 'en')})
        topic_set = SubElement(news_component, 'TopicSet', attrib={'FormalName': 'MediumImportance'})
        topic_index = 1
        topic = SubElement(topic_set, 'Topic', attrib={'Duid': 'T{num:04d}'.format(num=topic_index)})
        SubElement(topic, 'TopicType', attrib={'FormalName': 'Geography', 'Scheme': 'RTT'})
        SubElement(topic, 'FormalName', attrib={'Scheme': 'N2000'}).text = 'ASIA'
        topic_index += 1
        topic = SubElement(topic_set, 'Topic', attrib={'Duid': 'T{num:04d}'.format(num=topic_index)})
        SubElement(topic, 'TopicType', attrib={'FormalName': 'Geography', 'Scheme': 'RTT'})
        SubElement(topic, 'FormalName', attrib={'Scheme': 'N2000'}).text = 'AU'
        topic_index = self._get_topics(formatted_article, topic_set, topic_index)

        for company in formatted_article.get('company_codes', []):
            topic_index += 1
            topic = SubElement(topic_set, 'Topic', attrib={'Duid': 'T{num:04d}'.format(num=topic_index)})
            SubElement(topic, 'TopicType', attrib={'FormalName': 'Company'})
            SubElement(topic, 'FormalName', attrib={'Scheme': 'cRIC'}).text = company.get('qcode', '') + '.AX'

        main_news_component = SubElement(news_component, "NewsComponent",
                                         attrib={XML_LANG: formatted_article.get('language', 'en'), 'Essential': 'no',
                                                 'EquivalentsList': 'no', 'Duid': 'NC00002'})
        admin_metadata_provider = SubElement(main_news_component, 'Provider')
        SubElement(admin_metadata_provider, 'Party', attrib={'FormalName': app.config['ORGANIZATION_NAME']})
        SubElement(main_news_component, 'Role', attrib={'FormalName': 'MainText'})
        self._format_news_lines(formatted_article, main_news_component)
        self._format_descriptive_metadata(formatted_article, main_news_component, topic_index)
        self._format_body(formatted_article, main_news_component)

    def _get_topics(self, formatted_article, topic_set, topic_index):
        """
        Using the Reuters catalog map the IPTC codes to the Reuters topics

        :param formatted_article:
        :param topic_set:
        :param topic_index:
        :return:
        """
        path = get_filepath('topicset-reuters-3rdParty_news2000.xml')
        tree = etree.parse(str(path))
        for subject in formatted_article.get('subject', []):
            topic = tree.xpath('./NewsItem/TopicSet/Topic/FormalName[text()="iptc:' + subject.get('qcode', '') + '"]')
            if len(topic) == 1:
                thing = str(topic[0].xpath('../TopicType/@FormalName')[0])
                other_thing = topic[0].xpath('../FormalName[@Scheme="N2000"]')[0].text
                topic_index = topic_index + 1
                topic = SubElement(topic_set, 'Topic', attrib={'Duid': 'T{num:04d}'.format(num=topic_index)})
                SubElement(topic, 'TopicType', attrib={'FormalName': thing, 'Scheme': 'RTT'})
                SubElement(topic, 'FormalName', attrib={'Scheme': 'N2000'}).text = other_thing
        return topic_index

    def _format_descriptive_metadata(self, formatted_article, main_news_component, topic_index):
        """
        Create a Descriptive_metadata element

        :param dict formatted_article:
        :param Element main_news_component:
        """
        descriptive_metadata = SubElement(main_news_component, "DescriptiveMetadata")
        if formatted_article.get('source', '') == 'AAP':
            SubElement(descriptive_metadata, 'OfInterestTo', attrib={'Scheme': "ProducrCode", "FormalName": 'AUP'})
            SubElement(descriptive_metadata, 'OfInterestTo', attrib={'Scheme': "ProducrCode", "FormalName": 'AAP'})
        elif formatted_article.get('source', '') == 'NZN':
            SubElement(descriptive_metadata, 'OfInterestTo', attrib={'Scheme': "ProducrCode", "FormalName": 'NZP'})
        category = next((iter((formatted_article.get('anpa_category') or []))), None)
        if category:
            if category.get('qcode').upper() == 'F':
                SubElement(descriptive_metadata, 'OfInterestTo', attrib={'Scheme': "ProducrCode", "FormalName": 'AAPF'})
            elif category.get('qcode').upper() in {'R', 'S', 'T'}:
                SubElement(descriptive_metadata, 'OfInterestTo', attrib={'Scheme': "ProducrCode", "FormalName": 'AAPS'})
            elif category.get('qcode').upper() == 'F':
                SubElement(descriptive_metadata, 'OfInterestTo', attrib={'Scheme': "ProducrCode", "FormalName": 'AAPF'})
            else:
                SubElement(descriptive_metadata, 'OfInterestTo', attrib={'Scheme': "ProducrCode", "FormalName": 'AAPG'})
        for i in range(1, topic_index + 1):
            SubElement(descriptive_metadata, 'TopicOccurrence', attrib={"Topic": '#T{num:04d}'.format(num=i),
                                                                        "Impotance": "Medium"})

    def _format_body(self, formatted_article, main_news_component):
        """
        Create an body text NewsComponent element

        :param dict formatted_article:
        :param Element main_news_component:
        """
        content_item = SubElement(main_news_component, "ContentItem", attrib={'Duid': 'CI00001'})
        SubElement(content_item, 'MediaType', {'FormalName': 'Text'})
        SubElement(content_item, 'Format', {'FormalName': 'XHTML'})
        data_content = SubElement(content_item, 'DataContent')
        html = SubElement(data_content, 'html', attrib={'xmlns': 'http://www.w3.org/1999/xhtml'})
        head = SubElement(html, 'head')
        title = SubElement(head, 'title')
        title.text = formatted_article.get('headline', '')
        body = SubElement(html, 'body')

        if formatted_article.get(FORMAT, FORMATS.HTML) == FORMATS.PRESERVED:
            body.append(etree.fromstring(formatted_article.get('body_html')))
        else:
            if formatted_article.get('byline'):
                body.append(etree.fromstring('<p>' + formatted_article.get('byline', '') + '</p>'))

            root = sd_etree.parse_html(self.append_body_footer(formatted_article), content='html')
            if formatted_article.get('dateline', {}).get('text') and not formatted_article.get('auto_publish', False):
                ptag = root.find('.//p')
                if ptag is not None:
                    ptag.text = formatted_article['dateline']['text'] + ' ' + (ptag.text or '')

            body_html = etree.tostring(root, encoding="unicode")
            body_html = body_html.replace('<p>', '__##br##__')
            body_html = body_html.replace('</p>', '__##br##__')
            body_html = body_html.replace('<br/>', '__##br##__')

            root = sd_etree.parse_html(body_html, content='html')
            body_html = etree.tostring(root, encoding="unicode", method="text")

            body_html = body_html.replace('\n', '__##br##__')
            list_paragraph = body_html.split('__##br##__')
            for p in list_paragraph:
                if p and p.strip():
                    body.append(etree.fromstring('<p>' + p + '</p>'))

            if SIGN_OFF in formatted_article:
                body.append(etree.fromstring(
                    '<p>' + formatted_article.get('source', '') + ' ' + formatted_article.get(SIGN_OFF, '') + '</p>'))

    def _format_news_lines(self, formatted_article, main_news_component):
        """
        Create a NewsLines element

        :param dict article:
        :param Element main_news_component:
        """
        news_lines = SubElement(main_news_component, "NewsLines")
        if formatted_article.get('headline'):
            SubElement(news_lines, 'HeadLine').text = formatted_article.get('headline')
        if formatted_article.get('byline'):
            SubElement(news_lines, 'ByLine').text = formatted_article.get('byline') or ''
        if formatted_article.get('dateline', {}).get('text', ''):
            SubElement(news_lines, 'DateLine').text = formatted_article.get('dateline', {}).get('text', '')
        rights = superdesk.get_resource_service('vocabularies').get_rightsinfo(formatted_article)
        SubElement(news_lines, 'CreditLine').text = rights.get('copyrightholder')
        SubElement(news_lines, 'CopyrightLine').text = rights.get('copyrightnotice', '')

    def can_format(self, format_type, article):
        return format_type == 'reuters_newsml' and article[ITEM_TYPE] == CONTENT_TYPE.TEXT
