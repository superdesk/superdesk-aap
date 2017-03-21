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

from eve.utils import config
import superdesk
from superdesk import get_resource_service
from apps.packages.takes_package_service import TakesPackageService
from superdesk.metadata.packages import LAST_TAKE, RESIDREF, SEQUENCE, LINKED_IN_PACKAGES
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE
import requests
from requests.auth import HTTPBasicAuth
import json


class RemoteSyncCommand(superdesk.Command):
    """Command that will pull the published content from a remote instance of Superdesk.
    """

    option_list = [
        superdesk.Option('--remote', '-rmt', dest='remote', required=True),
        superdesk.Option('--username', '-usr', dest='username', required=True),
        superdesk.Option('--password', '-pwd', dest='password', required=True)
    ]

    headers = {"Content-type": "application/json;charset=UTF-8", "Accept": "application/json"}

    token = None
    url = None

    def _login_to_remote(self, remote, username, password):
        """
        Log into the API of the remote instance of superdesk and save the token for future requests
        :param remote:
        :param username:
        :param password:
        :return:
        """
        try:
            post_data = {'username': username, 'password': password}
            response = requests.post('{}/{}'.format(remote, 'auth_db'), json=post_data, verify=False,
                                     headers=self.headers)
            if int(response.status_code) // 100 == 2:
                content = json.loads(response.content.decode('UTF-8'))
                self.token = content.get('token')
                return True
            else:
                print('Login to remote superdesk API failed with response status code: {}'.format(response.status_code))
                return False
        except Exception as ex:
            print('Login to remote superdesk API failed with exception: {}'.format(ex))

    def _get_remote_published_items(self):
        """
        Query the remote instance of superdesk for published items and process each of them
        :return:
        """
        try:
            from_count = 0
            while True:
                # The query excludes spiked items and returns only text items that are the last published version
                query = {"query": {"filtered": {"filter": {"and": [{"terms": {"type": ["text"]}}, {"not": {
                    "and": [{"term": {"_type": "published"}}, {"term": {"package_type": "takes"}},
                            {"term": {"last_published_version": False}}]}}]}}},
                         "sort": [{"publish_sequence_no": "asc"}],
                         "size": 100, "from": from_count}
                params = {'repo': 'published', 'source': json.dumps(query)}
                response = requests.get('{}/{}'.format(self.url, 'search'), auth=HTTPBasicAuth(self.token, None),
                                        params=params, verify=False)
                content = json.loads(response.content.decode('UTF-8'))
                if len(content['_items']) == 0:
                    break
                for item in content['_items']:
                    try:
                        self._process_item(item['archive_item'])
                    except Exception as ex:
                        print('Exception processing {}'.format(ex))
                from_count += 100
        except Exception as ex:
            print("Exception getting remote published items: {}", ex)

    def _get_remote_package(self, id):
        """
        Given the id of a package retrieve it from the remote instance of superdesk
        :param id:
        :return:
        """
        response = requests.get('{}/{}/{}'.format(self.url, 'archive', id), auth=HTTPBasicAuth(self.token, None),
                                verify=False)
        return json.loads(response.content.decode('UTF-8'))

    def _inject_item(self, item):
        """
        Inject the passed item into the local database and publish it.
        :param item:
        :return:
        """
        item.pop(LINKED_IN_PACKAGES, None)
        get_resource_service('archive').post([item])
        get_resource_service('archive_publish').patch(id=item[config.ID_FIELD],
                                                      updates={ITEM_STATE: CONTENT_STATE.PUBLISHED,
                                                               'auto_publish': True})

    def _inject_take(self, item, take1):
        """
        Given the item and a the first take, link the item into the package sequence and publish it.
        :param item:
        :param take1:
        :return:
        """
        item.pop(LINKED_IN_PACKAGES, None)
        get_resource_service('archive').post([item])
        take1_item = get_resource_service('archive').find_one(req=None, _id=take1.get(RESIDREF))
        TakesPackageService().link_as_next_take(take1_item, item)
        get_resource_service('archive_publish').patch(id=item[config.ID_FIELD],
                                                      updates={ITEM_STATE: CONTENT_STATE.PUBLISHED,
                                                               'auto_publish': True})

    def _process_item(self, item):
        """
        Process an item that has been retrieved from the remote instance of Superdesk
        :param item:
        :return:
        """
        if '_id' in item:
            print("\n\n\n\nProcessing {} headline:[{}] slugline:[{}] takekey:[{} state:{}]".format(item['_id'],
                                                                                                   item.get('headline',
                                                                                                            ''),
                                                                                                   item.get('slugline',
                                                                                                            ''),
                                                                                                   item.get(
                                                                                                       'anpa_take_key',
                                                                                                       ''),
                                                                                                   item.get('state',
                                                                                                            '')))
            if 'rewritten_by' in item:
                print('Item has been rewritten so ignoring it')
                return

            if item['state'] != 'published':
                print('State:  {}  id: {}'.format(item.get('state', ''), item.get('_id', '')))

            if (item.get('state', '')) == 'killed':
                print("Item has been killed, ignoring it")

            fields_to_remove = ('unique_name', 'unique_id', 'takes', '_etag', '_type', '_current_version', '_updated')
            for field in fields_to_remove:
                item.pop(field, None)
            item['state'] = 'in_progress'
            item['_current_version'] = 1

            service = get_resource_service('archive')

            local_item = service.find_one(req=None, _id=item.get('_id'))
            if local_item is None:
                # Test if the item is linked into any takes package
                if 'linked_in_packages' in item and len(item.get('linked_in_packages', [])) > 0 and \
                        any(p.get('package_type', '') == 'takes' for p in item.get('linked_in_packages', [])):
                    pkg_id = TakesPackageService().get_take_package_id(item)
                    remote_pkg = self._get_remote_package(pkg_id)
                    refs = TakesPackageService().get_package_refs(remote_pkg)
                    take1 = next((ref for ref in refs if ref.get(SEQUENCE) == 1), None)
                    if LAST_TAKE not in remote_pkg or remote_pkg[LAST_TAKE] == item[config.ID_FIELD]:
                        if len(refs) == 1:
                            # simple safe to publish single take
                            print("Single take")
                            self._inject_item(item)
                        elif len(refs) > 1:
                            print("Last take")
                            self._inject_take(item, take1)
                    else:
                        if take1.get(RESIDREF) == item[config.ID_FIELD]:
                            print("Take 1")
                            self._inject_item(item)
                        else:
                            print("Other take")
                            self._inject_take(item, take1)
                else:
                    print("Item is not linked in packages {}".format(item.get('_id', '')))
                    self._inject_item(item)
            else:
                print("Already Imported")
        else:
            print("Rubish item {}".format(item))

    def run(self, remote, username, password):
        self.url = remote
        if self._login_to_remote(remote, username, password):
            self._get_remote_published_items()


superdesk.command('app:remote_sync', RemoteSyncCommand())
