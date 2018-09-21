# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2018 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import json
from eve.utils import ParsedRequest
from superdesk import get_resource_service
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE, ITEM_TYPE, CONTENT_TYPE, PUBLISH_STATES
from superdesk.errors import StopDuplication, InvalidStateTransitionError
from .am_service_content import am_service_content


def am_snaps_auto_publish(item, **kwargs):
    """AM snaps Auto Publish.

    :param item:
    :param kwargs:
    :return:
    """

    if item.get(ITEM_STATE) not in PUBLISH_STATES:
        raise InvalidStateTransitionError(message='Internal Destination auto publish macro can '
                                                  'only be called after publishing the item.')

    if item.get(ITEM_TYPE) != CONTENT_TYPE.TEXT or \
            item[ITEM_STATE] in {CONTENT_STATE.KILLED, CONTENT_STATE.RECALLED} or \
            not item.get('sms_message'):
        raise StopDuplication()

    # set the content as per AM rules
    item = am_service_content(item, **kwargs)

    sms_message = item.pop('sms_message', None)
    item.pop('body_footer', None)
    item.pop('associations', None)
    item['anpa_take_key'] = 'snap'
    for field in ['abstract', 'body_html']:
        item[field] = sms_message

    # need to check that a story with the same sms_message has not been published to SMS before
    query = {
        "query": {
            "filtered": {
                "query": {
                    "query_string": {
                        "query": "abstract:(\"{}\") AND anpa_take_key:snap".format(item['abstract'])
                    }
                },
                "filter": {
                    "and": [
                        {"terms": {"state": [CONTENT_STATE.PUBLISHED, CONTENT_STATE.CORRECTED]}},
                        {"term": {"genre.qcode": "AM Service"}},
                    ]
                }
            }
        }
    }

    req = ParsedRequest()
    req.args = {'source': json.dumps(query)}
    published = get_resource_service('published').get(req=req, lookup=None)
    if published and published.count():
        raise StopDuplication

    new_id = get_resource_service('archive').duplicate_content(item, state='routed')
    get_resource_service('archive_publish').patch(
        id=new_id,
        updates={ITEM_STATE: item.get(ITEM_STATE), 'auto_publish': True}
    )

    # raise stop duplication on successful completion so that
    # internal destination superdesk.internal_destination.handle_item_published
    # will not duplicate the item.
    raise StopDuplication()


name = 'am_snaps_auto_publish'
label = 'AM Snaps Auto Publish'
callback = am_snaps_auto_publish
access_type = 'backend'
action_type = 'direct'
