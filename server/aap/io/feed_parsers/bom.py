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
from superdesk.errors import AlreadyExistsError
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
from superdesk.io.iptc import subject_codes
from superdesk.utc import utcnow
from superdesk import get_resource_service
from superdesk.errors import ParserError
import uuid
import logging
import re

logger = logging.getLogger(__name__)


class BOMParser(FileFeedParser):
    """
    This parser is to process the Australian Government Bureau of Meteorology
    """
    NAME = 'bom_file'
    label = 'Australian Government Bureau of Meteorology Warnings'

    # Map the third letter of the product code to the city/bureau and the state for the story
    city_code_map = {'Y': {'bureau': 'Melbourne', 'state': 'Antarctica'}, 'W': {'bureau': 'Perth', 'state': 'WA'},
                     'T': {'bureau': 'Hobart', 'state': 'Tas'}, 'S': {'bureau': 'Adelaide', 'state': 'SA'},
                     'N': {'bureau': 'Sydney', 'state': 'NSW'}, 'Q': {'bureau': 'Brisbane', 'state': 'Qld'},
                     'D': {'bureau': 'Darwin', 'state': 'NT'}, 'V': {'bureau': 'Melbourne', 'state': 'Vic'},
                     'A': {'bureau': 'Canberra', 'state': 'ACT'}}

    def can_parse(self, file_path):
        """
        Determines if the parser can likely be able to parse the file.
        :param file_path:
        :return:
        """
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                if len(lines) > 0 and lines[0][:2] == 'ID':
                    return True
                return False
        except Exception as ex:
            print(ex)
            return False

    def set_item_defaults(self, item, filename):
        """
        Set normal defaults in the item
        :param item:
        :param filename:
        :return:
        """
        item['urgency'] = 3
        item['priority'] = 3
        item['pubstatus'] = 'usable'
        item['versioncreated'] = utcnow()
        item[ITEM_TYPE] = CONTENT_TYPE.TEXT
        item[FORMAT] = FORMATS.PRESERVED
        item['guid'] = filename + '-' + str(uuid.uuid4())
        item['anpa_category'] = [{'qcode': 'b'}]
        item['subject'] = [{'qcode': '17005000', 'name': subject_codes['17005000']}]

    def _get_decsription(self, lines, provider):
        """Lookup the bom product to determine the descriptive string, not finding this is a fatal error

        :param lines:
        :param provider:
        :return:
        """
        warning_str = 'Unknown'
        bom_products_map = get_resource_service('vocabularies').find_one(req=None, _id='bom_products')
        product = [x for x in bom_products_map.get('items', []) if x['qcode'] == lines[0].strip() and x['is_active']]
        if len(product) > 0:
            warning_str = product[0].get('name', '')
        else:
            logger.error('No BOM product mapping found for {}'.format(lines[0].strip()))
            raise ParserError.parseMessageError(Exception('No BOM product'), provider, data=lines[0])
        return warning_str

    def _set_slugline(self, item, lines, provider):
        item['slugline'] = 'Weather ' + self._get_decsription(lines, provider)

    def _get_time(self, lines):
        """ Scan each line looking for the time and then the date

        :param lines:
        :return:
        """
        time_str = ''
        date_str = ''
        for line in lines:
            # try to find the time somewhere in each line
            time = re.search(r'(^| )at (.*?)( am | pm |UTC )', line, re.IGNORECASE)
            if time:
                time_str = time.group(2).replace(' ', '') + time.group(3).replace(' ', '')
                # try to find the date on the same line
                date = re.search(
                    r' (\d{1,2}) (January|February|March|April|May|June|July|August|September|October'
                    r'|November|December) (\d{4})', line, re.IGNORECASE)
                if date:
                    date_str = date.group(2) + ' ' + date.group(1)
                return (time_str, date_str)
        return (time_str, date_str)

    def _set_take_key(self, item, lines, time):
        """The anpa take key consists of the city and the issue time

        :param item:
        :param lines:
        :return:
        """
        city_code = lines[0][2:3]
        item['anpa_take_key'] = self.city_code_map.get(city_code, {}).get('bureau', '')

        # Try to match the state in the city map to the locators/place
        locators = get_resource_service('vocabularies').find_one(req=None, _id='locators')
        item['place'] = [x for x in locators.get('items', []) if
                         x['qcode'] == self.city_code_map.get(city_code, {}).get('state', '').upper() and x[
                             'is_active']]

        # Now need to append the issue time
        item['anpa_take_key'] = item['anpa_take_key'] + ' ' + time[0]

    def _set_headline(self, item, lines, time):
        city_code = lines[0][2:3]
        item['headline'] = item['slugline'] + ' ' + self.city_code_map.get(city_code, {}).get('state', '') +\
            ': Issued ' + time[0] + ', ' + time[1]

    def parse(self, filename, provider=None):
        try:
            with open(filename, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                item = {}
                time_date = self._get_time(lines)

                self.set_item_defaults(item, filename)
                self._set_slugline(item, lines, provider)
                self._set_take_key(item, lines, time_date)
                self._set_headline(item, lines, time_date)
                item['body_html'] = '<pre>' + ''.join(lines[1:]) + '</pre>'
            return item
        except Exception as ex:
            logging.exception(ex)


try:
    register_feed_parser(BOMParser.NAME, BOMParser())
except AlreadyExistsError as ex:
    pass
