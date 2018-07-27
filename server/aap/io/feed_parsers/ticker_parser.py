# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license*.
from superdesk.io.registry import register_feed_parser, register_feeding_service_parser
from superdesk.io.feeding_services.file_service import FileFeedingService
from .text_file import TextFileParser
from superdesk.errors import AlreadyExistsError
import time


class TickerFileParser(TextFileParser):
    """
    A simple parser for ticker files, the headline gives an indication it is an AAP ticker story. The body of the
    story is the content for the ticker.
    """

    NAME = 'AAP Ticker File'

    def parse(self, filename, provider=None):
        item = super().parse(filename, provider)
        item['headline'] = 'AAP Ticker on {}'.format(time.strftime("%A %H:%M:%S", time.localtime()))
        return item

    def post_process_item(self, item):
        item['headline'] = item['headline'][:40]
        return item


try:
    register_feed_parser(TickerFileParser.NAME, TickerFileParser())
except AlreadyExistsError as ex:
    pass
register_feeding_service_parser(FileFeedingService.NAME, TickerFileParser.NAME)
