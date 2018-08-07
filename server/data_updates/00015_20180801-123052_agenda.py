# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : superdesk
# Creation: 2018-08-01 12:31

from superdesk.commands.data_updates import DataUpdate
from apps.prepopulate.app_initialize import AppInitializeWithDataCommand


class DataUpdate(DataUpdate):

    resource = 'agenda'

    def forwards(self, mongodb_collection, mongodb_database):
        init = AppInitializeWithDataCommand()
        init.run(entity_name='agenda_city_map')
        init.run(entity_name='agenda_country_map')
        init.run(entity_name='agenda_iptc_map')

    def backwards(self, mongodb_collection, mongodb_database):
        for resource in ['agenda_city_map', 'agenda_country_map', 'agenda_iptc_map']:
            collection = mongodb_database[resource]
            collection.drop()
