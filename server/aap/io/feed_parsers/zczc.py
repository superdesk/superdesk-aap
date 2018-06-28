# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license*.
from superdesk.io.registry import register_feed_parser
from superdesk.io.feed_parsers import FileFeedParser
from superdesk.io.registry import register_feeding_service_error
from superdesk import get_resource_service
from superdesk.errors import AlreadyExistsError
from aap.errors import AAPParserError
from superdesk.io.iptc import subject_codes
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
from superdesk.utc import utcnow
from superdesk.logging import logger
import uuid
import html


class ZCZCFeedParser(FileFeedParser):
    """
    Feed Parser which can parse if the feed is in ZCZC format.

    It is expected that the stories contained in the files will be framed by the strings
    ZCZC

    NNNN

    * the NNNN is optional
    """

    NAME = 'zczc'

    START_OF_MESSAGE = 'ZCZC'
    END_OF_MESSAGE = 'NNNN'

    CATEGORY = '$'
    KEYWORD = ':'
    TAKEKEY = '='
    HEADLINE = '^'
    FORMAT = '*'  # *format "X" text "T" tabular
    SERVICELEVEL = '&'  # &service level - Default A but for results should match category
    IPTC = '+'  # +IPTC Subject Reference Number as defined in the SubjectReference.ini file
    PLACE = '@'
    GENRE = '~'

    # Possible values for format
    TEXT = 'X'
    TABULAR = 'T'

    ITEM_SLUGLINE = 'slugline'
    ITEM_HEADLINE = 'headline'
    ITEM_ANPA_CATEGORY = 'anpa_category'
    ITEM_SUBJECT = 'subject'
    ITEM_TAKE_KEY = 'anpa_take_key'
    ITEM_PLACE = 'place'
    ITEM_GENRE = 'genre'

    header_map = {KEYWORD: ITEM_SLUGLINE, TAKEKEY: ITEM_TAKE_KEY,
                  HEADLINE: ITEM_HEADLINE, SERVICELEVEL: None}

    def can_parse(self, file_path):
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                for line in lines:
                    if self.START_OF_MESSAGE in line:
                        return True
                return False
        except Exception as ex:
            logger.exception(ex)
            return False

    def parse(self, filename, provider=None):
        try:
            item = {}
            self.set_item_defaults(item, provider)

            with open(filename, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                header = False
                body = False
                for line in lines:
                    if self.START_OF_MESSAGE in line and not header:
                        item['guid'] = filename + str(uuid.uuid4())
                        header = True
                        continue
                    if header:
                        if line == '\n':
                            continue
                        if line[0] in self.header_map:
                            if self.header_map[line[0]]:
                                item[self.header_map[line[0]]] = line[1:-1]
                            continue
                        if line[0] == self.CATEGORY:
                            item[self.ITEM_ANPA_CATEGORY] = [{'qcode': line[1]}]
                            continue
                        if line[0] == self.FORMAT:
                            if line[1] == self.TEXT:
                                item[ITEM_TYPE] = CONTENT_TYPE.TEXT
                                continue
                            if line[1] == self.TABULAR:
                                item[FORMAT] = FORMATS.PRESERVED
                                continue
                            continue
                        if line[0] == self.GENRE:
                            genre = line[1:-1]
                            if genre:
                                genre_map = get_resource_service('vocabularies').find_one(req=None, _id='genre')
                                item['genre'] = [x for x in genre_map.get('items', []) if
                                                 x['qcode'] == genre and x['is_active']]
                            continue
                        if line[0] == self.IPTC:
                            iptc_code = line[1:-1]
                            if iptc_code.isdigit():
                                item[self.ITEM_SUBJECT] = [{'qcode': iptc_code, 'name': subject_codes[iptc_code]}]
                            continue
                        header = False
                        body = True
                        item['body_html'] = line
                    else:
                        if self.END_OF_MESSAGE in line:
                            break
                        if body:
                            item['body_html'] = item.get('body_html', '') + line
                if item.get(FORMAT) == FORMATS.PRESERVED:
                    item['body_html'] = '<pre>' + html.escape(item['body_html']) + '</pre>'

            return self.post_process_item(item, provider)

        except Exception as ex:
            raise AAPParserError.ZCZCParserError(exception=ex, provider=provider)

    def set_item_defaults(self, item, provider):
        item['urgency'] = 5
        item['pubstatus'] = 'usable'
        item['versioncreated'] = utcnow()
        item[ITEM_TYPE] = CONTENT_TYPE.TEXT
        item[FORMAT] = FORMATS.HTML

    def post_process_item(self, item, provider):
        """
        Applies the transormations required based on the provider of the content and the item it's self
        :param item:
        :param provider:
        :return: item
        """
        return item


try:
    register_feed_parser(ZCZCFeedParser.NAME, ZCZCFeedParser())
except AlreadyExistsError as ex:
    pass
register_feeding_service_error('file', AAPParserError.ZCZCParserError().get_error_description())
