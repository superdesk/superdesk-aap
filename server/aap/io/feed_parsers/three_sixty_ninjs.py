# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015, 2016, 2017 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import datetime
from superdesk.utc import utc
from superdesk.io.registry import register_feed_parser
from superdesk.io.feed_parsers import NINJSFeedParser
from superdesk.media.renditions import get_renditions_spec, can_generate_custom_crop_from_original


class ThreeSixtyNinjs(NINJSFeedParser):
    NAME = '360 ninjs'

    label = '360 NINJS Feed Parser'

    def __init__(self):
        super().__init__()

    def can_parse(self, file_path):
        return True

    def parse(self, file_path, provider=None):
        self.items = []
        if super().can_parse(file_path):
            self.items = super().parse(file_path, provider)
        return self.items

    def _transform_from_ninjs(self, ninjs):

        # Remove all associations other than featuremedia
        if ninjs.get('associations') and ninjs.get('type') == 'text':
            delete_keys = [key for key in ninjs.get('associations').keys() if key != 'featuremedia']
            for key in delete_keys:
                ninjs['associations'].pop(key, None)
            ninjs.get('associations', {}).get('featuremedia').get('renditions').pop('FIXME', None)
            # Avoid problem of old images being received an then getting removed on ingest.
            ninjs.get('associations', {}).get('featuremedia').pop('versioncreated', None)
            rendition_spec = get_renditions_spec(without_internal_renditions=True)
            height = ninjs.get('associations', {}).get('featuremedia').get('renditions').get('original').get('height')
            width = ninjs.get('associations', {}).get('featuremedia').get('renditions').get('original').get('width')
            can_crop = True
            for (_spec, detail) in rendition_spec.items():
                if not can_generate_custom_crop_from_original(width, height, detail):
                    can_crop = False
            if not can_crop:
                ninjs.pop('associations', None)
        ninjs.pop('profile', None)
        if not ninjs.get('byline'):
            ninjs['byline'] = '360info'

        item = super()._transform_from_ninjs(ninjs)

        if ninjs.get('renditions', {}).get('original'):
            item['renditions'] = {'original': ninjs.get('renditions', {}).get('original')}
            item.get('renditions').get('original').pop('media')

        # make sure every picture has an alt text and truncate things to pass validation
        for _key, associated_item in item.get('associations', {}).items():
            if associated_item:
                if associated_item.get('type') == 'picture':
                    # renditions will be set from the ingested image
                    associated_item.pop('renditions', None)

        if ninjs.get('type') == 'picture':
            # fix to pass validation
            item['headline'] = ninjs.get('headline', '')[:42]
            if not item['headline']:
                item['headline'] = 'No Headline'
            item['alt_text'] = item['headline']
            item['description_text'] = ninjs.get('description_text', '')[:100]
            if not item['description_text']:
                item['description_text'] = 'No Caption'

        if ninjs.get('type') == 'text':

            # add marketplace keyword
            if item.get('keywords'):
                item['keywords'].append('marketplace')
            else:
                item.setdefault('keywords', ['marketplace'])

            # All features
            item['anpa_category'] = [{'qcode': 'c'}]

            # All items should have a uri, if canceled it is used to identify the already received item.
            item['uri'] = item['guid']

            try:
                if ninjs.get('embargoed'):
                    item['embargoed'] = datetime.datetime.strptime(ninjs.get('embargoed'),
                                                                   '%Y-%m-%dT%H:%M:%S+00:00').replace(tzinfo=utc)
            except ValueError:
                pass

        return item


register_feed_parser(ThreeSixtyNinjs.NAME, ThreeSixtyNinjs())
