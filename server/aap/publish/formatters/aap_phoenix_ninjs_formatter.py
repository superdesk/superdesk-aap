# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import json
import superdesk
from superdesk.publish.formatters.ninjs_formatter import NINJSFormatter
from superdesk.utils import json_serialize_datetime_objectId
from superdesk.errors import FormatterError
from superdesk.metadata.item import GUID_FIELD, ITEM_TYPE, CONTENT_TYPE
from superdesk.metadata.packages import RESIDREF, GROUP_ID, GROUPS, ROOT_GROUP, REFS


class PhoenixNINJSFormatter(NINJSFormatter):

    def __init__(self):
        super().__init__()
        self.can_preview = False
        self.can_export = False
        self.format_type = 'aap phoenix'

    def format(self, article, subscriber, codes=None):
        try:
            pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)

            ninjs = self._transform_to_ninjs(article, subscriber)
            ninjs['original_item'] = article.get('family_id', article.get(GUID_FIELD, article.get('uri')))

            if article.get('type') == 'composite':
                ninjs['sections'] = self._get_sections(article, ninjs)

            return [(pub_seq_num, json.dumps(ninjs, default=json_serialize_datetime_objectId))]
        except Exception as ex:
            raise FormatterError.ninjsFormatterError(ex, subscriber)

    def _transform_to_ninjs(self, article, subscriber, recursive=True):
        ninjs = super()._transform_to_ninjs(article, subscriber, recursive)

        # if the article has an abstract then the description text has been over written by the abstract
        if article.get('abstract'):
            # if it is a picture then put it back
            if article.get('type') == 'picture':
                ninjs['description_text'] = article.get('description_text', '')

        result = superdesk.get_resource_service("product_tests").test_products(article, lookup=None)
        ninjs['products'] = [{"code": p["product_id"], "name": p.get("name")} for p in result if
                             p.get("matched", False)]

        if article.get('flags', {}).get('marked_for_sms', False) and 'sms_message' in article:
            ninjs['sms_message'] = article.get('sms_message', article.get('abstract', ''))
        return ninjs

    def _get_sections(self, article, ninjs):
        """
        Construct a sections entry for Phoenix as per their request
        :param article:
        :return:
        """

        if article.get('extra', {}).get('package_description'):
            # Add the description for the entire package
            sections = [{'items': [{'type': 'html', 'html': article.get('extra', {}).get('package_description', '')}]}]
        else:
            sections = []

        for group in article.get(GROUPS, []):
            if group[GROUP_ID] == ROOT_GROUP:
                continue

            group_items = []

            # Add any description for the group if there is one available
            description_name = 'package_' + group[GROUP_ID].replace(' ', '_') + '_description'
            if article.get('extra', {}).get(description_name, None):
                group_items.append({'type': 'html', 'html': article.get('extra', {}).get(description_name, '')})

            for ref in group[REFS]:
                if RESIDREF in ref:
                    # Any pictures get promoted to feature media and not presented as part of the package
                    if ref.get(ITEM_TYPE) == 'picture':
                        # find the image published or not
                        archive_pic = superdesk.get_resource_service('archive').find_one(req=None, _id=ref[RESIDREF])
                        image_ninjs = self._transform_to_ninjs(archive_pic, None, False)
                        if isinstance(ninjs.get('associations'), dict):
                            ninjs['associations']['featuremedia'] = image_ninjs
                    else:
                        item = dict()
                        item['guid'] = ref[RESIDREF]
                        item['type'] = 'newsitem' if ref.get(ITEM_TYPE) == CONTENT_TYPE.TEXT else ref.get(ITEM_TYPE)
                        group_items.append(item)

            if len(group_items):
                sections.append({'header': group[GROUP_ID], 'items': group_items})
        return sections
