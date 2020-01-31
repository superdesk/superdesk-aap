# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from .import_text_archive import AppImportTextArchiveCommand  # noqa
from .socket_load_test import SocketLoadTestCommand  # noqa
from .socket_listener import SocketListenerCommand  # noqa
from .remote_sync import RemoteSyncCommand  # noqa
from .fix_items_expired import FixItemsExpiry  # noqa
from .export_legal_archive_to_archived import ExportLegalArchiveToArchived  # noqa
from .export_to_newroom import ExportToNewsroom  # noqa
from .import_sport_calendar import ImportSportCalendarDoc  # noqa
from .fulfill_image_assignments import FullfillImageAssignments  # noqa
from superdesk.celery_app import celery
from superdesk.default_settings import celery_queue
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


def init_app(app):
    if app.config.get('ENABLE_FULFILL_ASSIGNMENTS', False):
        if not app.config.get('CELERY_TASK_ROUTES').get('aap.commands.fulfill_assignments'):
            app.config['CELERY_TASK_ROUTES']['aap.commands.fulfill_assignments'] = {
                'queue': celery_queue('expiry'),
                'routing_key': 'expiry.fulfill_assignments'
            }

        if not app.config.get('CELERY_BEAT_SCHEDULE').get('planning:fulfill_assignments'):
            app.config['CELERY_BEAT_SCHEDULE']['planning:fulfill_assignments'] = {
                'task': 'aap.commands.fulfill_assignments',
                'schedule': timedelta(minutes=5)
            }


@celery.task(soft_time_limit=600)
def fulfill_assignments():
    FullfillImageAssignments().run()
