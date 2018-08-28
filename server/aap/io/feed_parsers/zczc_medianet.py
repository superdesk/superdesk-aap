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
import superdesk
from superdesk.io.iptc import subject_codes
from superdesk.etree import parse_html, to_string
import html


class ZCZCMedianetParser(ZCZCFeedParser):
    NAME = 'Medianet_zczc'

    place_map = {'MNETALL': 'FED',
                 'MNETNSW': 'NSW',
                 'MNETQLD': 'QLD',
                 'MNETVIC': 'VIC',
                 'MNETSA': 'SA',
                 'MNETWA': 'WA',
                 'MNETACT': 'ACT',
                 'MNETNT': 'NT',
                 'MNETTAS': 'TAS'}

    subject_map = {'MFI': '04000000',
                   'MEN': '01021000',
                   'MSP': '15000000',
                   'MHE': '07007000',
                   'MIT': '13010000'}

    def set_item_defaults(self, item, provider):
        super().set_item_defaults(item, provider)
        # Medianet
        item['original_source'] = 'Medianet'
        item['urgency'] = 5
        self.CATEGORY = '$'
        self.TAKEKEY = ':'
        self.PLACE = '%'

        self.header_map = {self.PLACE: self.ITEM_PLACE, self.TAKEKEY: self.ITEM_TAKE_KEY}

    def post_process_item(self, item, provider):

        InvestorRelease = (len(item.get('anpa_category', [])) and
                           item['anpa_category'][0].get('qcode', '').lower() == 'k')

        if InvestorRelease:
            # IRW News Release:
            item['slugline'] = 'IRW News Release'
            item['headline'] = 'IRW News Release: ' + item.get(self.ITEM_TAKE_KEY, '')
        else:
            item['slugline'] = 'Media Release'
            item['headline'] = 'Media Release: ' + item.get(self.ITEM_TAKE_KEY, '')

        if item[FORMAT] == FORMATS.HTML:
            item['body_html'] = '<pre>' + html.escape(item['body_html']) + '</pre>'

        # Truncate the take key if required
        if len(item.get(self.ITEM_TAKE_KEY, '')) > 24:
            item[self.ITEM_TAKE_KEY] = item.get(self.ITEM_TAKE_KEY, '')[0:24]

        genre_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='genre')
        item['genre'] = [x for x in genre_map.get('items', []) if
                         x['qcode'] == 'Press Release' and x['is_active']]
        body_html_elem = parse_html(item.get('body_html', '<pre> </pre>'))
        ptag = body_html_elem.find('.//pre')
        if ptag is not None:
            if item[FORMAT] == FORMATS.PRESERVED:
                if InvestorRelease:
                    ptag.text = '{} '.format(
                        'Investor Relations news release distributed by AAP Medianet. \r\n\r\n\r\n') \
                        + ptag.text
                else:
                    ptag.text = '{} '.format('Media release distributed by AAP Medianet. \r\n\r\n\r\n') + ptag.text
                item['body_html'] = to_string(body_html_elem)
            else:
                body = ''
                if InvestorRelease:
                    body = '<p>Investor Relations news release distributed by AAP Medianet.<br><br></p>'
                else:
                    body = '<p>Media release distributed by AAP Medianet.<br><br></p>'
                pars = ptag.text.split('\n\n')
                for p in pars:
                    body = body + '<p>' + p.replace('\n', '<br>') + '</p>'
                item['body_html'] = body

        locator_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='locators')
        place_strs = item.pop('place').split(' ')
        for place in place_strs:
            if place in self.place_map:
                replace = [x for x in locator_map.get('items', []) if
                           x['qcode'] == self.place_map.get(place, '').upper()]
                if replace is not None:
                    item[self.ITEM_PLACE] = replace

            if place in self.subject_map:
                if item.get(self.ITEM_SUBJECT) is None:
                    item[self.ITEM_SUBJECT] = []
                item['subject'].append(
                    {'qcode': self.subject_map.get(place), 'name': subject_codes[self.subject_map.get(place)]})

        return item


try:
    register_feed_parser(ZCZCMedianetParser.NAME, ZCZCMedianetParser())
except AlreadyExistsError as ex:
    pass
register_feeding_service_error('file', AAPParserError.ZCZCParserError().get_error_description())
