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
from superdesk.etree import parse_html, to_string
from lxml import etree
logger = logging.getLogger(__name__)


def remove_breaks(item, **kwargs):
    try:
        html = item.get('body_html')
        if html:
            html = html.replace('<br>', '<br/>').replace('</br>', ' ')
            parsed = parse_html(html, content='xml')
            for br in parsed.xpath('//br'):
                br.tail = ' ' + br.tail if br.tail else ' '
            etree.strip_elements(parsed, 'br', with_tail=False)
            item['body_html'] = to_string(parsed)
            return item

    except Exception as ex:
        logging.exception('Exception in preserve format macro: ', ex)
        raise ex


name = 'remove_breaks'
label = 'Remove Line Breaks'
callback = remove_breaks
access_type = 'frontend'
action_type = 'direct'
order = 7
