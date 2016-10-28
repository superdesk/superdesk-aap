# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license*.
from superdesk.io import register_feed_parser
from superdesk.io.feed_parsers import FileFeedParser
from superdesk.errors import AlreadyExistsError
from superdesk.utc import utcnow
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, FORMAT, FORMATS
import logging
import re
import uuid


class PDAResultsParser(FileFeedParser):
    NAME = "PDAResults"

    CityMap = {'NSW': 'Sydney', 'VIC': 'Melbourne', 'QLD': 'Brisbane', 'SA': 'Adelaide', 'WA': 'Perth',
               'TAS': 'Hobart', 'NT': 'Darwin', 'ACT': 'Canberra'}

    def can_parse(self, file_path):
        """
        Determines if the parser can likely be able to parse the file.
        :param file_path:
        :return:
        """
        try:
            with open(file_path, 'rb') as f:
                line = f.read()
                if len(line) > 0:
                    if line[0:1] == b'\x01':
                        return True
                return False
        except Exception:
            return False

    def parse(self, filename, provider=None):
        """
        Attempt to parse the file and return the item
        :param filename:
        :param provider:
        :return:
        """
        try:
            with open(filename, 'rb') as f:
                lines = [line for line in f]
                item = {'guid': filename + '-' + str(uuid.uuid4()), 'urgency': 5, 'pubstatus': 'usable',
                        'versioncreated': utcnow(), ITEM_TYPE: CONTENT_TYPE.TEXT, FORMAT: FORMATS.PRESERVED}
                m = re.match(
                    b'\x01(.*)' +
                    b'\x1f(.*)' +
                    b'\x1f([Y|N])' +
                    b'\x1f([Y|N])' +
                    b'\x1f(.*)' +
                    b'\x1f(Monday|Tuesday|Wednesday|Thursday|Friday)', lines[0], flags=re.I)
                if m:
                    state = m.group(5).decode('ascii')
                    item['slugline'] = m.group(1).decode('ascii') + ' Gallop'
                    item['anpa_take_key'] = ('Result ' if '-' not in m.group(2).decode('ascii') else 'Results ') + \
                        m.group(2).decode('ascii') + ' ' + self.CityMap.get(state, '')
                    correction = m.group(3).decode('ascii')
                    abandoned = m.group(4).decode('ascii')
                    day_of_week = m.group(6).decode('ascii')
                    item['headline'] = item.get('slugline', '') + ' ' + item.get('anpa_take_key', '') + ' ' + \
                        day_of_week

                    # if abandoned then the city string might get shortened
                    if abandoned == 'Y':
                        city = self.CityMap.get(state, '')
                        if state.upper() in set(['NSW', 'TAS', 'NT', 'WA']):
                            city = self.CityMap.get(state, '')[:4]
                        if state.upper() in set(['VIC', 'QLD', 'SA']):
                            city = self.CityMap.get(state, '')[:5]
                        # append the city to the take key
                        item['anpa_take_key'] = ('Result ' if '-' not in m.group(2).decode('ascii') else 'Results ') + \
                            m.group(2).decode('ascii') + ' ' + city
                        item['headline'] = item.get('slugline', '') + ' ' + item.get('anpa_take_key', '') + ' ' + \
                            day_of_week

                    if correction == 'Y':
                        item['headline'] = 'RPTG CRTG ' + item.get('headline', '')
                    else:
                        if abandoned == 'Y':
                            item['anpa_take_key'] = item.get('anpa_take_key', '') + ' ABANDONED'
                            item['headline'] = item.get('headline', '') + ' ABANDONED'

                item['body_html'] = '<pre>' + b'\n'.join(lines[1:]).decode('ascii') + '</pre>'
                # remove the sign off as recieved, it will get put back on when published
                if item.get('body_html', '').find('AAP RESULTS'):
                    item['body_html'] = item.get('body_html', '').replace('AAP RESULTS', '')
                    item['sign_off'] = 'RESULTS'

                item['subject'] = [{'qcode': '15030001'}]
                item['anpa_category'] = [{'qcode': 'r'}]
            return item
        except Exception as ex:
            logging.exception(ex)


try:
    register_feed_parser(PDAResultsParser.NAME, PDAResultsParser())
except AlreadyExistsError as ex:
    pass
