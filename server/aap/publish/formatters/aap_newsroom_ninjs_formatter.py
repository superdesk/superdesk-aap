# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.publish.formatters.ninjs_newsroom_formatter import NewsroomNinjsFormatter
from .unicodetoascii import clean_string


class AAPNewsroomNinjsFormatter(NewsroomNinjsFormatter):

    clean_fields = ('body_html', 'headline', 'description_text', 'description_html')

    def __init__(self):
        self.format_type = 'aap newsroom ninjs'
        self.can_preview = False
        self.can_export = False
        self.internal_renditions = ['original', 'viewImage', 'baseImage']

    def _transform_to_ninjs(self, article, subscriber, recursive=True):
        ninjs = super()._transform_to_ninjs(article, subscriber, recursive)
        # Replace such things as smart quotes to ensure that the usage of quotes is consistent within the article
        for f in self.clean_fields:
            if ninjs.get(f):
                ninjs[f] = clean_string(ninjs.get(f))
        return ninjs
