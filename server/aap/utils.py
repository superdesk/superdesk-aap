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

from datetime import datetime
from pytz import timezone
from superdesk.utc import get_date
from apps.archive.common import format_dateline_to_locmmmddsrc
from flask import current_app as app
from superdesk.etree import parse_html


def set_dateline(item, city, source, set_date=False, text=None):
    """Set the dateline for item"""
    if not city:
        return

    cities = app.locators.find_cities()
    located = [c for c in cities if c['city'].lower() == city.lower()]
    item.setdefault('dateline', {})
    item['dateline']['located'] = located[0] if len(located) > 0 else {'city_code': city, 'city': city,
                                                                       'tz': 'UTC', 'dateline': 'city'}
    if set_date:
        item['dateline']['date'] = datetime.fromtimestamp(get_date(item['firstcreated']).timestamp(),
                                                          tz=timezone(item['dateline']['located']['tz']))
    item['dateline']['source'] = source
    if text:
        item['dateline']['text'] = text
    else:
        item['dateline']['text'] = format_dateline_to_locmmmddsrc(item['dateline']['located'],
                                                                  get_date(item['firstcreated']),
                                                                  source=source)


DATELINE_REGEX = r' \((Reuters|Thomson Reuters Foundation|Variety\.com|OPTA|Gracenote|AP)\) - '


def remove_dateline(item):
    """Remove the dateline from item"""
    html = item.get('body_html')
    if not html:
        return

    match = re.search(DATELINE_REGEX, html, re.IGNORECASE)
    if not match:
        return

    # get the matched string
    matched_string = match.group(0)
    parsed = parse_html(html, content='xml')
    pars = parsed.xpath('//p')

    for par in pars:
        if not par.text:
            continue
        if matched_string in par.text:
            city, source, the_rest = par.text.partition(matched_string)
            search_string = ''.join([s for s in [city, source]])
            item['body_html'] = html.replace(search_string, '')
            break
