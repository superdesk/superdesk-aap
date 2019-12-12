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
import re
from superdesk.metadata.item import FORMATS, FORMAT, GUID_FIELD, FAMILY_ID
import html


class AAPNewsroomNinjsFormatter(NewsroomNinjsFormatter):

    clean_fields = ('body_html', 'headline', 'description_text', 'description_html')

    PATTERN = r'((?:<a href[^>]+>)|(?:<a href=\"))?((?:(?:https|http)://)[\w/\-?=%.]+\.[\w/\-?=&;%#@.\+:]+)'
    URL_REGEX = re.compile(PATTERN, re.IGNORECASE)

    def _format_url_to_anchor_tag(self, tag_text):
        def replacement(match_object):
            href_tag, url = match_object.groups()
            if href_tag:
                # Since it has an href tag, this isn't what we want to change,
                # so return the whole match.
                return match_object.group(0)
            else:
                return '<a href="{0}" target="_blank">{0}</a>'.format(html.unescape(url), url)

        return re.sub(self.URL_REGEX, replacement, tag_text)

    def __init__(self):
        self.format_type = 'aap newsroom ninjs'
        self.can_preview = False
        self.can_export = False
        self.internal_renditions = ['original', 'viewImage', 'baseImage']

    def _transform_to_ninjs(self, article, subscriber, recursive=True):
        ninjs = super()._transform_to_ninjs(article, subscriber, recursive)

        # If the item was ingested and auto-published, the guid is set to the ingest_id
        # which in FileFeeds will be the path to the file that was ingested
        # [STTNHUB-58] - Auto published ingested items should preserve id
        # (https://github.com/superdesk/superdesk-core/pull/1579)
        # Change the guid back to using the family_id of the item
        if (ninjs.get(GUID_FIELD) or '').startswith('/mnt/'):
            ninjs[GUID_FIELD] = article.get(FAMILY_ID)

        if article.get(FORMAT) == FORMATS.HTML:
            ninjs['body_html'] = self._format_url_to_anchor_tag(ninjs.get('body_html', ''))

        # if the article has an abstract then the description text has been over written by the abstract
        if article.get('abstract'):
            # if it is a picture then put it back
            if article.get('type') == 'picture':
                ninjs['description_text'] = article.get('description_text', '')

        if article.get('anpa_take_key'):
            ninjs['anpa_take_key'] = article['anpa_take_key']

        # Replace such things as smart quotes to ensure that the usage of quotes is consistent within the article
        for f in self.clean_fields:
            if ninjs.get(f):
                ninjs[f] = clean_string(ninjs.get(f))
        return ninjs
