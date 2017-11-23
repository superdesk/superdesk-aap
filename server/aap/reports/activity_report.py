# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from datetime import datetime, timedelta
import logging
from eve.utils import date_to_str
from flask import current_app as app
import superdesk
from superdesk import Resource
from superdesk.lock import lock, unlock
from superdesk.utc import utcnow, get_date

logger = logging.getLogger(__name__)


class ActivityReportResource(Resource):
    schema = {
        'users': Resource.rel('users'),
        'create_count': {
            'type': 'integer'
        },
        'submit_count': {
            'type': 'integer'
        },
        'publish_count': {
            'type': 'integer'
        },
        'update_count': {
            'type': 'integer'
        },
        'total_count': {
            'type': 'integer'
        },
        'activity_date': {
            'type': 'datetime'
        }
    }

    item_methods = []
    resource_methods = []
    internal_resource = True


class GenerateActivityCountReport(superdesk.Command):

    option_list = {
        superdesk.Option('--input_date', '-i', dest='input_date', default=utcnow()),
        superdesk.Option('--days_to_process', '-d', dest='days_to_process', default=7),
    }

    def run(self, input_date, days_to_process=7):
        lock_name = 'report:generate_activity_count'
        if not lock(lock_name, expire=610):
            logger.warning("Task: {} is already running.".format(lock_name))
            return

        try:
            start_date, end_date = self._get_date_range(input_date, days_to_process)

            pipeline = [
                {
                    "$match": {
                        "_created": {
                            "$gte": date_to_str(start_date),
                            "$lte": date_to_str(end_date)
                        },
                        "user_id": {"$ne": None},
                        "original_item_id": {"$exists": False}
                    }
                },

                {
                    "$group": {
                        "_id": "$item_id",
                        "operations": {
                            "$push": {
                                "operation": "$operation",
                                "user_id": "$user_id",
                                "created": "$_created"
                            }
                        }
                    }
                },

                {
                    "$match": {
                        "operations.operation": {"$ne": "spike"}
                    }
                },

                {
                    "$unwind": {
                        "path": "$operations"
                    }
                },

                {
                    "$project": {
                        "user_id": "$operations.user_id",
                        "operation": "$operations.operation",
                        "created": "$operations.created",
                        "_id": 1
                    }
                },

                {
                    "$group": {
                        "_id": {
                            "activity_date": {
                                "$dateToString": {
                                    "format": "%Y-%m-%d",
                                    "date": "$created"
                                }
                            },
                            "user_id": "$user_id"
                        },
                        "create_count": {"$sum": {"$cond": [{"$eq": ["$operation", "create"]}, 1, 0]}},
                        "update_count": {"$sum": {"$cond": [{"$eq": ["$operation", "update"]}, 1, 0]}},
                        "submit_count": {"$sum": {"$cond": [{"$eq": ["$operation", "move"]}, 1, 0]}},
                        "publish_count": {
                            "$sum": {"$cond": [{"$in": ["$operation", ["publish", "correct", "kill"]]}, 1, 0]}
                        },
                        "total_count": {"$sum": {"$cond": [
                            {"$in": ["$operation", ["move", "create", "update", "publish", "correct", "kill"]]}, 1, 0]}}
                    }
                },

                {
                    "$project": {
                        "_id": 0,
                        "user_id": "$_id.user_id",
                        "activity_date": "$_id.activity_date",
                        "create_count": 1,
                        "update_count": 1,
                        "submit_count": 1,
                        "publish_count": 1,
                        "total_count": 1
                    }
                }
            ]

            items = list(app.data.mongo.aggregate('archive_history', pipeline, {}))

            if items:
                self._process_report(items)

            return items
        except:
            logger.exception("Failed to execute GenerateActivityCountReport")
        finally:
            unlock(lock_name)

    def _process_report(self, items):
        """To insert/update the activity report

        :param list items:
        """
        service = superdesk.get_resource_service('activity_report')
        new_items = []

        for item in items:
            item['activity_date'] = get_date(item['activity_date'])
            existing_item = service.find_one(req=None,
                                             activity_date=item['activity_date'],
                                             user_id=item['user_id'])
            if existing_item:
                service.patch(existing_item['_id'], item)
            else:
                new_items.append(item)

        if new_items:
            service.post(new_items)

    def _get_date_range(self, input_date, days_to_process=1):
        """Calculate the date range to process

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


superdesk.command('report:activitycount', GenerateActivityCountReport())
