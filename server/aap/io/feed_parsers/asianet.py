# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015, 2016, 2017 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import html
import uuid
from superdesk.io.feed_parsers import FileFeedParser
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
from superdesk.utc import utcnow
from superdesk.io.registry import register_feed_parser, register_feeding_service_error
from superdesk.errors import AlreadyExistsError
from aap.errors import AAPParserError
from superdesk.text_utils import get_text_word_count
from aap.publish.formatters.unicodetoascii import to_ascii


class AsiaNetFeedParser(FileFeedParser):
    """
    Feed Parser which can parse if the feed is in AsiaNet format
    """

    NAME = 'asianet'
    label = 'AsiaNet'

    def can_parse(self, file_path):
        try:
            # Only get the first two lines of the file
            with open(file_path, 'r', encoding='windows-1252') as f:
                lines = [f.readline(), f.readline()]
                if lines[0].lower().startswith('source') and lines[1].lower().startswith('media release'):
                    return True

            return False
        except:
            return False

    def parse(self, file_path, provider=None):
        try:
            item = {
                'guid': '{}-{}'.format(file_path, uuid.uuid4()),
                'pubstatus': 'usable',
                'versioncreated': utcnow(),
                ITEM_TYPE: CONTENT_TYPE.TEXT,
                FORMAT: FORMATS.PRESERVED,
            }

            with open(file_path, 'r', encoding='windows-1252') as f:
                data = f.read().replace('\r', '')

            header, dateline_data, body_data = data.split('\n\n', 2)

            self._process_header(item, header)

            start_of_body = 'MEDIA RELEASE '
            source, data = data.split(start_of_body, 1)
            data = start_of_body + data

            item['anpa_category'] = [{'qcode': 'j'}]
            item['original_source'] = 'AsiaNet'
            item['word_count'] = get_text_word_count(data)
            item['body_html'] = '<pre>' + to_ascii(html.escape(data)) + '</pre>'

            return item
        except Exception as e:
            raise AAPParserError.AsiaNetParserError(file_path, e)

    def _truncate_headers(self, item):
        # Truncate the anpa_take_key and headline to the lengths defined on the validators if required
        max_anpa_take_key_len = 24
        if 'anpa_take_key' in item:
            if len(item['anpa_take_key']) > max_anpa_take_key_len:
                item['anpa_take_key'] = item['anpa_take_key'][:max_anpa_take_key_len]

    def _process_header(self, item, header):
        """Process the header of the file, that contains the slugline, take key and headline

        It is possible that the source line is spread across multiple lines.
        So iterate over them to make sure we get all the data. The only assumption is that media release is only
        1 line in the header

        :param dict item: The item where the data will be stored
        :param str header: The header of the file
        """
        source = 'anpa_take_key'
        for line in header.split('\n'):
            if line.lower().startswith('media release'):
                break

            if source not in item:
                item[source] = line
            else:
                item[source] += line

        # Clean up the header entries
        item['anpa_take_key'] = item['anpa_take_key'][8:].replace('\n', '').strip()
        item['headline'] = 'Media Release: ' + item.get('anpa_take_key', '')
        item['slugline'] = 'AAP Medianet'
        self._truncate_headers(item)


try:
    register_feed_parser(AsiaNetFeedParser.NAME, AsiaNetFeedParser())
except AlreadyExistsError:
    pass

register_feeding_service_error('file', AAPParserError.AsiaNetParserError().get_error_description())
