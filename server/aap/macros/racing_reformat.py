# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2016 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk import etree as sd_etree
from lxml import etree
from superdesk.metadata.item import FORMAT, FORMATS


def racing_reformat_macro(item, **kwargs):
    """Given a pre tagged content convert it to HTML

    :param item:
    :param kwargs:
    :return:
    """

    # If not preserved in the first place then don't do anything
    if item[FORMAT] != FORMATS.PRESERVED:
        return

    # Nothing to do!
    if 'body_html' not in item:
        return None

    root = sd_etree.parse_html(item['body_html'], content='html')
    body_html = etree.tostring(root, encoding="unicode", method="text")

    # Paragraphs created on new lines
    body_html = body_html.replace('\n', '__##br##__')
    list_paragraph = body_html.split('__##br##__')
    item['body_html'] = ''.join('<p>' + p + '</p>' for p in list_paragraph if p and p.strip())

    # Ensure that the format is HTML
    item[FORMAT] = FORMATS.HTML
    return item


name = 'Racing reformat'
label = 'Racing reformat'
callback = racing_reformat_macro
access_type = 'frontend'
action_type = 'direct'
