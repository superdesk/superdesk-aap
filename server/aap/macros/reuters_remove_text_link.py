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
import re


logger = logging.getLogger(__name__)


def reuters_remove_text_link(item, **kwargs):
    """

    :param item:
    :param kwargs:
    :return:
    """
    pattern = r'((?:<a href[^>]+>)|(?:<a href=\"))?((?:(?:https|http)://)[\w/\-?=%.]+\.[\w/\-?=&;%#@.\+:]+)'
    url_regex = re.compile(pattern, re.IGNORECASE)

    def remove_text_link(tag_text):
        return re.sub(url_regex, '', tag_text)

    html = item.get('body_html')
    if html and ('http' in html or 'HTTP' in html):
        item['body_html'] = remove_text_link(html)
    return item

name = 'Reuters text link'
callback = reuters_remove_text_link
access_type = 'backend'
action_type = 'direct'