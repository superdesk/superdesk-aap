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
import lxml.html
import superdesk.etree as sd_etree

logger = logging.getLogger(__name__)


def remove_anchors(item, **kwargs):
    """

    :param item:
    :param kwargs:
    :return:
    """

    def clean_html(html):
        cleaner = lxml.html.clean.Cleaner(remove_tags=['a'])
        root = lxml.html.fromstring(html)

        for elem in root.iter():
            elem.attrib.pop("id", None)
            elem.attrib.pop("class", None)
            if elem.tag in ('hl2', 'pre', 'note'):
                elem.tag = 'p'

        root = cleaner.clean_html(root)
        return sd_etree.to_string(root, method="html")

    if item.get('body_html'):
        item['body_html'] = clean_html(item.get('body_html', ''))

    return item


name = 'Remove Anchors'
label = 'Remove Links from text'
callback = remove_anchors
access_type = 'frontend'
action_type = 'direct'
