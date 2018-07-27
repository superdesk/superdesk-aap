# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from superdesk.publish.formatters import Formatter
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE
from .unicodetoascii import to_ascii
import re
from superdesk.etree import parse_html
from lxml import etree
import superdesk


class TickerFormatter(Formatter):
    """Generate the format required by the ticker, See the document MONO SIMPLE SIGN DATA PROTOCOL Revision 1.4c
    """

    STX = b'\x02'  # Start of text, Start of message
    PASS = b'\x81'  # Password character
    SPEED = b'\xB0'  # Scroll speed set to slowest
    ETX = b'\x03'  # End of text end of message

    def __init__(self):
        self.format_type = 'aap ticker'
        self.can_preview = False
        self.can_export = False

    def format(self, article, subscriber, codes=None):
        pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)
        ticker_msg = []
        # Start of text
        ticker_msg.append(self.STX)
        ticker_msg.append(self.PASS)
        ticker_msg.append(self.SPEED)
        # text of the message
        body = to_ascii(self.get_text_content(article.get('body_html', '')))
        for c in body:
            ticker_msg.append(c.encode('ascii', 'replace'))
        ticker_msg.append(self.ETX)

        return [{'published_seq_num': pub_seq_num, 'encoded_item': b''.join(ticker_msg), 'formatted_item': body}]

    def get_text_content(self, content):
        # It's only a one line ticker so new line and carriage return become spaces
        content = re.sub('[\n]', ' ', content)
        content = re.sub('[\r]', ' ', content)
        # remove control chars as these will upset the ticker
        content = re.sub(r'[\x00-\x1f]', '', content)
        if content == '':
            return ''

        parsed = parse_html(content, content='html')
        text = etree.tostring(parsed, encoding="unicode", method="text")
        return text

    def can_format(self, format_type, article):
        return format_type == self.format_type and article[ITEM_TYPE] == CONTENT_TYPE.TEXT
