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
import superdesk
from superdesk.resource import Resource
from apps.archive.common import ARCHIVE
from superdesk.utc import utcnow, get_date
from eve.utils import date_to_str, ParsedRequest
from superdesk import get_resource_service, config
from datetime import datetime, timedelta
from superdesk.lock import lock, unlock
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE


logger = logging.getLogger(__name__)


def compare_dictionaries(dict1, dict2):
    """
    Compare two dict.
    :param dict1:
    :param dict2:
    :return:
    """
    if dict1 is None or dict2 is None:
        return False

    if type(dict1) is not dict or type(dict2) is not dict:
        return False

    dicts_are_equal = True

    for key in dict1.keys():
        if isinstance(dict1[key], dict):
            dicts_are_equal = dicts_are_equal and key in dict2 and compare_dictionaries(dict1[key], dict2[key])
        else:
            dicts_are_equal = dicts_are_equal and key in dict2 and (dict1[key] == dict2[key])

    return dicts_are_equal


class LegalArchiveConsistencyResource(Resource):
    schema = {
        'started_at': {
            'type': 'datetime'
        },
        'completed_at': {
            'type': 'datetime'
        },
        'archive': {
            'type': 'integer'
        },
        'legal': {
            'type': 'integer'
        },
        'archive_only': {
            'type': 'list'
        },
        'identical': {
            'type': 'integer'
        },
        'resource': {
            'type': 'string'
        },
        'difference': {
            'type': 'dict'
        }
    }

    item_methods = []
    resource_methods = []
    internal_resource = True


class LegalArchiveConsistencyCheckCommand(superdesk.Command):

    option_list = {
        superdesk.Option('--input_date', '-i', dest='input_date', default=utcnow()),
        superdesk.Option('--days_to_process', '-d', dest='days_to_process', default=1),
        superdesk.Option('--page_size', '-p', dest='page_size', default=500),
    }

    default_page_size = 500
    archive_ids = []

    def run(self, input_date, days_to_process, page_size):

        lock_name = 'legal_archive:consistency'
        self.default_page_size = int(page_size)
        days_to_process = int(days_to_process)
        if not lock(lock_name, expire=610):
            logger.warn("Task: {} is already running.".format(lock_name))
            return

        try:
            logger.info('Input Date: {}  ---- Days to Process: {}'.format(input_date, days_to_process))
            self.check_legal_archive_consistency(input_date, days_to_process)
            self.check_legal_archive_version_consistency()
            self.check_legal_archive_queue_consistency()
            logger.info('Completed the legal archive consistency check.')
        except:
            logger.exception("Failed to execute LegalArchiveConsistencyCheckCommand")
        finally:
            unlock(lock_name)

    def check_legal_archive_consistency(self, input_date, days_to_process):
        start_time = utcnow()
        start_date, end_date = self._get_date_range(input_date, days_to_process)
        logger.info('start_date: {}  ---- end_date: {}'.format(start_date, end_date))
        archive_items = self._get_archive_items(start_date, end_date)
        if archive_items:
            self.archive_ids = list(archive_items.keys())

        logger.info("Found {} items in archive.".format(len(archive_items)))
        legal_archive_items = self._get_legal_archive_items(self.archive_ids)
        logger.info("Found {} items in legal archive.".format(len(legal_archive_items)))
        record = self.check_consistency('archive', archive_items, legal_archive_items)
        record['completed_at'] = utcnow()
        record['started_at'] = start_time
        get_resource_service('legal_archive_consistency').post([record])

    def check_legal_archive_version_consistency(self):
        start_time = utcnow()
        if not self.archive_ids:
            return

        archive_items = self._get_archive_version_items(self.archive_ids)
        logger.info("Found {} items in archive versions.".format(len(archive_items)))
        legal_archive_items = self._get_legal_archive_version_items(self.archive_ids)
        logger.info("Found {} items in legal archive versions.".format(len(legal_archive_items)))
        record = self.check_consistency('archive_versions', archive_items, legal_archive_items)
        record['completed_at'] = utcnow()
        record['started_at'] = start_time
        get_resource_service('legal_archive_consistency').post([record])

    def check_legal_archive_queue_consistency(self):
        start_time = utcnow()
        if not self.archive_ids:
            return

        archive_items = self._get_publish_queue_items(self.archive_ids)
        logger.info("Found {} items in publish queue.".format(len(archive_items)))
        legal_archive_items = self._get_legal_publish_queue_items(self.archive_ids)
        logger.info("Found {} items in legal publish queue.".format(len(archive_items)))
        record = self.check_consistency('publish_queue', archive_items, legal_archive_items)
        record['completed_at'] = utcnow()
        record['started_at'] = start_time
        get_resource_service('legal_archive_consistency').post([record])

    def check_consistency(self, resource, archive_items, legal_items):
        record = {'resource': resource, 'archive': len(archive_items), 'legal': len(legal_items)}
        archive_ids = set(archive_items.keys())
        legal_ids = set(legal_items.keys())
        record['archive_only'] = list(archive_ids - legal_ids)
        diff = {}
        for k, v in archive_items.items():
            if not compare_dictionaries(v, legal_items.get(k)):
                diff[k.replace('.', ':')] = {'archive': v, 'legal': legal_items.get(k)}

        record['difference'] = diff
        record['identical'] = len(archive_items) - len(diff)
        return record

    def __get_key(self, item):
        return item.get(config.ID_FIELD)

    def __get_version_key(self, item):
        return '{}-{}'.format(item.get('_id_document'), item.get(config.VERSION))

    def _get_items(self, resource, query, sort, keys, callback):
        req = ParsedRequest()
        cursor = get_resource_service(resource).get_from_mongo(req=req, lookup=query)
        count = cursor.count()
        no_of_buckets = len(range(0, count, self.default_page_size))
        items = {}
        req.sort = sort

        for bucket in range(0, no_of_buckets):
            skip = bucket * self.default_page_size
            logger.info('Page : {}, skip: {}'.format(bucket + 1, skip))
            cursor = get_resource_service(resource).get_from_mongo(req=req, lookup=query)
            cursor.skip(skip)
            cursor.limit(self.default_page_size)
            cursor = list(cursor)
            items.update({callback(item): {key: item.get(key)
                         for key in keys if key in item} for item in cursor})
        return items

    def _get_archive_items(self, start_date, end_date):
        """
        Gets the archive items from the mongo database that were updated today
        :return:
        """
        query = {
            '$and': [
                {'_updated': {'$gte': date_to_str(start_date), '$lte': date_to_str(end_date)}},
                {ITEM_STATE: {'$in': [
                    CONTENT_STATE.CORRECTED,
                    CONTENT_STATE.PUBLISHED,
                    CONTENT_STATE.KILLED,
                    CONTENT_STATE.RECALLED
                ]}}
            ]
        }

        return self._get_items(ARCHIVE, query, '_created',
                               [config.VERSION, 'versioncreated', 'state'],
                               self.__get_key)

    def _get_legal_archive_items(self, archive_ids):
        """
        Get the legal archive items
        :param list archive_ids:
        :return dict:
        """
        if not archive_ids:
            return {}

        query = {
            '$and': [{'_id': {'$in': archive_ids}}]
        }

        return self._get_items('legal_archive', query, '_created',
                               [config.VERSION, 'versioncreated', 'state'],
                               self.__get_key)

    def _get_archive_version_items(self, archive_ids):
        """
        Get the archive version items
        :param list archive_ids:
        :return dict:
        """
        if not archive_ids:
            return {}

        query = {
            '$and': [{'_id_document': {'$in': archive_ids}}]
        }

        return self._get_items('archive_versions', query, '_created',
                               [config.VERSION, 'versioncreated', 'state'],
                               self.__get_version_key)

    def _get_legal_archive_version_items(self, archive_ids):
        """
        Get the legal archive version items
        :param list archive_ids:
        :return dict:
        """
        if not archive_ids:
            return {}

        query = {
            '$and': [{'_id_document': {'$in': archive_ids}}]
        }

        return self._get_items('legal_archive_versions', query, '_created',
                               [config.VERSION, 'versioncreated', 'state'],
                               self.__get_version_key)

    def _get_publish_queue_items(self, archive_ids):
        """
        Get the publish queue items
        :param list archive_ids:
        :return dict:
        """
        if not archive_ids:
            return {}

        query = {
            '$and': [{'item_id': {'$in': archive_ids}}]
        }

        return self._get_items('publish_queue', query, '_created',
                               ['published_seq_num', 'publishing_action',
                                'unique_name', 'item_version',
                                'state', 'content_type'],
                               self.__get_key)

    def _get_legal_publish_queue_items(self, archive_ids):
        """
        Get the legal publish queue items
        :param list archive_ids:
        :return dict:
        """
        if not archive_ids:
            return {}

        query = {
            '$and': [{'item_id': {'$in': archive_ids}}]
        }

        return self._get_items('legal_publish_queue', query, '_created',
                               ['published_seq_num', 'publishing_action',
                                'unique_name', 'item_version',
                                'state', 'content_type'],
                               self.__get_key)

    def _get_date_range(self, input_date, days_to_process=1):
        """
        Calculate the date range to process
        :param datetime input_date:
        :param int days_to_process:
        :return:
        """
        if not input_date:
            input_date = utcnow()
        elif isinstance(input_date, str):
            input_date = get_date(input_date)
        elif not isinstance(input_date, datetime):
            raise ValueError("Invalid Input Date.")

        end_date = input_date
        start_date = (end_date - timedelta(days=int(days_to_process))).replace(hour=0, minute=0,
                                                                               second=0, microsecond=0)

        return start_date, end_date


superdesk.command('legal_archive:consistency_check', LegalArchiveConsistencyCheckCommand())
