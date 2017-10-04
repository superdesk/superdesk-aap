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
from dateutil.parser import parse as date_parser
from flask import current_app as app

from superdesk.io.feed_parsers import FileFeedParser
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
from superdesk.utc import utc, utcnow
from superdesk.io.registry import register_feed_parser, register_feeding_service_error
from superdesk.errors import AlreadyExistsError
from aap.errors import AAPParserError
from superdesk.text_utils import get_word_count


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

            header, dateline_data, data = data.split('\n\n', 2)

            self._process_header(item, header)
            self._process_dateline(item, dateline_data)

            item['original_source'] = 'AsiaNet'
            item['word_count'] = get_word_count(data)
            item['body_html'] = '<pre>' + html.escape(data) + '</pre>'

            return item
        except Exception as e:
            raise AAPParserError.AsiaNetParserError(file_path, e)

    def _process_header(self, item, header):
        """Process the header of the file, that contains the slugline, take key and headline

        It is possible that the source line is spread across multiple lines, as well as the headline.
        So iterate over them to make sure we get all the data. The only assumption is that media release is only
        1 line in the header

        :param dict item: The item where the data will be stored
        :param str header: The header of the file
        """
        source = 'slugline'
        for line in header.split('\n'):
            if line.lower().startswith('media release'):
                source = 'anpa_take_key'

            if source not in item:
                item[source] = line
            else:
                item[source] += line

            if source == 'anpa_take_key':
                source = 'headline'

        # Clean up the header entries
        item['slugline'] = item['slugline'][8:].replace('\n', '').strip()
        item['anpa_take_key'] = item['anpa_take_key'][14:]
        item['headline'] = item['headline'].replace('\n', '')

    def _process_dateline(self, item, dateline):
        """Process the dateline string to get the individual elements.

        Examples:
        AUSTIN, Texas, Feb. 1, 2017 /PRNewswire-AsiaNet/ --
        LONDON, Feb. 1 /PRNewswire-AsiaNet / --
        NEW YORK, LONDON and BEIJING, Feb. 2, 2017 /PRNewswire-AsiaNet/ --

        :param dict item: The item where the data will be stored
        :param str dateline: The string from the dateline int file
        """
        item.setdefault('dateline', {})
        dateline, source = dateline.split('/', 1)

        date = date_parser(dateline, fuzzy=True).replace(tzinfo=utc)
        item['dateline']['date'] = date

        item['dateline']['source'] = source[:-4].strip()
        item['dateline']['text'] = dateline.strip()

        # Attempt to set the city data to the dateline.location key
        cities = app.locators.find_cities()
        for city in dateline.replace(' and ', ',').split(','):
            located = [c for c in cities if c['city'].lower() == city.strip().lower()]
            if len(located) > 0:
                item['dateline']['located'] = located[0]
                break

        if 'located' not in item['dateline']:
            city = dateline.split(',')[0]
            item['dateline']['located'] = {
                'city_code': city,
                'city': city,
                'tz': 'UTC',
                'dateline': 'city'
            }


try:
    register_feed_parser(AsiaNetFeedParser.NAME, AsiaNetFeedParser())
except AlreadyExistsError as ex:
    pass

register_feeding_service_error('file', AAPParserError.AsiaNetParserError().get_error_description())
