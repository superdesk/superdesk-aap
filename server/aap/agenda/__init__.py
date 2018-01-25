# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


from .city_map import CityMapResource
from .iptc_map import IPTCMapResource
from .country_map import CountryMapResource
from superdesk.services import BaseService
import superdesk
from apps.prepopulate.app_initialize import __entities__

__entities__['agenda_city_map'] = ('agenda_city_map.json', '', True)
__entities__['agenda_iptc_map'] = ('agenda_iptc_map.json', '', True)
__entities__['agenda_country_map'] = ('agenda_country_map.json', '', False)


def init_app(app):
    endpoint_name = 'agenda_city_map'
    service = BaseService(endpoint_name, backend=superdesk.get_backend())
    CityMapResource(endpoint_name, app=app, service=service)

    endpoint_name = 'agenda_iptc_map'
    service = BaseService(endpoint_name, backend=superdesk.get_backend())
    IPTCMapResource(endpoint_name, app=app, service=service)

    endpoint_name = 'agenda_country_map'
    service = BaseService(endpoint_name, backend=superdesk.get_backend())
    CountryMapResource(endpoint_name, app=app, service=service)
