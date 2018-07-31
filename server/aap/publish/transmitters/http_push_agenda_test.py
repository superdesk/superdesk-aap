# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

"""Superdesk"""

from superdesk.tests import TestCase
from httmock import urlmatch, HTTMock
import json
from .http_push_agenda import HTTPAgendaPush
from planning import init_app as planning_init_app
from superdesk import get_resource_service
from superdesk.errors import PublishHTTPPushServerError
import requests


class AgendaTransmit(TestCase):
    def setUp(self):
        planning_init_app(self.app)
        self.setupRemoteSyncMock(self)

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.user_search, self.get_key, self.user_edit, self.save_entry])
        context.mock.__enter__()

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/user/search')
    def user_search(self, url, request):
        resp = [{'IDUser': 1, 'ApiKey': None}]
        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/account/generatekey')
    def get_key(self, url, request):
        resp = {'key': 'YourNewKey'}
        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/user/edit')
    def user_edit(self, url, request):
        return {'status_code': 200}

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/entry/saveentry')
    def save_entry(self, url, request):
        self.assertEqual(request.headers.get('x-agenda-api-key'), 'YourNewKey')
        return {'status_code': 200,
                'headers': {'Location': 'x/9999'}}

    def test_send_event(self):
        user = [{'_id': 1, 'email': 'mock@mail.com.au', 'byline': 'A Mock Up', 'sign_off': 'TA'}]
        self.app.data.insert('users', user)
        planning = [{'_id': '1234', 'type': 'planning'}]
        self.app.data.insert('planning', planning)
        destination = {
            "name": "Agenda 2",
            "format": "agenda_planning",
            "config": {
                "secret_token": "123456",
                "assets_url": "http://bogus.aap.com.au/api"
            },
            "delivery_type": "http_agenda_push"
        }
        item = "{\"Categories\": [{\"ID\": 4, \"IsSelected\": true}], \"Type\": \"planning\", \"TimeFromZone\": " \
               "\"+11:00\", \"Coverages\": [{\"CoverageStatus\": {\"ID\": 1}, \"Role\": {\"ID\": 1}}], \"TimeFrom\": " \
               "\"10:40\", \"PublishingUser\": 1, \"TimeTo\": \"10:40\"," \
               " \"ExternalIdentifier\": \"1234\", \"Visibility\": {\"ID\": 1}, \"TimeToZone\": \"+11:00\", " \
               "\"Agencies\": [{\"ID\": 1, \"IsSelected\": true}], \"SpecialInstructions\": null, \"City\": " \
               "{\"ID\": 106}, \"Title\": \"OBAMA\", \"Region\": {\"ID\": 10}, \"DescriptionFormat\": \"html\", " \
               "\"Description\": \"<p>Obama to give a talk at the New Zealand-United States Council in " \
               "Auckland on March 22. </p>\", \"DateFrom\": \"2018-03-22\", \"EntrySchedule\": {\"ID\": null}, " \
               "\"Country\": {\"ID\": 16}, \"WorkflowState\": {\"ID\": 2}, \"IsNew\": true}"
        transmitter = HTTPAgendaPush()
        transmitter._push_item(destination, item)
        planning = get_resource_service('planning').find_one(req=None, _id='1234')
        self.assertEqual(planning.get('unique_id'), '9999')


class AgendaFailUserSearchTransmit(TestCase):
    def setUp(self):
        planning_init_app(self.app)
        self.setupRemoteSyncMock(self)

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.user_search, self.save_entry])
        context.mock.__enter__()

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/user/search')
    def user_search(self, url, request):
        raise requests.exceptions.HTTPError

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/entry/saveentry')
    def save_entry(self, url, request):
        self.assertEqual(request.headers.get('x-agenda-api-key'), '123456')
        return {'status_code': 200,
                'headers': {'Location': 'x/9999'}}

    def test_send_event(self):
        user = [{'_id': 1, 'email': 'mock@mail.com.au', 'byline': 'A Mock Up', 'sign_off': 'TA'}]
        self.app.data.insert('users', user)
        planning = [{'_id': '1234', 'type': 'planning'}]
        self.app.data.insert('planning', planning)
        destination = {
            "name": "Agenda 2",
            "format": "agenda_planning",
            "config": {
                "secret_token": "123456",
                "assets_url": "http://bogus.aap.com.au/api"
            },
            "delivery_type": "http_agenda_push"
        }
        item = "{\"Categories\": [{\"ID\": 4, \"IsSelected\": true}], \"Type\": \"planning\", \"TimeFromZone\": " \
               "\"+11:00\", \"Coverages\": [{\"CoverageStatus\": {\"ID\": 1}, \"Role\": {\"ID\": 1}}], \"TimeFrom\": " \
               "\"10:40\", \"PublishingUser\": 1, \"TimeTo\": \"10:40\"," \
               " \"ExternalIdentifier\": \"1234\", \"Visibility\": {\"ID\": 1}, \"TimeToZone\": \"+11:00\", " \
               "\"Agencies\": [{\"ID\": 1, \"IsSelected\": true}], \"SpecialInstructions\": null, \"City\": " \
               "{\"ID\": 106}, \"Title\": \"OBAMA\", \"Region\": {\"ID\": 10}, \"DescriptionFormat\": \"html\", " \
               "\"Description\": \"<p>Obama to give a talk at the New Zealand-United States Council in " \
               "Auckland on March 22. </p>\", \"DateFrom\": \"2018-03-22\", \"EntrySchedule\": {\"ID\": null}, " \
               "\"Country\": {\"ID\": 16}, \"WorkflowState\": {\"ID\": 2}, \"IsNew\": true}"
        transmitter = HTTPAgendaPush()
        transmitter._push_item(destination, item)
        planning = get_resource_service('planning').find_one(req=None, _id='1234')
        self.assertEqual(planning.get('unique_id'), '9999')


class AgendaFaileToGetKeyTransmit(TestCase):
    def setUp(self):
        planning_init_app(self.app)
        self.setupRemoteSyncMock(self)

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.user_search, self.get_key, self.save_entry])
        context.mock.__enter__()

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/user/search')
    def user_search(self, url, request):
        resp = [{'IDUser': 1, 'ApiKey': None}]
        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/account/generatekey')
    def get_key(self, url, request):
        raise Exception

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/entry/saveentry')
    def save_entry(self, url, request):
        self.assertEqual(request.headers.get('x-agenda-api-key'), '123456')
        return {'status_code': 200,
                'headers': {'Location': 'x/9999'}}

    def test_send_event(self):
        user = [{'_id': 1, 'email': 'mock@mail.com.au', 'byline': 'A Mock Up', 'sign_off': 'TA'}]
        self.app.data.insert('users', user)
        planning = [{'_id': '1234', 'type': 'planning'}]
        self.app.data.insert('planning', planning)
        destination = {
            "name": "Agenda 2",
            "format": "agenda_planning",
            "config": {
                "secret_token": "123456",
                "assets_url": "http://bogus.aap.com.au/api"
            },
            "delivery_type": "http_agenda_push"
        }
        item = "{\"Categories\": [{\"ID\": 4, \"IsSelected\": true}], \"Type\": \"planning\", \"TimeFromZone\": " \
               "\"+11:00\", \"Coverages\": [{\"CoverageStatus\": {\"ID\": 1}, \"Role\": {\"ID\": 1}}], \"TimeFrom\": " \
               "\"10:40\", \"PublishingUser\": 1, \"TimeTo\": \"10:40\"," \
               " \"ExternalIdentifier\": \"1234\", \"Visibility\": {\"ID\": 1}, \"TimeToZone\": \"+11:00\", " \
               "\"Agencies\": [{\"ID\": 1, \"IsSelected\": true}], \"SpecialInstructions\": null, \"City\": " \
               "{\"ID\": 106}, \"Title\": \"OBAMA\", \"Region\": {\"ID\": 10}, \"DescriptionFormat\": \"html\", " \
               "\"Description\": \"<p>Obama to give a talk at the New Zealand-United States Council in " \
               "Auckland on March 22. </p>\", \"DateFrom\": \"2018-03-22\", \"EntrySchedule\": {\"ID\": null}, " \
               "\"Country\": {\"ID\": 16}, \"WorkflowState\": {\"ID\": 2}, \"IsNew\": true}"
        transmitter = HTTPAgendaPush()
        transmitter._push_item(destination, item)
        planning = get_resource_service('planning').find_one(req=None, _id='1234')
        self.assertEqual(planning.get('unique_id'), '9999')


class AgendaFailToSaveEntryTransmit(TestCase):
    def setUp(self):
        planning_init_app(self.app)
        self.setupRemoteSyncMock(self)

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.user_search, self.get_key, self.user_edit, self.save_entry])
        context.mock.__enter__()

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/user/search')
    def user_search(self, url, request):
        resp = [{'IDUser': 1, 'ApiKey': None}]
        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/account/generatekey')
    def get_key(self, url, request):
        resp = {'key': 'YourNewKey'}
        resp_bytes = json.dumps(resp).encode('UTF-8')
        return {'status_code': 200,
                'content': resp_bytes
                }

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/user/edit')
    def user_edit(self, url, request):
        return {'status_code': 200}

    @urlmatch(scheme='http', netloc='bogus.aap.com.au', path='/api/entry/saveentry')
    def save_entry(self, url, request):
        return {'status_code': 500}

    def test_send_event(self):
        user = [{'_id': 1, 'email': 'mock@mail.com.au', 'byline': 'A Mock Up', 'sign_off': 'TA'}]
        self.app.data.insert('users', user)
        planning = [{'_id': '1234', 'type': 'planning'}]
        self.app.data.insert('planning', planning)
        destination = {
            "name": "Agenda 2",
            "format": "agenda_planning",
            "config": {
                "secret_token": "123456",
                "assets_url": "http://bogus.aap.com.au/api"
            },
            "delivery_type": "http_agenda_push"
        }
        item = "{\"Categories\": [{\"ID\": 4, \"IsSelected\": true}], \"Type\": \"planning\", \"TimeFromZone\": " \
               "\"+11:00\", \"Coverages\": [{\"CoverageStatus\": {\"ID\": 1}, \"Role\": {\"ID\": 1}}], \"TimeFrom\": " \
               "\"10:40\", \"PublishingUser\": 1, \"TimeTo\": \"10:40\"," \
               " \"ExternalIdentifier\": \"1234\", \"Visibility\": {\"ID\": 1}, \"TimeToZone\": \"+11:00\", " \
               "\"Agencies\": [{\"ID\": 1, \"IsSelected\": true}], \"SpecialInstructions\": null, \"City\": " \
               "{\"ID\": 106}, \"Title\": \"OBAMA\", \"Region\": {\"ID\": 10}, \"DescriptionFormat\": \"html\", " \
               "\"Description\": \"<p>Obama to give a talk at the New Zealand-United States Council in " \
               "Auckland on March 22. </p>\", \"DateFrom\": \"2018-03-22\", \"EntrySchedule\": {\"ID\": null}, " \
               "\"Country\": {\"ID\": 16}, \"WorkflowState\": {\"ID\": 2}, \"IsNew\": true}"
        transmitter = HTTPAgendaPush()
        try:
            with self.assertRaises(PublishHTTPPushServerError):
                transmitter._push_item(destination, item)
        except Exception:
            self.fail('Expected exception type was not raised.')
