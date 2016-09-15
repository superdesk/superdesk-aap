#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license*.

from .zczc import ZCZCFeedParser
from superdesk.metadata.item import FORMAT, FORMATS
from superdesk.io import register_feeding_service_error
from superdesk.errors import AlreadyExistsError
from superdesk.io import register_feed_parser
from aap.errors import AAPParserError


class ZCZCMedianetParser(ZCZCFeedParser):

    NAME = 'Meadinet_zczc'

    def set_item_defaults(self, item, provider):
        super().set_item_defaults(item, provider)
        # Medianet
        item[FORMAT] = FORMATS.PRESERVED
        item['original_source'] = 'Medianet'
        item['urgency'] = 8
        self.HEADLINE = ':'
        self.header_map = {'%': None, self.HEADLINE: self.ITEM_HEADLINE}

try:
    register_feed_parser(ZCZCMedianetParser.NAME, ZCZCMedianetParser())
except AlreadyExistsError as ex:
    pass
register_feeding_service_error('file', AAPParserError.ZCZCParserError().get_error_description())
