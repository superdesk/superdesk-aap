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
from planning.assignments.assignments_history import ASSIGNMENT_HISTORY_ACTIONS
from eve.utils import ParsedRequest
from flask import json
from flask import current_app as app
import requests
from lxml import etree
from superdesk.celery_task_utils import get_lock_id
from superdesk.lock import lock, unlock
from copy import deepcopy
from eve.utils import config
from bson import ObjectId

logger = logging.getLogger(__name__)


class FullfillImageAssignments(superdesk.Command):
    # The headers returned by the login request to the DC Rest service
    dc_headers = dict()

    def _dc_login(self):
        """
        Function will log into the DC system rest API and save the response headers
        :return:
        """
        url = app.config.get('DC_URL')
        username = app.config.get('DC_USERNAME')
        password = app.config.get('DC_PASSWORD')

        response = requests.get(url + '/?login[username]={}&login[password]={}'.format(username, password))
        response.raise_for_status()

        self.dc_headers = response.headers

    def _get_dc_image_by_id(self, collection, id):
        """
        This function given a DC collection and the DC id of an image will return the meta data from DC for that image
        :param collection:
        :param id:
        :return: The XML response that should contain the metadata for the single image
        """
        url = app.config.get('DC_URL')

        if not self.dc_headers:
            try:
                self._dc_login()
            except Exception as ex:
                logger.exception(ex)
                return None

        retries = 0
        while retries < 3:
            try:
                response = requests.get(url + '/archives/{}?search_docs[query]=id%3d'
                                              '{}&search_docs[format]=full'.format(collection, id),
                                        headers={'cookie': self.dc_headers.get('Set-Cookie')})
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                logger.exception(e)
                try:
                    self._dc_login()
                except requests.exceptions.RequestException:
                    logger.error('DC login failed')
                retries += 1
        if retries == 3:
            logger.error('Failed to get image assignment from DC {}'.format(id))
            return None
        return etree.fromstring(response.content)

    def _get_dc_images_by_field(self, archive, value):
        url = app.config.get('DC_URL')

        if not self.dc_headers:
            try:
                self._dc_login()
            except Exception as ex:
                logger.exception(ex)
                return None

        here_now = utc_to_local(app.config['DEFAULT_TIMEZONE'], utcnow())
        start = (here_now - timedelta(days=2)).strftime('%Y%m%d')

        retries = 0
        while retries < 3:
            try:
                response = requests.get(url + '/archives/{}?search_docs[query]='
                                              '({}%3D{})%26(MODDATE%3E{})'
                                              '&search_docs[format]=full'.format(archive,
                                                                                 app.config['DC_SEARCH_FIELD'],
                                                                                 value, start),
                                        headers={'cookie': self.dc_headers.get('Set-Cookie')})
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                logger.exception(e)
                try:
                    self._dc_login()
                except requests.exceptions.RequestException:
                    logger.error('DC login failed')
                retries += 1
        if retries == 3:
            logger.error('Failed to get image by field from DC {}'.format(id))
            return None
        return etree.fromstring(response.content)

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
        Attempt to get the superdesk user that corresponds to the DC user that last modified the image, if that fails
        return the user that made the assignment originally
        :param assignment:
        :return:
        """
        dc_image = self._get_dc_image_by_id('imagearc', assignment.get('image').get('_id'))
        if dc_image is not None:
            doc = dc_image.find('./dc_rest_docs/dc_rest_doc')
            if doc is not None:
                modified_by = doc.find('./dcdossier').attrib.get('modified_by')
                if modified_by and not modified_by == 'system':
                    user_service = superdesk.get_resource_service('users')
                    user = user_service.find_one(req=None, username=modified_by)
                    if user:
                        logger.info('Setting fulfillment user for {} to {}'.format(assignment.get('image').get('_id'),
                                                                                   user.get('username')))
                        return {'proxy_user': user.get('_id')}
        assigned_to = assignment.get('assignment').get('assigned_to')
        # return the assignor user or the assignor desk, if nothing else available
        return {'proxy_user': assigned_to.get('assignor_user', assigned_to.get('assignor_desk'))}

    def _extract_user(self, image):
        """
        Given an image dossier extract the user that modified it
        :param image:
        :return:
        """
        dossier = image.find('./dc_rest_docs/dc_rest_doc/dcdossier')
        if dossier is not None:
            modified_by = dossier.attrib.get('modified_by')
        if modified_by is not None and not modified_by == 'system':
            user_service = superdesk.get_resource_service('users')
            user = user_service.find_one(req=None, username=modified_by)
            if user:
                return user
        return None

    def _check_in_progress(self, assignments, complete):
        """
        Check the AAP Image Pool for any assignments that may be in progress
        :param assignments:
        :return:
        """
        in_progress_assignments = list()
        in_list = set()
        for assignment in assignments:
            # If we have marked the assignment complete ignore it
            if assignment.get('_id') in complete:
                continue
            if assignment.get('assigned_to', {}).get('state') == ASSIGNMENT_WORKFLOW_STATE.ASSIGNED:
                # look in the AAP Image pool
                dc_images = self._get_dc_images_by_field('aapimage', assignment.get('_id'))
                if dc_images is not None:
                    count = dc_images.find('./doc_count')
                    if count is not None and int(count.text) > 0:
                        logger.info('Found in progress items in aapimage for {}'.format(assignment.get('_id')))
                        user = self._extract_user(dc_images)
                        in_list.add(assignment.get('_id'))
                        in_progress_assignments.append({'assignment': assignment, 'user': user})
                        continue
                # look in the picedit pool
                dc_images = self._get_dc_images_by_field('picedit', assignment.get('_id'))
                if dc_images is not None:
                    count = dc_images.find('./doc_count')
                    if count is not None and int(count.text) > 0:
                        logger.info('Found in progress items in picedit for {}'.format(assignment.get('_id')))
                        user = self._extract_user(dc_images)
                        if assignment.get('_id') not in in_list:
                            in_list.add(assignment.get('_id'))
                            in_progress_assignments.append({'assignment': assignment, 'user': user})
        return in_progress_assignments

    def _mark_as_in_progress(self, assignments):
        """
        Set the assignment state for that passed assignments to in progress
        :param assignments:
        :return:
        """
        service = superdesk.get_resource_service('assignments')
        for assignment in assignments:
            logger.warning('Marking assignment {} in progress'.format(assignment.get('assignment').get('_id')))
            assignment.get('assignment')[config.ID_FIELD] = ObjectId(assignment.get('assignment')[config.ID_FIELD])
            assigned_to = assignment.get('assignment').get('assigned_to')
            updates = {'assigned_to': deepcopy(assigned_to)}
            updates['assigned_to']['state'] = ASSIGNMENT_WORKFLOW_STATE.IN_PROGRESS
            try:
                service.patch(assignment.get('assignment')[config.ID_FIELD], updates)
                if assignment.get('user') is None:
                    updates['proxy_user'] = assigned_to.get('assignor_user', assigned_to.get('assignor_desk'))
                else:
                    updates['proxy_user'] = assignment.get('user').get(config.ID_FIELD)
                superdesk.get_resource_service('assignments_history').on_item_updated(
                    updates, assignment.get('assignment'), ASSIGNMENT_HISTORY_ACTIONS.START_WORKING)
            except Exception as ex:
                logger.exception(ex)

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

        complete = [c.get('assignment').get('_id') for c in completed_assignments]

        # check if any of the outstanding assignments are in either the picedit or aapimage pools
        in_progress_assignments = self._check_in_progress(assignments, complete)

        self._mark_as_in_progress(in_progress_assignments)

        unlock(lock_name)
        logger.info('Finished fulfilling assignments')


superdesk.command('app:fullfill_image_assignments', FullfillImageAssignments())
