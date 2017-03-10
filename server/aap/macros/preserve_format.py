# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from superdesk.metadata.item import FORMATS, FORMAT
import logging
import html
from superdesk.etree import parse_html, etree

logger = logging.getLogger(__name__)


def format_text_content(tag):
    for x in tag.iter():
        if x.text is not None:
            x.text = x.text.strip() + '\n'


def sanitize_tags(item):
    content = item.get('body_html', '')
    content = content.replace('<br>', '<br/>').replace('</br>', '')
    content = content.replace('&nbsp;', ' ')

    parsed = parse_html(content, content='html')

    # breaks are replaced with line feeds
    for br in parsed.xpath('//br'):
        br.tail = '\n' + br.tail if br.tail else '\n'
    etree.strip_elements(parsed, 'br', with_tail=False)

    for tag in parsed.iter():
        if tag.getparent() is not None and tag.getparent().tag == 'body':
            format_text_content(tag)
    item['body_html'] = '<pre>{}</pre>'.format(html.escape(''.join(parsed.itertext())))
    item[FORMAT] = FORMATS.PRESERVED
    return item


def preserve(item, **kwargs):
    """
    This macro removes any markup from body_html and wraps it with <pre> tag
    And sets the preserve_format field to true
    :param item: Story
    :param kwargs:
    :return:
    """
    try:
        return sanitize_tags(item)
    except Exception as ex:
        logging.exception('Exception in preserve format macro: ', ex)
        raise ex


name = 'preserve_format'
label = 'Preserve Format'
callback = preserve
access_type = 'frontend'
action_type = 'direct'
order = 6
