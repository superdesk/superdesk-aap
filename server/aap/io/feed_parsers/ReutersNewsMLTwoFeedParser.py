# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015, 2016, 2017 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.io.feed_parsers import NewsMLTwoFeedParser
from superdesk.io.registry import register_feed_parser, register_feeding_service_parser
from apps.io.feeding_services.reuters import ReutersHTTPFeedingService


class ReutersNewsMLTwoFeedParser(NewsMLTwoFeedParser):
    """
    Feed Parser which can parse if the feed is in NewsML 2 format.

    """

    NAME = 'reutersnewsml2'
    label = 'Reuters News ML 2.0 Parser'

    def parse_content_place(self, tree, item):
        """Parse subject with type="cptType:5" into place list."""
        item['place'] = []


register_feed_parser(ReutersNewsMLTwoFeedParser.NAME, ReutersNewsMLTwoFeedParser())
register_feeding_service_parser(ReutersHTTPFeedingService.NAME, ReutersNewsMLTwoFeedParser.NAME)
