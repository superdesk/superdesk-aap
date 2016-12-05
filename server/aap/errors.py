# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.errors import ParserError


class AAPParserError(ParserError):

    ParserError._codes.update({1100: 'ZCZC input could not be processed',
                               1101: 'News Bites input could not be processed',
                               1102: 'PDA Results input could not be processed'})

    @classmethod
    def ZCZCParserError(cls, exception=None, provider=None):
        return ParserError(1100, exception, provider)

    @classmethod
    def NewsBitesParserError(cls, exception=None, provider=None):
        return ParserError(1101, exception, provider)

    @classmethod
    def PDAResulstParserError(cls, exception=None, provider=None):
        return ParserError(1102, exception, provider)
