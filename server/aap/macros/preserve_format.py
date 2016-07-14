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
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def sanitize_pre_tags(item):
    soup = BeautifulSoup(item.get('body_html', ''), 'html.parser')
    sanitized_text = ''
    for p in soup.findAll(['pre', 'p', 'div']):
        if len(list(p.children)) > 0:
            sanitized_children = ''
            for c in p.children:
                if c.name in ['div', 'p']:
                    rowc = c.get_text()
                    sanitized_children = '{}{}{}'.format(sanitized_children, rowc, '\n')

            if not sanitized_children:
                row = p.get_text()
                sanitized_children = '{}{}'.format(row, '\n')

            sanitized_text = '{}{}'.format(sanitized_text, sanitized_children)
    item['body_html'] = '<pre>{}</pre>'.format(sanitized_text)
    return item


def sanitize_tags(item):
    item['body_html'] = item.get('body_html', '').replace('&nbsp;', ' ')
    soup = BeautifulSoup(item.get('body_html', ''), 'html.parser')
    sanitized_text = ''
    for p in soup.findAll(['p', 'div']):
        row = p.get_text()
        sanitized_text = '{}{}{}'.format(sanitized_text, row, '\n')
    item['body_html'] = '<pre>{}</pre>'.format(sanitized_text)
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
        if item.get(FORMAT) == FORMATS.PRESERVED:
            # this item has been processed before
            # to make sure process again
            return sanitize_pre_tags(item)
        else:
            return sanitize_tags(item)
    except Exception as ex:
        logging.exception('Exception in preserve format macro: ', ex)
        raise ex


name = 'preserve_format'
label = 'Preserve Format'
callback = preserve
access_type = 'frontend'
action_type = 'direct'
