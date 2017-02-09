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
from aap.errors import AAPParserError
from datetime import datetime
from superdesk.io.iptc import subject_codes
from superdesk.logging import logger
import re
import superdesk


class ZCZCPMFParser(ZCZCFeedParser):

    NAME = 'PMF_zczc'

    def set_item_defaults(self, item, provider):
        super().set_item_defaults(item, provider)
        item[FORMAT] = FORMATS.PRESERVED
        item['original_source'] = 'Pagemasters'
        self.KEYWORD = '#'
        self.TAKEKEY = '@'
        self.HEADLINE = ':'
        self.header_map = {self.KEYWORD: self.ITEM_SLUGLINE, self.TAKEKEY: self.ITEM_TAKE_KEY,
                           self.HEADLINE: self.ITEM_HEADLINE}

    def _set_results_genre(self, item):
        genre_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='genre')
        item['genre'] = [x for x in genre_map.get('items', []) if
                         x['qcode'] == 'Results (sport)' and x['is_active']]

    def post_process_item(self, item, provider):
        try:
            # is it a horse or dog racing item
            if item.get(self.ITEM_SLUGLINE, '').find('Grey') != -1 or item.get(self.ITEM_SLUGLINE, '').find(
                    'Trot') != -1 or item.get(self.ITEM_SLUGLINE, '').find('Gallop') != -1:
                # Don't look for the date in the TAB Dividends
                if item.get(self.ITEM_HEADLINE, '').find('TAB DIVS') == -1:
                    try:
                        raceday = datetime.strptime(item.get(self.ITEM_HEADLINE, ''), '%d/%m/%Y')
                        item[self.ITEM_TAKE_KEY] = 'Fields ' + raceday.strftime('%A')
                    except:
                        item[self.ITEM_TAKE_KEY] = 'Fields'
                    # it's the dogs
                    if item.get(self.ITEM_SLUGLINE, '').find('Grey') != -1:
                        item[self.ITEM_HEADLINE] = item.get(self.ITEM_SLUGLINE) + 'hound ' + item.get(
                            self.ITEM_TAKE_KEY,
                            '')
                        item[self.ITEM_SUBJECT] = [{'qcode': '15082000', 'name': subject_codes['15082000']}]
                    if item.get(self.ITEM_SLUGLINE, '').find('Trot') != -1:
                        item[self.ITEM_HEADLINE] = item.get(self.ITEM_SLUGLINE) + ' ' + item.get(self.ITEM_TAKE_KEY,
                                                                                                 '')
                        item[self.ITEM_SUBJECT] = [{'qcode': '15030003', 'name': subject_codes['15030003']}]
                else:
                    # Dividends
                    if item.get(self.ITEM_HEADLINE, '').find('TAB DIVS') != -1:
                        item[self.ITEM_TAKE_KEY] = re.sub(' Monday$| Tuesday$| Wednesday$| Thursday$| Friday$',
                                                          '', item[self.ITEM_HEADLINE])
                        item[self.ITEM_HEADLINE] = '{} {}'.format(item[self.ITEM_SLUGLINE], item[self.ITEM_HEADLINE])
                        if item.get(self.ITEM_SLUGLINE, '').find('Greyhound') != -1:
                            item[self.ITEM_SLUGLINE] = item.get(self.ITEM_SLUGLINE, '').replace('Greyhound', 'Greys')
                            item[self.ITEM_SUBJECT] = [{'qcode': '15082000', 'name': subject_codes['15082000']}]
                        if item.get(self.ITEM_SLUGLINE, '').find('Trot') != -1:
                            item[self.ITEM_SUBJECT] = [{'qcode': '15030003', 'name': subject_codes['15030003']}]
                        if item.get(self.ITEM_SLUGLINE, '').find('Gallop') != -1:
                            item[self.ITEM_SUBJECT] = [{'qcode': '15030001', 'name': subject_codes['15030001']}]
                item[self.ITEM_ANPA_CATEGORY] = [{'qcode': 'r'}]
                self._set_results_genre(item)
            elif item.get(self.ITEM_SLUGLINE, '').find(' Betting') != -1:
                try:
                    raceday = datetime.strptime(item.get(self.ITEM_HEADLINE, ''), '%d/%m/%Y')
                    item[self.ITEM_TAKE_KEY] = raceday.strftime('%A')
                except:
                    pass
                item[self.ITEM_SLUGLINE] = item.get(self.ITEM_SLUGLINE, '').replace(' Betting', ' Market')
                item[self.ITEM_HEADLINE] = '{} {}'.format(item[self.ITEM_SLUGLINE], item[self.ITEM_TAKE_KEY])
                item[self.ITEM_SUBJECT] = [{'qcode': '15030001', 'name': subject_codes['15030001']}]
                item[self.ITEM_ANPA_CATEGORY] = [{'qcode': 'r'}]
            elif item.get(self.ITEM_SLUGLINE, '').find('AFL') != -1:
                item[self.ITEM_ANPA_CATEGORY] = [{'qcode': 't'}]
                item[self.ITEM_SUBJECT] = [{'qcode': '15084000', 'name': subject_codes['15084000']}]
                self._set_results_genre(item)
            else:
                item[self.ITEM_ANPA_CATEGORY] = [{'qcode': 'f'}]
                item[self.ITEM_SUBJECT] = [{'qcode': '04000000', 'name': subject_codes['04000000']}]
            return item

        except Exception as ex:
            logger.exception(ex)


try:
    register_feed_parser(ZCZCPMFParser.NAME, ZCZCPMFParser())
except AlreadyExistsError as ex:
    pass
register_feeding_service_error('file', AAPParserError.ZCZCParserError().get_error_description())
