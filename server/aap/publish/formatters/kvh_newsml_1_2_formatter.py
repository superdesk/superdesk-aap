# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.publish.formatters.newsml_1_2_formatter import NewsML12Formatter
from lxml.etree import SubElement
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE


class KVHNewsML12Formatter(NewsML12Formatter):

    def _format_descriptive_metadata(self, article, main_news_component):
        """
        Add take key to the  Descriptive_metadata element if available

        :param dict article:
        :param Element main_news_component:
        """
        super()._format_descriptive_metadata(article, main_news_component)
        descriptive_metadata = main_news_component.find('DescriptiveMetadata')
        if descriptive_metadata and 'anpa_take_key' in article and article.get('anpa_take_key'):
            SubElement(descriptive_metadata, 'Property',
                       {'FormalName': 'TakeKey', 'Value': article.get('anpa_take_key', '')})

    def can_format(self, format_type, article):
        """
        Test if the article can be formatted to NewsML 1.2 or not.

        :param str format_type:
        :param dict article:
        :return: True if article can formatted else False
        """
        return format_type == 'kvh_newsml12' and \
            article[ITEM_TYPE] in {CONTENT_TYPE.TEXT, CONTENT_TYPE.PREFORMATTED, CONTENT_TYPE.COMPOSITE,
                                   CONTENT_TYPE.PICTURE, CONTENT_TYPE.VIDEO, CONTENT_TYPE.AUDIO}
