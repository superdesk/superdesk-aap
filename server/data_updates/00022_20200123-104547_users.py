# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : superdesk
# Creation: 2020-01-23 10:46

from superdesk.commands.data_updates import DataUpdate
from superdesk import get_resource_service


class DataUpdate(DataUpdate):

    resource = 'users'

    def forwards(self, mongodb_collection, mongodb_database):
        users_service = get_resource_service('users')
        for user in users_service.get(req=None, lookup=None):
            user_id = user['_id']

            mongodb_collection.update({'_id': user_id}, {
                '$set': {'display_name': user.get('first_name', '') + ' ' + user.get('last_name', '')}
            })

    def backwards(self, mongodb_collection, mongodb_database):
        users_service = get_resource_service('users')
        for user in users_service.get(req=None, lookup=None):
            user_id = user['_id']

            mongodb_collection.update({'_id': user_id}, {
                '$set': {'display_name': user.get('last_name', '') + ', ' + user.get('first_name', '')}
            })
