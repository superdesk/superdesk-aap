# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import os
from superdesk.macros import *  # noqa
from superdesk import register_jinja_filter


load_macros(os.path.realpath(os.path.dirname(__file__)), 'aap.macros')  # noqa


def escape_for_json(data):
    return data.translate(str.maketrans({
        "\\": "\\\\",
        "\"": "\\\""
    }))


def init_app(app):
    register_jinja_filter('escape_for_json', escape_for_json)
