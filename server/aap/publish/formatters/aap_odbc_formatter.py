# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from superdesk.io.iptc import subject_codes
from .aap_formatter_common import set_subject
from .field_mappers.locator_mapper import LocatorMapper
from .field_mappers.slugline_mapper import SluglineMapper
import superdesk
from .unicodetoascii import to_ascii
from superdesk.etree import get_text


class AAPODBCFormatter():
    def get_odbc_item(self, article, subscriber, category, codes, pass_through=False):
        """
        Construct an odbc_item with the common key value pairs populated, if pass_through is true then the headline
        original headline is maintained.
        :param article:
        :param subscriber:
        :param category:
        :param codes:
        :param pass_through:
        :return:
        """
        article['headline'] = get_text(article.get('headline', ''), content='html')
        pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)
        odbc_item = dict(originator=article.get('source', None), sequence=pub_seq_num,
                         category=category.get('qcode').lower(),
                         author=get_text(article.get('byline', '') or '', content='html').replace('\'', '\'\''),
                         keyword=SluglineMapper().map(article=article,
                                                      category=category.get('qcode').upper(),
                                                      truncate=True).replace('\'', '\'\'') if not pass_through else
                         (article.get('slugline', '') or '').replace('\'', '\'\''),
                         subject_reference=set_subject(category, article),
                         take_key=(article.get('anpa_take_key', '') or '').replace('\'', '\'\''))
        if 'genre' in article and len(article['genre']) >= 1:
            odbc_item['genre'] = article['genre'][0].get('name', None)
        else:
            odbc_item['genre'] = 'Current'  # @genre
        odbc_item['news_item_type'] = 'News'
        odbc_item['fullStory'] = 1
        odbc_item['ident'] = '0'  # @ident
        odbc_item['selector_codes'] = ' '.join(codes) if codes else ' '

        headline = to_ascii(LocatorMapper().get_formatted_headline(article, category.get('qcode').upper()))
        odbc_item['headline'] = headline.replace('\'', '\'\'').replace('\xA0', ' ')

        self.expand_subject_codes(odbc_item)
        self.set_usn(odbc_item, article)

        return pub_seq_num, odbc_item

    def add_ednote(self, odbc_item, article):
        """
        Add the editorial note if required
        :param odbc_item:
        :param article:
        :return:
        """
        if article.get('ednote'):
            ednote = 'EDS:{}\r\n'.format(article.get('ednote').replace('\'', '\'\''))
            odbc_item['article_text'] = ednote + odbc_item['article_text']

    def add_byline(self, odbc_item, article):
        """
        Add the byline to the article text
        :param odbc_item:
        :param article:
        :return:
        """
        if article.get('byline') and article.get('byline') != '':
            byline = get_text(article.get('byline', ''), content='html')
            if len(byline) >= 3 and byline[:2].upper() != 'BY':
                byline = 'By ' + byline
            byline = '\x19   {}\x19\r\n'.format(byline).replace('\'', '\'\'')
            odbc_item['article_text'] = byline + odbc_item['article_text']

    def expand_subject_codes(self, odbc_item):
        """
        Expands the subject reference to the subject matter and subject detail
        :param odbc_item:
        :return:
        """
        if 'subject_reference' in odbc_item and odbc_item['subject_reference'] is not None \
                and odbc_item['subject_reference'] != '00000000':
            odbc_item['subject'] = subject_codes[odbc_item['subject_reference'][:2] + '000000']
            if odbc_item['subject_reference'][2:5] != '000':
                odbc_item['subject_matter'] = subject_codes[odbc_item['subject_reference'][:5] + '000']
            else:
                odbc_item['subject_matter'] = ''
            if not odbc_item['subject_reference'].endswith('000'):
                odbc_item['subject_detail'] = subject_codes[odbc_item['subject_reference']]
            else:
                odbc_item['subject_detail'] = ''
        else:
            odbc_item['subject_reference'] = '00000000'

    def set_usn(self, odbc_item, article):
        """
        Set the usn (unique story number) in the odbc item
        :param odbc_item:
        :param article:
        :return:
        """
        odbc_item['usn'] = article.get('unique_id', None)  # @usn
