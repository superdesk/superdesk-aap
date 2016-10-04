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
from bs4 import BeautifulSoup, NavigableString

class ZCZCMedianetParser(ZCZCFeedParser):

    NAME = 'Meadinet_zczc'

    def set_item_defaults(self, item, provider):
        super().set_item_defaults(item, provider)
        # Medianet
        item[FORMAT] = FORMATS.PRESERVED
        item['original_source'] = 'Medianet'
        item['urgency'] = 8
        self.CATEGORY = '$'
        self.TAKEKEY = ':'

        self.header_map = {'%': None, self.TAKEKEY: self.ITEM_TAKE_KEY}

    def post_process_item(self, item, provider):
        item['slugline'] = 'Media Release'
        item['headline'] = 'Media Release: ' + item.get(self.ITEM_TAKE_KEY, '')

        genre_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='genre')
        item['genre'] = [x for x in genre_map.get('items', []) if
                         x['qcode'] == 'Press Release' and x['is_active']]
        soup = BeautifulSoup(item.get('body_html', ''), "html.parser")
        ptag = soup.find('pre')
        if ptag is not None:
            ptag.insert(0, NavigableString('{} '.format('Media release distributed by AAP Medianet. \r\n\r\n\r\n')))
            item['body_html'] = str(soup)

        return item

try:
    register_feed_parser(ZCZCMedianetParser.NAME, ZCZCMedianetParser())
except AlreadyExistsError as ex:
    pass
register_feeding_service_error('file', AAPParserError.ZCZCParserError().get_error_description())
