# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import newrelic.agent
import logging

logger = logging.getLogger(__name__)


def init_app(app):
    try:
        app.on_pre_GET += on_pre_request_get_callback
        app.on_post_GET += on_post_request_get_callback
        app.on_pre_POST += on_pre_request_post_callback
        app.on_post_POST += on_post_request_post_callback
        app.on_pre_PATCH += on_pre_request_patch_callback
        app.on_post_PATCH += on_post_request_patch_callback
        app.on_pre_DELETE += on_pre_request_delete_callback
        app.on_post_DELETE += on_post_request_delete_callback
    except Exception:
        logger.error('Failed to start instrumentation.')


def on_pre_request_get_callback(resource, request, lookup):
    newrelic_start_transaction(resource, request, lookup, 'Get')


def on_post_request_get_callback(resource, request, lookup):
    newrelic_end_transaction(resource, request, lookup, 'Get')


def on_pre_request_post_callback(resource, request):
    newrelic_start_transaction(resource, request, None, 'Post')


def on_post_request_post_callback(resource, request, payload):
    newrelic_end_transaction(resource, request, payload, 'Post')


def on_pre_request_patch_callback(resource, request, payload):
    newrelic_start_transaction(resource, request, payload, 'Patch')


def on_post_request_patch_callback(resource, request, payload):
    newrelic_end_transaction(resource, request, payload, 'Patch')


def on_pre_request_delete_callback(resource, request, lookup):
    newrelic_start_transaction(resource, request, lookup, 'Delete')


def on_post_request_delete_callback(resource, request, lookup):
    newrelic_end_transaction(resource, request, lookup, 'Delete')


def newrelic_start_transaction(resource, request, lookup, method):
    name = resource
    group = 'Python/eve.endpoints/{}'.format(method)
    if not resource:
        return
    try:
        newrelic.agent.set_transaction_name(name, group=group)
    except Exception:
        logger.error('failed to start transaction name. {} --- {}'.format(resource, method))


def newrelic_end_transaction(resource, request, lookup, method):
    try:
        if not resource:
            return
        newrelic.agent.end_of_transaction()
    except Exception:
        logger.error('failed to end transaction name. {} --- {}'.format(resource, method))
