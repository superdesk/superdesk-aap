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
from superdesk.io.iptc import subject_codes
from superdesk.logging import logger
from aap.macros.racing_reformat import racing_reformat_macro


class ZCZCRacingParser(ZCZCFeedParser):
    NAME = 'Racing_zczc'

    # These destination codes will be extracted from the line begining with YY or HH and appended to the keywords
    destinations = ('PEB', 'FFB', 'FORM', 'RFG')

    def set_item_defaults(self, item, provider):
        super().set_item_defaults(item, provider)
        item[FORMAT] = FORMATS.PRESERVED

    def _scan_lines(self, item, lines):
        for line_num in range(3, min(len(lines), 6)):
            if lines[line_num] != '':
                item[self.ITEM_HEADLINE] = lines[line_num].strip()
                item[self.ITEM_SLUGLINE] = lines[line_num].strip()
                break

    def post_process_item(self, item, provider):
        try:
            lines_to_remove = 1
            # Pagemasters sourced content is Greyhound or Trot related, maybe AFL otherwise financial
            # It is from the Racing system
            item[self.ITEM_ANPA_CATEGORY] = [{'qcode': 'r'}]
            item[self.ITEM_SUBJECT] = [{'qcode': '15030001', 'name': subject_codes['15030001']}]
            lines = item['body_html'].split('\n')
            # If the content is to be routed/auto published
            if lines[0].upper().find('YY ') != -1 or lines[0].upper().find('HH ') != -1:
                for dest in self.destinations:
                    if lines[0].upper().find(' ' + dest.upper()) != -1:
                        if (item.get('keywords')):
                            item.get('keywords', []).append(dest)
                        else:
                            item['keywords'] = [dest]

            if lines[2] and lines[2].find(':SPORT -') != -1:
                item[self.ITEM_HEADLINE] = lines[2][9:]
                if lines[1] and lines[1].find(':POTTED :') != -1:
                    item[self.ITEM_SLUGLINE] = lines[1][9:]
                lines_to_remove = 3
            elif lines[1] and lines[1].find('RACING : ') != -1:
                item[self.ITEM_HEADLINE] = lines[1][8:]
                item[self.ITEM_SLUGLINE] = lines[1][8:]
                lines_to_remove = 2
            elif lines[1] and lines[1].find(':POTTED :') != -1:
                item[self.ITEM_HEADLINE] = lines[1][9:]
                item[self.ITEM_SLUGLINE] = lines[1][9:]
                lines_to_remove = 2
            elif lines[1] and lines[1].find(':Premierships') != -1:
                item[self.ITEM_HEADLINE] = lines[1][1:]
                item[self.ITEM_SLUGLINE] = item[self.ITEM_HEADLINE]
                # the overflow of the slugline is dumped in the take key
                item[self.ITEM_TAKE_KEY] = item.get(self.ITEM_SLUGLINE)[21:]
                item[self.ITEM_SLUGLINE] = item[self.ITEM_SLUGLINE][:21]
                lines_to_remove = 2
            elif lines[1] and lines[1].find(' WEIGHTS ') != -1:
                self._scan_lines(item, lines)
            elif lines[0] and lines[0].find('YY ') != -1 or lines[0].find('HH ') != -1:
                item[self.ITEM_HEADLINE] = lines[1]
                item[self.ITEM_SLUGLINE] = lines[1]
                if lines[1].find(' Comment ') != -1:
                    # need to split the line on the word Comment
                    item[self.ITEM_SLUGLINE] = lines[1][:lines[1].find('Comment')] + 'Comment'
                    item[self.ITEM_TAKE_KEY] = lines[1][lines[1].find('Comment') + 8:]
                    item[self.ITEM_HEADLINE] = lines[1][:lines[1].find('Comment')] + 'Gallop Comment ' + item[
                        self.ITEM_TAKE_KEY]
                    lines_to_remove = 2
            else:
                self._scan_lines(item, lines)

            item['body_html'] = '<pre>' + '\n'.join(lines[lines_to_remove:])

            # if the concatenation of the slugline and take key contain the phrase 'Brief Form' change the category to
            # h
            if (item.get(self.ITEM_SLUGLINE, '') + item.get(self.ITEM_TAKE_KEY, '')).lower().find('brief form') >= 0:
                item[self.ITEM_ANPA_CATEGORY] = [{'qcode': 'h'}]
            # Another exception
            if 'NZ/AUST FIELDS' in item.get('body_html', ''):
                item[self.ITEM_ANPA_CATEGORY] = [{'qcode': 'h'}]

            # if the item has been marked as convert to HTML then we need to use the racing reformat macro
            # to convert it.
            if lines[0] and lines[0].find('HH ') != -1:
                racing_reformat_macro(item)

            return item

        except Exception as ex:
            logger.exception(ex)


try:
    register_feed_parser(ZCZCRacingParser.NAME, ZCZCRacingParser())
except AlreadyExistsError as ex:
    pass
register_feeding_service_error('file', AAPParserError.ZCZCParserError().get_error_description())
