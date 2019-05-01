# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import json
import superdesk
from superdesk.publish.formatters.ninjs_newsroom_formatter import NewsroomNinjsFormatter
from superdesk.utils import json_serialize_datetime_objectId
from superdesk.errors import FormatterError
from copy import deepcopy
from .unicodetoascii import clean_string


class MarketplaceNINJSFormatter(NewsroomNinjsFormatter):
    """Formatter for publishing the market place content to Newsroom.
    It attempts to update stories from Reuters, PA and AP if a newer version/correction is received.

    """
    clean_fields = ('body_html', 'headline', 'description_text', 'description_html')

    def __init__(self):
        self.format_type = 'marketplace ninjs'
        self.can_preview = False
        self.can_export = False

    def _transform_to_ninjs(self, article, subscriber, recursive=True):
        ninjs = super(NewsroomNinjsFormatter, self)._transform_to_ninjs(article, subscriber, recursive)
        for f in self.clean_fields:
            if ninjs.get(f):
                ninjs[f] = clean_string(ninjs.get(f))

        return ninjs

    def _get_ingested(self, article):
        """
        Passed am article it will try to return the article as ingested.
        :param article:
        :return:
        """
        if 'ingest_id' in article:
            return superdesk.get_resource_service('ingest').find_one(req=None, _id=article.get('ingest_id'))
        return None

    def _merge_versions(self, article):
        """
        If possible try to return a version of the article with an updated value in the guid. This value should be
        unique for the story across updates/re-writes and corrections
        :param article:
        :return:
        """
        if article.get('source') == 'Reuters' or article.get('source') == 'REUTERS':
            new_article = deepcopy(article)
            ingested = self._get_ingested(article)
            if ingested:
                # Remove the version from the guid
                new_article['guid'] = ':'.join(ingested.get('guid', '').split(':')[:-1])
                return new_article
        elif article.get('source') == 'PAA' or article.get('source') == 'PA':
            new_article = deepcopy(article)
            ingested = self._get_ingested(article)
            if ingested:
                # Remove the version (send last component from the guid)
                new_article['guid'] = '-'.join(
                    ingested.get('guid', '').split('-')[:-2] + ingested.get('guid', '').split('-')[-1:])
                return new_article
            return new_article
        elif article.get('source') == 'AP':
            # if the string Writethru is not in the take key we assume the story is unique
            if 'Ld-Writethru' not in article.get('anpa_take_key'):
                ingested = self._get_ingested(article)
                if ingested:
                    new_article = deepcopy(article)
                    new_article['guid'] = ingested.get('guid')
                    return new_article
                return article
            # Try to find a the version of the article that is not a Writethru assuming it is the original
            prev = superdesk.get_resource_service('ingest').find(where={'slugline': article.get('slugline'),
                                                                        'headline': article.get('headline'),
                                                                        'anpa_take_key': {
                                                                            '$regex': '^((?!Ld-Writethru).)*$',
                                                                            '$options': 'i'}})
            if prev.count() == 1:
                original = prev.next()
                new_article = deepcopy(article)
                new_article['guid'] = original.get('guid')
                return new_article
        return article

    def format(self, article, subscriber, codes=None):
        try:
            pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)

            ninjs = self._transform_to_ninjs(self._merge_versions(article), subscriber)
            ninjs['extra'] = {'published_id': article.get('_id')}

            return [(pub_seq_num, json.dumps(ninjs, default=json_serialize_datetime_objectId))]
        except Exception as ex:
            raise FormatterError.ninjsFormatterError(ex, subscriber)
