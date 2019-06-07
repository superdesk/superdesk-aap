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
from superdesk import get_resource_service
from superdesk.etree import parse_html, to_string
from .am_service_content import am_service_content
import re


logger = logging.getLogger(__name__)


def am_bob_publish(item, **kwargs):
    """
    Macro that will re-purpose content from Bulletin Builder to the AM service in Newsroom.
    :param item:
    :param kwargs:
    :return:
    """
    try:
        locator_map = get_resource_service('vocabularies').find_one(req=None, _id='locators')

        am_service_content(item)

        if len(item.get('anpa_category', [])):
            category = item.get('anpa_category')[0].get('qcode')
            if category.lower() in ['s', 't']:
                if item.get('headline').startswith('AFL:'):
                    item['place'] = [x for x in locator_map.get('items', []) if x['qcode'] == 'FED']
                elif item.get('headline').startswith('CRIK:'):
                    item['place'] = [x for x in locator_map.get('items', []) if x['qcode'] == 'FED']
                else:
                    if '(CANBERRA)' in item.get('anpa_take_key') or '(SYDNEY)' in item.get('anpa_take_key'):
                        item['place'] = [x for x in locator_map.get('items', []) if x['qcode'] == 'NSW']
                    elif '(BRISBANE)' in item.get('anpa_take_key') or '(GOLD COAST)' in item.get('anpa_take_key'):
                        item['place'] = [x for x in locator_map.get('items', []) if x['qcode'] == 'QLD']
                    elif '(MELBOURNE)' in item.get('anpa_take_key') or '(HOBART)' in item.get('anpa_take_key'):
                        item['place'] = [x for x in locator_map.get('items', []) if x['qcode'] == 'VIC']
                    elif '(ADELAIDE)' in item.get('anpa_take_key'):
                        item['place'] = [x for x in locator_map.get('items', []) if x['qcode'] == 'SA']
                    elif '(PERTH)' in item.get('anpa_take_key'):
                        item['place'] = [x for x in locator_map.get('items', []) if x['qcode'] == 'WA']
                    else:
                        item['place'] = [x for x in locator_map.get('items', []) if x['qcode'] == 'FED']
                # Remove the prefix from the headline
                if ':' in item.get('headline', '') and item.get('headline').index(':') < 10:
                    item['headline'] = item.get('headline').split(': ')[1]
            else:
                # If the item has a location/place prefix then try to remove that from the headline
                if len(item.get('place', [])):
                    item['headline'] = re.sub('^' + item.get('place')[0].get('qcode', '') + ': ', '',
                                              item.get('headline', ''), flags=re.IGNORECASE)

            html = item.get('body_html')
            if html:
                parsed = parse_html(html, content='xml')
                pars = parsed.xpath('//p')
                count = 0
                for par in reversed(pars):
                    if not par.text:
                        continue
                    if par.text == 'RTV':
                        item['body_html'] = item.get('body_html', '').replace('<p>RTV</p>', '')
                        break
                    if re.search(r'^[A-Za-z0-9_]{2,8} RTV', par.text, re.IGNORECASE):
                        par.text = par.text.replace(' RTV', '').replace('RAW', 'Reuters')
                        item['body_html'] = to_string(parsed, method='html')
                        break
                    count = ++count
                    if count > 5:
                        break

        return item
    except:
        logger.warning('Exception caught in macro: AM BOB Publisher')
        return item


name = 'AM BOB Publisher'
label = 'AM BOB Publisher'
callback = am_bob_publish
access_type = 'frontend'
action_type = 'direct'
group = 'AM Desk'
