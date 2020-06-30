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
from bson import json_util


def load_codes(filename):
    with open(filename, 'rb') as f:
        codes_bytes = f.read()
        codes = json_util.loads(codes_bytes.decode('UTF-8'))
        return codes


dirname = os.path.dirname(os.path.realpath(__file__))
data_media_topics = os.path.join(dirname, 'data', 'media_topics.json')
aap_media_topics = load_codes(data_media_topics)


def init_app(app):
    """Provides a mechanism to overload the media topics

    :param app:
    :return:
    """

    # Nothing to extend
    if not app.mediatopics:
        return

    # Update the topics with any local versions
    for topic in aap_media_topics:
        app.mediatopics.media_topic_map[topic.get('qcode')] = topic

    # clear the lookup maps
    app.mediatopics.clear_maps()

    # re-generate the lookup maps
    mediatopics = [t for (_k, t) in app.mediatopics.media_topic_map.items()]
    app.mediatopics.generate_mediatopic_to_subject_map(mediatopics)
