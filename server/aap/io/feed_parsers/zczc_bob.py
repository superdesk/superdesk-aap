#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license*.

from .zczc import ZCZCFeedParser
from superdesk.metadata.item import FORMAT, FORMATS
from superdesk.io.registry import register_feeding_service_error
from superdesk.errors import AlreadyExistsError
from superdesk.io.registry import register_feed_parser
from superdesk.utc import utcnow
from aap.errors import AAPParserError
import re
import superdesk
from superdesk.logging import logger
from aap.utils import set_dateline


class ZCZCBOBParser(ZCZCFeedParser):

    NAME = 'BOB_zczc'

    def set_item_defaults(self, item, provider):
        super().set_item_defaults(item, provider)
        item[FORMAT] = FORMATS.HTML
        item['original_source'] = 'BOB'
        self.CATEGORY = '%'
        self.KEYWORD = '#'
        self.HEADLINE = '$'
        self.TAKEKEY = ':'
        self.IPTC = '*'
        self.FORMAT = None
        self.header_map = {self.KEYWORD: self.ITEM_SLUGLINE, self.TAKEKEY: self.ITEM_TAKE_KEY,
                           self.HEADLINE: self.ITEM_HEADLINE, self.SERVICELEVEL: None,
                           self.PLACE: self.ITEM_PLACE}

    def post_process_item(self, item, provider):
        try:
            is_broadcast_script = False
            item['body_html'] = '<p>{}</p>'.format(
                re.sub('<p>   ', '<p>', item.get('body_html', '').replace('\n\n', '\n').replace('\n', '</p><p>')))
            if not item.get('genre'):
                genre_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='genre')
                item['genre'] = [x for x in genre_map.get('items', []) if
                                 x['qcode'] == 'Broadcast Script' and x['is_active']]
                item['sign_off'] = 'RTV'
                is_broadcast_script = True

            if self.ITEM_PLACE in item:
                if item[self.ITEM_PLACE] and is_broadcast_script:
                    item['headline'] = '{}: {}'.format(item[self.ITEM_PLACE], item.get(self.ITEM_HEADLINE, ''))
                locator_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='locators')
                place = [x for x in locator_map.get('items', []) if
                         x['qcode'] == item.get(self.ITEM_PLACE, '').upper()]
                if place is not None:
                    item[self.ITEM_PLACE] = place
                else:
                    item.pop(self.ITEM_PLACE)

            if item.get('genre') and item.get('genre')[0] and item.get('genre')[0].get('qcode') == 'AM Service':
                item['firstcreated'] = utcnow()
                item['abstract'] = item['headline']
                slugline = (item.get('slugline') or '').lower()
                dateline_city = ''
                for city in ['sydney', 'melbourne', 'brisbane', 'adelaide', 'perth']:
                    if city in slugline:
                        dateline_city = city
                        break

                set_dateline(item, dateline_city, provider.get('source'), set_date=True)

            # Remove the attribution
            item['body_html'] = item.get('body_html', '').replace('<p>AAP RTV</p>', '')
        except Exception as ex:
            logger.exception(ex)

        return item


try:
    register_feed_parser(ZCZCBOBParser.NAME, ZCZCBOBParser())
except AlreadyExistsError:
    pass
register_feeding_service_error('file', AAPParserError.ZCZCParserError().get_error_description())
