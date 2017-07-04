# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
from apps.archive.common import format_dateline_to_locmmmddsrc
from superdesk.utc import get_date
from flask import current_app as app
from superdesk.etree import parse_html

logger = logging.getLogger(__name__)


def reuters_derive_dateline(item, **kwargs):
    """
    It seems that most locations injected into the item by the parser are Bangalor
    This function looks for a dateline in the article body an uses that.
    :param items:
    :return:
    """
    try:
        html = item.get('body_html')
        if html:
            parsed = parse_html(html, content='xml')
            pars = parsed.xpath('//p')
            for par in pars:
                if not par.text:
                    continue
                city, source, the_rest = par.text.partition(' (Reuters) - ')
                if source:
                    # sometimes the city is followed by a comma and either a date or a state
                    city = city.split(',')[0]
                    if any(char.isdigit() for char in city):
                        return
                    cities = app.locators.find_cities()
                    located = [c for c in cities if c['city'].lower() == city.lower()]
                    # if not dateline we create one
                    if 'dateline' not in item:
                        item['dateline'] = {}
                    # there is already a dateline that is not Bangalore don't do anything just return
                    elif 'located' in item['dateline'] and 'BANGALORE' != item['dateline']['located'].get(
                            'city').upper():
                        return

                    item['dateline']['located'] = located[0] if len(located) == 1 else {'city_code': city,
                                                                                        'city': city,
                                                                                        'tz': 'UTC',
                                                                                        'dateline': 'city'}
                    item['dateline']['source'] = item.get('original_source', 'Reuters')
                    item['dateline']['text'] = format_dateline_to_locmmmddsrc(item['dateline']['located'],
                                                                              get_date(item['firstcreated']),
                                                                              source=item.get('original_source',
                                                                                              'Reuters'))
                    break

        return item
    except:
        logging.exception('Reuters dateline macro exception')


name = 'Reuters derive dateline'
callback = reuters_derive_dateline
access_type = 'backend'
action_type = 'direct'
