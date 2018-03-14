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
from unittest import mock
from superdesk.publish.formatters.ninjs_formatter import NINJSFormatter
from superdesk.utils import json_serialize_datetime_objectId
from superdesk.errors import FormatterError


@mock.patch('superdesk.publish.subscribers.SubscribersService.generate_sequence_number', lambda self, subscriber: 1)
class AAPNINJSFormatter(NINJSFormatter):
    rendition_properties = ('href', 'width', 'height', 'mimetype', 'poi', 'media', 'CropTop', 'CropBottom',
                            'CropRight', 'CropLeft')
    vidible_fields = {field: field for field in rendition_properties}
    vidible_fields.update({
        'url': 'href',
        'duration': 'duration',
        'mimeType': 'mimetype',
        'size': 'size',
    })

    def __init__(self):
        self.format_type = 'aap ninjs'
        self.can_preview = True
        self.can_export = True

    def format(self, article, subscriber, codes=None):
        try:
            pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)

            ninjs = self._transform_to_ninjs(article, subscriber)

            # if the article has an abstract then the description text has been over written by the abstract
            if article.get('abstract'):
                # if it is a picture then put it back
                if article.get('type') == 'picture':
                    ninjs['description_text'] = article.get('description_text', '')

            media = article.get('associations', {}).get('featuremedia')
            ninjs_media = article.get('associations', {}).get('featuremedia')
            if media and media.get('type') == 'picture':
                ninjs_media['description_text'] = media.get('description_text')

            return [(pub_seq_num, json.dumps(ninjs, default=json_serialize_datetime_objectId))]
        except Exception as ex:
            raise FormatterError.ninjsFormatterError(ex, subscriber)
