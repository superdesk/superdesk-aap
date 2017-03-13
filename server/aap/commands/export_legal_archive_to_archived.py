# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015, 2016, 2017 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
import superdesk
import json

from superdesk.celery_task_utils import get_lock_id
from superdesk.lock import lock, unlock
from superdesk import get_resource_service
from eve.utils import ParsedRequest
from apps.legal_archive import LEGAL_ARCHIVE_NAME

from copy import deepcopy

logger = logging.getLogger(__name__)


class ExportLegalArchiveToArchived(superdesk.Command):
    """Export legal archive content to archived.

    Only the content for the desk provided is exported.
    By default this is the 'COMMISSION' desk
    """

    default_desk = 'COMMISSION'

    option_list = [
        superdesk.Option('--desk', '-d', dest='desk', required=False)
    ]

    def run(self, desk=None):
        if desk:
            self.default_desk = desk

        logger.info('Starting to export {} desk legal archive content to archived'.format(self.default_desk))

        lock_name = get_lock_id('legal_archive', 'export_to_archived')
        if not lock(lock_name, expire=610):
            logger.info('Export legal archive to archived task is already running.')
            return

        try:
            list_ids = self._export_to_archived()
        finally:
            unlock(lock_name)

        if list_ids:
            logger.info('Completed exporting {} {} desk documents from legal archive to text archived'.format(
                len(list_ids),
                self.default_desk)
            )
        else:
            logger.info('Completed but nothing was exported...')

    def _get_desk_id(self):
        """Returns the ObjectID of the desk

        :return str: The ObjectID for the desk provided, or None if the desk was not found
        """
        logger.info('Fetching the ObjectID for the desk {}.'.format(self.default_desk))
        query = {'name': self.default_desk}
        req = ParsedRequest()
        req.where = json.dumps(query)

        desk_service = get_resource_service('desks')
        desk_item = list(desk_service.get_from_mongo(req=req, lookup=None))
        if not desk_item:
            logger.error('Failed to find the ObjectID for the provided desk {}'.format(self.default_desk))
            return None

        desk_id = desk_item[0]['_id']
        logger.info('ObjectID for the desk {} is {}.'.format(self.default_desk, desk_id))
        return desk_id

    def _export_to_archived(self):
        """Export legal archive content to archived.

        Copy all legal archive content that belongs to the desk provided
        into archived

        :return list: list of ids imported into archived, else if an error occurred reply with an empty list
        """
        logger.info('Exporting legal archive content to archived.')
        items = list()
        try:
            desk_id = self._get_desk_id()
            if not desk_id:
                return []

            for item in self._get_items():
                items.append(self._generate_archived_item(item, desk_id))

            return self._add_to_archived(items)
        except Exception as e:
            logging.exception('Failed to export legal archive content to archived. {}'.format(e))

        return []

    def _get_items(self):
        """Get items from the LegalArchive that belong to the COMMISSION desk

        :return: list: list of legal archive content
        """
        logger.info('Fetching legal archive content for the {} desk'.format(self.default_desk))

        query = {'task.desk': self.default_desk, 'type': 'text'}
        req = ParsedRequest()
        req.where = json.dumps(query)

        legal_archive_service = get_resource_service(LEGAL_ARCHIVE_NAME)

        legal_items = list(legal_archive_service.get_from_mongo(req=req, lookup=None))

        if legal_items:
            logger.info(
                'Found {} items in the legal archive for the {} desk'.format(
                    len(legal_items),
                    self.default_desk)
            )
        else:
            logger.warning('Failed to find any {} desk items in the legal archive'.format(self.default_desk))
            legal_items = []

        return legal_items

    def _generate_archived_item(self, legal_item, desk_id):
        """Convert the legal archive content for the archived content

        :param dict legal_item: legal archive item
        :param str desk_id: The ObjectID for the desk provided
        :return dict: archived item converted from legal archive item
        """
        archived_item = deepcopy(legal_item)

        archived_item.pop('task')
        archived_item['task'] = {'desk': desk_id}

        archived_item['item_id'] = archived_item['_id']
        archived_item.pop('_id')

        archived_item.pop('linked_in_packages', None)

        archived_item['last_published_version'] = True
        archived_item['moved_to_legal'] = True
        archived_item['is_take_item'] = False

        return archived_item

    def _add_to_archived(self, items):
        """Post the supplied list of items to the archived

        :param list items: list of archived items to add
        :return list: list of ids added to the archived
        """
        archived_service = get_resource_service('archived')
        return archived_service.post(items)


superdesk.command('legal_archive:export_to_archived', ExportLegalArchiveToArchived())
