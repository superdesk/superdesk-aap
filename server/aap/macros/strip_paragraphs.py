# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2016 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.metadata.item import FORMATS, FORMAT
import logging
import html
from superdesk.etree import parse_html
from aap.publish.formatters.unicodetoascii import to_ascii

logger = logging.getLogger(__name__)


def strip_paragraphs(item, **kwargs):

    def format_text_content(tag):
        for x in tag.iter():
            if x.text is not None:
                x.text = to_ascii(x.text.strip()) + (' ' if not x.text.endswith('__##NBSP##__') else '')

    content = item.get('body_html', '')
    content = content.replace('<br>', '<br/>').replace('</br>', '')
    content = content.replace('</p>', '__##NBSP##__</p>')

    parsed = parse_html(content, content='html')

    for tag in parsed.xpath('/div/child::*'):
        format_text_content(tag)

    item['body_html'] = '<p>{}</p>'.format(html.escape(''.join(parsed.itertext()))).replace('__##NBSP##__', '&nbsp;')
    item[FORMAT] = FORMATS.HTML
    return item


name = 'strip paragraphs'
label = 'Strip Paragraphs'
callback = strip_paragraphs
access_type = 'frontend'
action_type = 'direct'
group = 'Copytakers'
