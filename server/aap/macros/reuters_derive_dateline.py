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
from superdesk.etree import parse_html
from aap.utils import set_dateline


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

                    # there is already a dateline that is not Bangalore/BENGALURU don't do anything just return
                    if 'located' in (item.get('dateline') or {}) and \
                            item['dateline']['located'].get('city').upper() not in ['BANGALORE', 'BENGALURU']:
                        return

                    set_dateline(item, city, 'Reuters')
                    break

        return item
    except:
        logging.exception('Reuters dateline macro exception')


name = 'Reuters derive dateline'
callback = reuters_derive_dateline
access_type = 'backend'
action_type = 'direct'
