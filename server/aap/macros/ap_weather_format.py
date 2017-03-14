# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import re
from io import StringIO
from flask import current_app as app
from apps.archive.common import format_dateline_to_locmmmddsrc
from superdesk.utc import get_date
from datetime import datetime
from pytz import timezone
from superdesk.errors import SuperdeskApiError
import superdesk
from superdesk.etree import get_text


def ap_weather_format(item, **kwargs):
    if not item.get('slugline', '').startswith('WEA--GlobalWeather-Ce') or not item.get('source', '') == 'AP':
        raise SuperdeskApiError.badRequestError("Article should be an AP sourced weather table")
    item['slugline'] = 'WORLD WEATHER'

    text = get_text(item['body_html'], content='html')
    lines = text.splitlines()
    if not lines[0] == 'BC-WEA--Global Weather-Celsius,<':
        raise SuperdeskApiError.badRequestError("Table should be in Celsius only")

    # tabular column max lengths are extracted into this list
    columns = []
    # map of the columns to extract and the substitutions to apply to the column
    columnMap = ({'index': 0}, {'index': 1}, {'index': 2},
                 {'index': 3, 'substitute': [('COND', 'CONDITIONS'),
                                             ('pc', 'partly cloudy'), ('clr', 'clear'),
                                             ('cdy', 'cloudy'), ('rn', 'rain'),
                                             ('sn', 'snow')]})
    # story preamble
    preamble = 'Temperatures and conditions in world centres:\r\n'
    output = StringIO()
    output.write(preamble)

    # story is always datelined News York
    city = 'New York City'
    cities = app.locators.find_cities()
    located = [c for c in cities if c['city'].lower() == city.lower()]
    if 'dateline' not in item:
        item['dateline'] = {}
    item['dateline']['located'] = located[0] if len(located) > 0 else {'city_code': city, 'city': city,
                                                                       'tz': 'UTC', 'dateline': 'city'}
    item['dateline']['date'] = datetime.fromtimestamp(get_date(item['firstcreated']).timestamp(),
                                                      tz=timezone(item['dateline']['located']['tz']))
    item['dateline']['source'] = 'AP'
    item['dateline']['text'] = format_dateline_to_locmmmddsrc(item['dateline']['located'],
                                                              get_date(item['firstcreated']),
                                                              source=item.get('original_source', 'AP'))

    item['headline'] = 'World Weather for ' + item['dateline']['date'].strftime('%b %-d')

    item['subject'] = [{"name": "weather", "qcode": "17000000"}]
    locator_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='locators')
    item['place'] = [x for x in locator_map.get('items', []) if x['qcode'] == 'US']

    if lines:
        # scan all the lines in the file for potential collimated lines and calculate the length
        # of the column
        for line in lines:
            row = re.split('[;\<]+', line)
            # only consider it if there are more than two rows
            if len(row) > 2:
                index = 0
                for col in row:
                    # check if the column is mapped
                    map = [me for me in columnMap if me['index'] == index]
                    if len(map):
                        for sub in map[0].get('substitute', ()):
                            col = col.replace(sub[0], sub[1])
                    # if it's a new column
                    if 0 <= index < len(columns):
                        # check the length
                        if len(col) > columns[index]:
                            columns[index] = len(col)
                    else:
                        columns.append(len(col))
                    index += 1

        for line in lines:
            row = re.split('[;\<]+', line)
            if len(row) > 2:
                index = 0
                for col in row:
                    map = [me for me in columnMap if me['index'] == index]
                    if len(map) > 0:
                        for sub in map[0].get('substitute', ()):
                            col = col.replace(sub[0], sub[1])
                        output.write(
                            '{}'.format(col.lstrip('\t').ljust(columns[map[0].get('index')] + 2)).rstrip('\r\n'))
                    index += 1
                output.write('\r\n')

        item['body_html'] = '<pre>' + output.getvalue() + '</pre>'
    return item


name = 'Format AP Weather stories'
label = 'AP Weather'
callback = ap_weather_format
access_type = 'frontend'
action_type = 'direct'
