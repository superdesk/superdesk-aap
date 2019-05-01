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


def clean_string(str):
    """
    Replaces a selected group of unicode characters with alternatives
    :param str:
    :return: cleaned string
    """

    def get_translation_table():
        return ''.maketrans({'‘': '\'',  # 8216
                             '’': '\'',  # 8217
                             '‚': '\'',  # 8218
                             '‛': '\'',  # 8219
                             '“': '"',   # 8220
                             '”': '"',   # 8221
                             '‟': '"',   # 8223
                             '′': '\'',  # 8242
                             '″': '"',   # 8243
                             '‶': '"',   # 8246
                             '‵': '\'',  # 8245
                             'ˮ': '"',   # 750
                             '´': '\'',  # 180
                             'ʹ': '\'',  # 697
                             'ʻ': '\'',  # 699
                             'ʼ': '\'',  # 700
                             'ʺ': '"',   # 698
                             '̀': '\'',   # 768
                             '́': '\''    # 769
                             })

    return str.translate(get_translation_table()) if str else None


def to_ascii(input_str):
    try:
        return unidecode.unidecode(input_str) if input_str else ''
    except:
        logger.exception('Cannot convert input {} to ascii'.format(input_str))
        return input_str
