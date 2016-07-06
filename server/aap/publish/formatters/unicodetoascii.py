# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import unidecode
import logging


logger = logging.getLogger(__name__)


def to_ascii(input_str):
    try:
        return unidecode.unidecode(input_str)
    except:
        logger.exception('Cannot convert input {} to ascii'.format(input_str))
        return input_str
