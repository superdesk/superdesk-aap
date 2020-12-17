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
from superdesk.metadata.item import GUID_FIELD


class AAPNINJSFormatter(NINJSFormatter):

    def __init__(self):
        super().__init__()
        self.can_preview = False
        self.can_export = False
        self.format_type = 'aap ninjs'

    def format(self, article, subscriber, codes=None):
        try:
            pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)

            ninjs = self._transform_to_ninjs(article, subscriber)
            ninjs['original_item'] = article.get('family_id', article.get(GUID_FIELD, article.get('uri')))

            return [(pub_seq_num, json.dumps(ninjs, default=json_serialize_datetime_objectId))]
        except Exception as ex:
            raise FormatterError.ninjsFormatterError(ex, subscriber)
