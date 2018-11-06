# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from datetime import datetime
from pytz import timezone
from superdesk.utc import get_date
from apps.archive.common import format_dateline_to_locmmmddsrc
from flask import current_app as app


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
