# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
import json
import superdesk

from datetime import timedelta
from flask import current_app as app
from apps.archive.archive import SOURCE as ARCHIVE
from eve.utils import ParsedRequest, config, date_to_str
from superdesk import get_resource_service
from superdesk.celery_task_utils import get_lock_id
from superdesk.lock import lock, unlock
from superdesk.metadata.item import CONTENT_STATE, ITEM_STATE
from superdesk.utc import utcnow


logger = logging.getLogger(__name__)


class FixItemsExpiry(superdesk.Command):
    expiry_minutes = 60 * 24 * 3
    default_page_size = 500

    option_list = [
        superdesk.Option('--page-size', '-p', dest='page_size', required=False)
    ]

    def run(self, page_size=None):
        logger.info('Starting to fix expired content.')

        if app.settings.get('PUBLISHED_CONTENT_EXPIRY_MINUTES'):
            self.expiry_minutes = app.settings['PUBLISHED_CONTENT_EXPIRY_MINUTES']

        if page_size:
            self.default_page_size = int(page_size)

        lock_name = get_lock_id('archive', 'fix_expired_content')
        if not lock(lock_name, expire=610):
            logger.info('Fix expired content task is already running.')
            return
        try:
            self.fix_items_expiry()
        finally:
            unlock(lock_name)

        logger.info('Completed fixing expired content.')

    def fix_items_expiry(self):
        """Fix the expired items
        """
        now = utcnow()
        logger.info('Fixing expired content.')
        for items in self.get_items(now):
            for item in items:
                self.process_items(item)

    def get_items(self, now):
        """Get the items from the archive collection that have expiry in future
        and state is published, corrected, killed

        :param datetime now: current date time
        :return list: list of expired items
        """
        logger.info('Fetching expired items from archive collection.')
        now = now + timedelta(minutes=self.expiry_minutes)

        query = {
            'expiry': {'$gte': date_to_str(now)},
            ITEM_STATE: {'$in': [
                CONTENT_STATE.PUBLISHED,
                CONTENT_STATE.CORRECTED,
                CONTENT_STATE.KILLED,
                CONTENT_STATE.RECALLED
            ]}
        }

        req = ParsedRequest()
        req.sort = '[("unique_id", 1)]'
        req.where = json.dumps(query)
        cursor = get_resource_service(ARCHIVE).get_from_mongo(req=req, lookup=None)
        count = cursor.count()
        no_of_pages = 0
        if count:
            no_of_pages = len(range(0, count, self.default_page_size))
            unique_id = cursor[0]['unique_id']
            logger.info('Number of items to modify: {}, pages={}'.format(count, no_of_pages))
        else:
            logger.info('No items to modify.')

        for page in range(0, no_of_pages):
            logger.info('Fetching items for page number: {} unique_id: {}'. format((page + 1), unique_id))
            req = ParsedRequest()
            req.sort = '[("unique_id", 1)]'
            if page == 0:
                query['unique_id'] = {'$gte': unique_id}
            else:
                query['unique_id'] = {'$gt': unique_id}

            req.where = json.dumps(query)
            req.max_results = self.default_page_size
            cursor = get_resource_service(ARCHIVE).get_from_mongo(req=req, lookup=None)
            items = list(cursor)
            if len(items) > 0:
                unique_id = items[len(items) - 1]['unique_id']

            logger.info('Fetched No. of Items: {} for page: {}'.format(len(items), (page + 1)))
            yield items

    def process_items(self, item):
        """Set the new expiry for the item

        :param dict item:
        """
        old_expiry = item['expiry']
        new_expiry = item['versioncreated'] + timedelta(minutes=self.expiry_minutes)
        try:
            get_resource_service(ARCHIVE).system_update(item[config.ID_FIELD], {'expiry': new_expiry}, item)
            logger.info('Updated the expiry date for id: {}. Old: {} New: {}'.format(item[config.ID_FIELD],
                                                                                     old_expiry,
                                                                                     new_expiry))
        except:
            logger.exception('Failed to update the expiry date for id: {}. '
                             'Old: {} New: {}'.format(item[config.ID_FIELD], old_expiry, new_expiry))


superdesk.command('app:fix_items_expiry', FixItemsExpiry())
