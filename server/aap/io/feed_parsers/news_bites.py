# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license*.
import datetime
import pytz
from superdesk.io import register_feed_parser
from superdesk.io import register_feeding_service_error
from superdesk.errors import AlreadyExistsError
from aap.errors import AAPParserError
from superdesk.io.feed_parsers import FileFeedParser
from superdesk.logging import logger
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, BYLINE, FORMAT, FORMATS
from superdesk.utc import utcnow
import uuid
import re
from superdesk.io.iptc import subject_codes
from superdesk.etree import get_word_count
import html


class NewsBitesFeedParser(FileFeedParser):
    NAME = 'News Bites'

    START_OF_MESSAGE = 'zczc'

    # Field tags present in the source files
    # 'AN#'
    ORIGINAL_SOURCE = 'KN#'
    PUBLICATION_DATE = 'PD#'
    COMPANY_CODE = 'CO#'
    EXCHANGE = 'SO#'
    # 'SF#'
    BY = 'BY#'
    KEYWORD = 'KY#'
    TITLE = 'TI#'
    ABSTRACT = 'AB#'
    TEXT = 'TX#'

    ITEM_SLUGLINE = 'slugline'
    ITEM_HEADLINE = 'headline'
    ITEM_ANPA_CATEGORY = 'anpa_category'
    ITEM_SUBJECT = 'subject'
    ITEM_ORIGINAL_SOURCE = 'original_source'
    ITEM_VERSION_CREATED = 'versioncreated'
    ITEM_ABSTRACT = 'abstract'
    ITEM_BODY_HTML = 'body_html'

    # Ordered list of tuples (Field tag, mapped to field, group number from the regex call)
    field_list = [('AN#', None, 2), (ORIGINAL_SOURCE, ITEM_ORIGINAL_SOURCE, 3),
                  (PUBLICATION_DATE, ITEM_VERSION_CREATED, 4),
                  (COMPANY_CODE, None, 5), (EXCHANGE, None, 6), ('SF#', None, 7), (BY, BYLINE, 8),
                  (KEYWORD, ITEM_SLUGLINE, 9), (TITLE, ITEM_HEADLINE, 10), (ABSTRACT, ITEM_ABSTRACT, 11),
                  (TEXT, ITEM_BODY_HTML, 12)]

    def can_parse(self, file_path):
        try:
            with open(file_path, 'r', encoding='windows-1252') as f:
                lines = [line for line in f]
                m = re.match(self.START_OF_MESSAGE, lines[0])
                if m.group(0) == self.START_OF_MESSAGE:
                    return True
                return False
        except Exception as ex:
            logger.exception(ex)
            return False

    def parse(self, filename, provider=None):
        try:
            item = {}
            self.set_item_defaults(item, filename)
            with open(filename, 'r', encoding='windows-1252') as f:
                # read the whole file into a single string
                lines = f.read()
                # Construct pattern for the regular expression
                pattern = '(.*)\n'
                for f in self.field_list:
                    pattern = pattern + f[0] + '(.*)\n'
                m = re.match(pattern, ''.join(lines), re.MULTILINE | re.DOTALL)
                if m:
                    for f in self.field_list:
                        if f[1] is not None:
                            item[f[1]] = m.group(f[2])

            # fix the formatting
            item[self.ITEM_VERSION_CREATED] = self.datetime(item[self.ITEM_VERSION_CREATED])
            item[self.ITEM_BODY_HTML] = '<p>' + html.escape(item[self.ITEM_BODY_HTML].strip()).replace('\n', '</p><p>')\
                                        + '</p>'
            item.setdefault('word_count', get_word_count(item['body_html']))

            return item
        except Exception as ex:
            raise AAPParserError.NewsBitesParserError(exception=ex, provider=provider)

    def set_item_defaults(self, item, filename):
        item['guid'] = filename + ':' + str(uuid.uuid4())
        item['urgency'] = 5
        item['pubstatus'] = 'usable'
        item['versioncreated'] = utcnow()
        item[ITEM_TYPE] = CONTENT_TYPE.TEXT
        item['anpa_category'] = [{'qcode': 'f'}]
        item['subject'] = [{'qcode': '04000000', 'name': subject_codes['04000000']}]
        item[FORMAT] = FORMATS.HTML

    def datetime(self, string):
        """
        Convert the date string parsed from the source file to a datetime, assumes that the
        time is local to Sydney Australia
        :param string:
        :return:
        """
        # 06 June 2016 14:00:00
        local_dt = datetime.datetime.strptime(string, '%d %B %Y %H:%M:%S')
        local_tz = pytz.timezone('Australia/Sydney')
        aus_dt = local_tz.localize(local_dt, is_dst=None)
        return aus_dt.astimezone(pytz.utc)


try:
    register_feed_parser(NewsBitesFeedParser.NAME, NewsBitesFeedParser())
except AlreadyExistsError as ex:
    pass
register_feeding_service_error('file', AAPParserError.NewsBitesParserError().get_error_description())
