# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from ..field_mappers import FieldMapper
from superdesk.publish.formatters import Formatter


class SluglineMapper(FieldMapper):
    def map(self, article, category, **kwargs):
        """
        Based on the category and genre code it returns a prefix for the slugline
        :param dict article: original article
        :param str category: category of the article
        :param dict kwargs: keyword args
        :return: if found then the locator as string else None
        """
        formatter = Formatter()
        slugline = formatter.append_legal(article=article, truncate=kwargs.get('truncate', False))

        if slugline.upper().startswith('LEGAL:'):
            return slugline

        # Any Article with genre Explainer gets a locator EXP
        if [x for x in article.get('genre', []) if x['qcode'] == 'Explainer']:
            if not article.get('slugline', '').startswith('EXP:'):
                slugline = 'EXP: {}'.format(article.get('slugline', ''))

        # Any Finance category stories that have a genre of feature
        if category == 'F' and [x for x in article.get('genre', []) if x['qcode'] == 'Feature']:
            if not article.get('slugline', '').startswith('FINEX:'):
                slugline = 'FINEX: {}'.format(article.get('slugline', ''))

        return slugline[:24] if kwargs.get('truncate', False) else slugline
