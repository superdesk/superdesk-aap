# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

"""IPTC module"""

import os
from datetime import datetime
from superdesk.io.iptc import load_codes
from superdesk.io.iptc import subject_codes


dirname = os.path.dirname(os.path.realpath(__file__))
data_subject_codes = os.path.join(dirname, 'data', 'aap_subject_codes.json')
aap_subject_codes = load_codes(data_subject_codes)


def init_app(app):
    last_modified = datetime(2016, 7, 28)
    app.subjects.register(aap_subject_codes, last_modified)
    subject_codes.update(aap_subject_codes)
