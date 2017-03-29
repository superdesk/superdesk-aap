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
from datetime import datetime
from flask import current_app as app

from superdesk.io.feed_parsers import FileFeedParser
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
from superdesk.utc import utcnow, utc
from superdesk.io.registry import register_feed_parser, register_feeding_service_error
from superdesk.errors import AlreadyExistsError
from aap.errors import AAPParserError
from superdesk.etree import get_text_word_count


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
                ITEM_TYPE: CONTENT_TYPE.TEXT,
                FORMAT: FORMATS.PRESERVED
            }

            with open(file_path, 'r', encoding='windows-1252') as f:
                data = f.read().replace('\r', '')

            header, dateline_data, data = data.split('\n\n', 2)
            slugline, take_key, headline = header.split('\n', 2)

            slugline = slugline[8:].strip()
            headline = headline.replace('\n', '')

            item['slugline'] = slugline
            item['headline'] = headline
            item['anpa_take_key'] = take_key[14:]
            item['original_source'] = 'AsiaNet'
            item['word_count'] = get_text_word_count(data)

            self._process_dateline(item, dateline_data)

            item['body_html'] = '<pre>' + html.escape(data) + '</pre>'

            return item
        except Exception as e:
            raise AAPParserError.AsiaNetParserError(file_path, e)

    def _process_dateline(self, item, dateline):
        """Process the dateline string to get the individual elements.

        Examples:
        AUSTIN, Texas, Feb. 1, 2017 /PRNewswire-AsiaNet/ --
        LONDON, Feb. 1 /PRNewswire-AsiaNet / --
        NEW YORK, LONDON and BEIJING, Feb. 2, 2017 /PRNewswire-AsiaNet/ --

        :param: dict item: The item where the data will be stored
        :param str dateline: The string from the dateline int file
        """
        item.setdefault('dateline', {})

        # Get the first section of the data:
        # ['AUSTIN, Texas, Feb. 1, 2017', 'PRNewswire-AsiaNet/ --']
        # ['LONDON, Feb. 1', 'PRNewswire-AsiaNet /--']
        # ['NEW YORK, LONDON and Beijing, Feb. 2, 2017', 'PRNewswire-Asianet/ --']
        dateline, source = dateline.split(' /', 1)

        item['dateline']['source'] = source[:-4].strip()
        item['dateline']['text'] = dateline

        # Now split the locations and date:
        # ['AUSTIN, Texas, Feb', '1, 2017']
        # ['LONDON, Feb', '1']
        # ['NEW YORK, LONDON and BEIJING, Feb', '2, 2017']
        data = dateline.split('. ')

        # Attempt to get the day and year
        # If a ValueError is raised, that means there is no year in the dateline
        # So set the year to the current year
        try:
            day, year = data[1].split(', ')
        except ValueError:
            day = data[1]
            year = utcnow().year

        # Split up the data again to get the following:
        # ['AUSTIN', 'Texas', 'Feb]
        # ['LONDON', 'Feb']
        # ['NEW YORK', 'LONDON', 'BEIJING', 'Feb']
        data = data[0].replace(' and', ', ').split(', ')

        month = data[-1]

        date = datetime.strptime('{}-{:02}-{}'.format(month, int(day), year), '%b-%d-%Y').replace(tzinfo=utc)
        item['firstcreated'] = item['versioncreated'] = item['dateline']['date'] = date

        # Attempt to set the city data to the dateline.location key
        cities = app.locators.find_cities()
        for city in data[:-1]:
            located = [c for c in cities if c['city'].lower() == city.lower()]
            if len(located) > 0:
                item['dateline']['located'] = located[0]
                break

        if 'located' not in item['dateline']:
            city = data[:-1][0]
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
