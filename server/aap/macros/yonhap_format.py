# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk import etree as sd_etree
import logging
from flask import current_app as app
from lxml import etree
from apps.archive.common import format_dateline_to_locmmmddsrc
from superdesk.utc import get_date

logger = logging.getLogger(__name__)


def _yonhap_derive_dateline(item, **kwargs):
    """
    It seems that most locations injected into the item by the parser are Bangalor
    This function looks for a dateline in the article body an uses that.
    :param items:
    :return:
    """
    try:
        html = item.get('body_html')
        if html:
            parsed = sd_etree.parse_html(html, content='xml')
            pars = parsed.xpath('//p')
            for par in pars:
                if not par.text:
                    continue
                city, source, the_rest = par.text.partition(' (Yonhap) -- ')
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

                    item['dateline']['located'] = located[0] if len(located) == 1 else {'city_code': city,
                                                                                        'city': city,
                                                                                        'tz': 'UTC',
                                                                                        'dateline': 'city'}
                    item['dateline']['source'] = item.get('source', 'Yonhap')
                    item['dateline']['text'] = format_dateline_to_locmmmddsrc(item['dateline']['located'],
                                                                              get_date(item['firstcreated']),
                                                                              source='Yonhap')
                    break

        return item
    except:
        logging.exception('Yonhap dateline macro exception')


def yonhap_format(item, **kwargs):
    try:
        html = item.get('body_html')
        # Article must be from Yonhap
        if '(Yonhap)' not in html:
            return item
        item['source'] = 'Yonhap'

        if html:
            parsed = sd_etree.parse_html(html, content='xml')
            pars = parsed.xpath('//body')
            if len(pars) == 1:
                pars[0].tag = 'p'
                content = etree.tostring(pars[0], encoding="unicode")
                item['body_html'] = content.replace('&#13;\n   ', '</p><p>').replace('&#13;\n', '').replace('<br/>',
                                                                                                            ' ')
                _yonhap_derive_dateline(item)

    except Exception as ex:
        logging.exception('Exception in yonhap format macro: ', ex)
        raise ex

    return item


name = 'Format YONHAP stories'
label = 'YONHAP format'
callback = yonhap_format
access_type = 'frontend'
action_type = 'direct'
