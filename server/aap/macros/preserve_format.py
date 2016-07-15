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


def format_text_content(tag):
    for child_tag in tag.find_all():
        if child_tag.name == 'br':
            child_tag.replace_with('{}'.format(child_tag.get_text()))
        else:
            if child_tag.get_text() != '\n':
                child_tag.replace_with('{}\n'.format(child_tag.get_text()))

    para_text = tag.get_text().strip()
    if para_text != '\n':
        tag.replace_with('{}\n'.format(para_text))


def sanitize_tags(item):
    content = item.get('body_html', '')
    content = content.replace('<br>', '\n')
    content = content.replace('&nbsp;', ' ')
    soup = BeautifulSoup(content, 'html.parser')
    for top_level_tag in soup.find_all(recursive=False):
        format_text_content(top_level_tag)
    item['body_html'] = '<pre>{}</pre>'.format(soup.get_text())
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
