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
import superdesk


class ZCZCSportsResultsParser(ZCZCFeedParser):

    NAME = 'Sportsresults_zczc'

    def set_item_defaults(self, item, provider):
        super().set_item_defaults(item, provider)
        item[FORMAT] = FORMATS.PRESERVED
        item['original_source'] = 'Sports Results'

    def post_process_item(self, item, provider):
        genre_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='genre')
        item['genre'] = [x for x in genre_map.get('items', []) if
                         x['qcode'] == 'Results (sport)' and x['is_active']]
        return item

try:
    register_feed_parser(ZCZCSportsResultsParser.NAME, ZCZCSportsResultsParser())
except AlreadyExistsError as ex:
    pass
register_feeding_service_error('file', AAPParserError.ZCZCParserError().get_error_description())
