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
            return item

        item['body_html'] = item.get('body_html', '').replace('&nbsp;', ' ')
        soup = BeautifulSoup(item.get('body_html', ''), 'html.parser')
        sanitized_text = ''
        for p in soup.findAll('p'):
            row = p.get_text()
            sanitized_text = '{}{}{}'.format(sanitized_text, row, '\n')
        item['body_html'] = '<pre>{}</pre>'.format(sanitized_text)
        item[FORMAT] = FORMATS.PRESERVED
        return item
    except Exception as ex:
        logging.exception('Exception in preserve format macro: ', ex)
        raise ex


name = 'preserve_format'
label = 'Preserve Format'
callback = preserve
access_type = 'frontend'
action_type = 'direct'
