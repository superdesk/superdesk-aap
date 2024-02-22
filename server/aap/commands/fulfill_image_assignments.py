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
from superdesk.utc import utcnow, utc_to_local
from datetime import timedelta
from planning.common import ASSIGNMENT_WORKFLOW_STATE
from eve.utils import ParsedRequest
from flask import json
from flask import current_app as app
from superdesk.celery_task_utils import get_lock_id
from superdesk.lock import lock, unlock
from bson import ObjectId

logger = logging.getLogger(__name__)


class FullfillImageAssignments(superdesk.Command):

    def _get_outstanding_photo_assignments(self):
        """
        Check for any picture assignments, assigned and scheduled in the last day or so
        :return: The Id of any sheduled picure assignments
        """
        service = superdesk.get_resource_service('assignments')
        query = {
            'query': {
                'bool': {
                    'must': [
                        {
                            'terms': {
                                'assigned_to.state': [
                                    ASSIGNMENT_WORKFLOW_STATE.ASSIGNED,
                                    ASSIGNMENT_WORKFLOW_STATE.IN_PROGRESS
                                ]
                            }
                        },
                        {
                            'term': {
                                'planning.g2_content_type': 'picture'
                            }
                        },
                        {
                            'range': {
                                'planning.scheduled': {
                                    'gte': 'now-2d'
                                }
                            }
                        }
                    ],
                    'must_not': {
                        'exists': {
                            'field': 'lock_user'
                        }
                    }
                }
            }
        }
        req = ParsedRequest()
        req.args = {'source': json.dumps(query)}
        req.max_results = 500

        assignments = service.get(req=req, lookup=None)
        if assignments.count() > 0:
            logger.warning('Found {} outstanding assignments in planning'.format(assignments.count()))
        else:
            logger.warning('No outstanding assignments found')
        return assignments

    def _check_complete(self, assignments):
        """
        Using the photos API Look for any images that have a configured field that match the id of
        the assignment that have been created in the last day
        :param assignments:
        :return: A list of dictionaries that contain the assignment and matching image
        """
        complete_assignments = list()

        # Restrict the search for potentialy complete assignments to the last couple of days
        here_now = utc_to_local(app.config['DEFAULT_TIMEZONE'], utcnow())
        start = (here_now - timedelta(days=5)).strftime('%Y-%m-%d')
        end = (here_now + timedelta(days=1)).strftime('%Y-%m-%d')

        service = superdesk.get_resource_service('aapmm')
        rq = ParsedRequest()
        for assignment in assignments:
            rq.args = {'source': json.dumps({"query": {
                "filtered": {"query": {
                    "query_string": {"query": "{}:{}".format(app.config['DC_SEARCH_FIELD'], assignment.get('_id'))}}}},
                "post_filter": {'and': [{'range': {'firstcreated': {'gte': start, 'lte': end}}}]}
            })}
            images = service.get(req=rq, lookup=None)
            # there may be multiple images that make up the assignment, we only need on to mark the
            # assignment as complete
            if images.count() > 0:
                complete_assignments.append({'assignment': assignment, 'image': images[0]})
        logger.warning('Found {} completed assignments on the photos system'.format(len(complete_assignments)))
        return complete_assignments

    def _get_image_modifier(self, assignment):
        """
        The credit is given to the assignor
        :param assignment:
        :return:
        """
        assigned_to = assignment.get('assignment').get('assigned_to')
        # return the assignor user or the assignor desk, if nothing else available
        return {'proxy_user': assigned_to.get('assignor_user', assigned_to.get('assignor_desk'))}

    def _mark_as_complete(self, assignments):
        """
        Mark the passed assignments as complete
        :param assignments:
        :return:
        """
        service = superdesk.get_resource_service('assignments_complete')
        for assignment in assignments:
            user = self._get_image_modifier(assignment)
            try:
                logger.warning('Marking assignment {} as complete'.format(assignment.get('assignment').get('_id')))
                service.patch(ObjectId(assignment.get('assignment').get('_id')), user)
            except Exception as ex:
                logger.exception(ex)

    def run(self, ):
        logger.info('Starting to fullfill assignments.')

        lock_name = get_lock_id('planning', 'fulfill_assignments')
        if not lock(lock_name, expire=610):
            logger.info('{} Fulfill Assignments task is already running')
            return

        # Get a list of the outstanding photo assignments
        assignments = list(self._get_outstanding_photo_assignments())

        # query for any images available from the image site API with those assigment id's
        completed_assignments = self._check_complete(assignments)

        self._mark_as_complete(completed_assignments)

        unlock(lock_name)
        logger.info('Finished fulfilling assignments')


superdesk.command('app:fullfill_image_assignments', FullfillImageAssignments())
