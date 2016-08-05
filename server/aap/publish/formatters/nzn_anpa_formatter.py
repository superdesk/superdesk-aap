# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from .anpa_formatter import AAPAnpaFormatter
from .category_list_map import get_nzn_category_list
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE


class NZNAnpaFormatter(AAPAnpaFormatter):

    def _get_category_list(self, category_list):
        return get_nzn_category_list(category_list)

    def _get_mapped_source(self, article):
        return article.get('source', '') if article.get('source', '') != 'AAP' else 'NZN'

    def can_format(self, format_type, article):
        return format_type == 'NZN ANPA' and article[ITEM_TYPE] == CONTENT_TYPE.TEXT
