# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# see https://gspread.readthedocs.io/en/latest/oauth2.html and https://github.com/burnash/gspread/blob/master/README.md
# for generating a credentials file

import superdesk
from apps.prepopulate.app_initialize import get_filepath
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime
from datetime import timedelta
from geopy.geocoders import Nominatim
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, GUID_FIELD, CONTENT_STATE
from superdesk.io.iptc import subject_codes
from superdesk.utc import utcnow, local_to_utc
import hashlib
from eve.utils import config
from flask import current_app as app
from eve.utils import ParsedRequest

logger = logging.getLogger(__name__)


class ImportSportCalendarDoc(superdesk.Command):
    option_list = [
        superdesk.Option('--id', '-id', dest='id', required=True),
    ]

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    epoch = datetime.strptime('1899-12-30', '%Y-%m-%d')

    localityHierarchy = [
        'city',
        'state',
        'state_district',
        'region',
        'county',
        'island',
        'town',
        'moor',
        'waterways',
        'village',
        'district',
        'borough',
    ]

    areaHierarchy = [
        'island',
        'town',
        'moor',
        'waterways',
        'village',
        'hamlet',
        'municipality',
        'district',
        'borough',
        'airport',
        'national_park',
        'suburb',
        'croft',
        'subdivision',
        'farm',
        'locality',
        'islet',
    ]

    sheet_map = {'Swimming': '15062000',
                 'Women''s Cricket Internationals': '15017000',
                 'Soccer Internationals': '15054000',
                 'Surfing': '15061000',
                 'Men''s cricket Internationals': '15017000',
                 'MotoGP': '15041000',
                 'Cycling': '15019000',
                 'LPGA Tour': '15027000',
                 'ALPGA Tour': '15027000',
                 'Australian PGA': '15027000',
                 'Formula 1': '15039000',
                 'Super W': '15049000',
                 'Rugby 7s': '15049001',
                 'Athletics': '15005000',
                 'A-League': '15054000',
                 'PGA Tour': '15027000',
                 'Golf European Tour': '15027000',
                 'NRL': '15048000',
                 'AFL': '15084000',
                 'AFLW': '15084000',
                 'Super Rugby': '15049000',
                 'NBL': '15008000',
                 'ATP': '15065000',
                 'WTA': '15065000',
                 'Hockey': '15024000',
                 'Sheffield Shield': '15017000',
                 'Supercars': '15039000'}

    tz_map = dict()

    def __init__(self):
        self.geolocator = Nominatim(user_agent='Superdesk Planning')
        self.not_found = set()

    def _set_location_not_found(self, item, location_string):
        item['location'] = [{
            'name': location_string,
            'qcode': '',
            'geo': ''
        }]
        # print('Location not found : {}'.format(location_string))
        self.not_found.add(location_string)

    def _set_location(self, item, location_string):

        # lookup the location string as unique name in the location collection, if this is found then we use that
        locations_service = superdesk.get_resource_service('locations')
        req = ParsedRequest()
        req.args = {'q': location_string, 'default_operator': 'AND'}
        location = locations_service.get(req=req, lookup=None)
        if location.count():
            item['location'] = [{
                'name': location[0].get('name', location[0].get('name', '')),
                'address': {
                    'line': location[0].get('address', {}).get('line', []),
                    'area': location[0].get('address', {}).get('area', ''),
                    'locality': location[0].get('address', {}).get('locality', ''),
                    'postal_code': location[0].get('address', {}).get('postal_code', ''),
                    'country': location[0].get('address', {}).get('country', ''),
                },
                'qcode': location[0].get('guid')
            }]
            return
        self._set_location_not_found(item, location_string)
        return

    def _set_default_item(self, title, _id, thumbprint, country):
        """
        Construct an item with the common values as required
        :param sport_id:
        :param comp_id:
        :param match_id:
        :return:
        """
        item = dict()
        item[ITEM_TYPE] = CONTENT_TYPE.EVENT
        item[GUID_FIELD] = 'urn:aapsportssheet:{}:{}'.format(_id, thumbprint)
        item['anpa_category'] = [
            {'qcode': 't', 'subject': '15000000', 'name': 'Domestic Sport'}] if country.lower() in ['australia',
                                                                                                    'aus'] else [
            {'qcode': 's', 'subject': '15000000', 'name': 'Overseas Sport'}]

        for k, v in self.sheet_map.items():
            if k in title:
                item['subject'] = [{'qcode': v,
                                    'name': subject_codes.get(v, ''), 'parent': '15000000'}]
                break
        item['occur_status'] = [x for x in self.eocstat_map.get('items', []) if
                                x['qcode'] == 'eocstat:eos5' and x.get('is_active', True)][0]
        item['occur_status'].pop('is_active', None)
        item['versioncreated'] = utcnow()
        item['state'] = CONTENT_STATE.SCHEDULED
        item['pubstatus'] = 'usable'
        calendars = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='event_calendars')
        item['calendars'] = [c for c in calendars.get('items', [])
                             if c.get('qcode').lower() in ('sport', 'sportgeneral')]

        return item

    def _set_country(self, country):
        sheet_country = country.lower()
        if sheet_country == 'usa':
            sheet_country = 'united states'
        if sheet_country == 'uae':
            sheet_country = 'united arab emirates'
        if sheet_country == 'england' or sheet_country == 'scotland':
            sheet_country = 'united kingdom'
        return sheet_country

    def _process_sheet(self, title, dates, values, _id):
        i = 0
        for date in dates:
            start_date = self.epoch + timedelta(days=date)

            dt = start_date
            end_dt = None
            if values[i][1] and values[i][1].lower() != 'tbc':
                try:
                    hours = values[i][1].split(':')[0]
                    minutes = values[i][1].split(':')[1]
                    dt = dt + timedelta(hours=int(hours), minutes=int(minutes))
                except:
                    pass
            if values[i][2] and values[i][2].lower() != 'tbc':
                try:
                    hours = values[i][2].split(':')[0]
                    minutes = values[i][2].split(':')[1]
                    end_dt = start_date + timedelta(hours=int(hours), minutes=int(minutes))
                except:
                    pass

            v = values[i]
            item = self._set_default_item(title, _id, hashlib.sha1('-'.join(v).encode('utf8')).hexdigest(),
                                          v[7] if v[7] else 'australia')
            self._set_location(item, '{} {} {} {}'.format(v[4], v[5], v[6], v[7]))

            sheet_country = self._set_country(v[7])
            sheet_city = v[5].lower()
            loc = sheet_city + '/' + sheet_country

            tz = self.tz_map.get(loc, config.DEFAULT_TIMEZONE)

            item['name'] = v[3]
            item['definition_short'] = v[3]
            item['source'] = 'AAP Sports Sheet'
            if end_dt:
                item['dates'] = {
                    'start': local_to_utc(tz, dt),
                    'end': local_to_utc(tz, end_dt),
                    'tz': tz,
                }
            else:
                item['dates'] = {
                    'start': local_to_utc(tz, dt),
                    'end': local_to_utc(tz, dt) + timedelta(hours=23, minutes=59, seconds=59),
                    'tz': tz,
                }

            # print('{} {} {} {} {}'.format(title, item['name'], item.get('dates').get('start'),
            # item.get('dates').get('end'), tz))
            # print('{}-{} city:[{}] state:[{}] county[{}] ---> {}'.format(title, item['name'], v[5], v[6], v[7], tz))
            print('{},{},{},{},{},{}'.format(title.replace(',', ' '), item['name'].replace(',', ' '), v[5], v[6], v[7],
                                             tz))
            old = superdesk.get_resource_service('events').find_one(req=None, guid=item['guid'])
            if old:
                superdesk.get_resource_service('events').patch(old.get('_id'), item)
            else:
                superdesk.get_resource_service('events').post([item])

            i += 1

    def get_time_zone(self, cities, v, title):
        sheet_country = self._set_country(v[7])
        sheet_state = v[6].lower()
        sheet_city = v[5].lower()
        loc = sheet_city + '/' + sheet_country
        if loc not in self.tz_map:
            located = [c for c in cities if c['city'].lower() == v[5].lower() and (
                c['state'].lower() == sheet_country or c['country'].lower() == sheet_country)]
            if len(located):
                #  print('{}/{} tz {}'.format(sheet_city, sheet_country, located[0].get('tz')))
                pass
            else:
                located = [c for c in cities if
                           (c['state_code'].lower() == sheet_state or c['state'].lower() == sheet_state)
                           and c['country'].lower() == sheet_country]
                if len(located):
                    # print('{}/{} tz {}'.format(sheet_city, sheet_country, located[0].get('tz')))
                    pass
                else:
                    located = [c for c in cities if c['country'].lower() == sheet_country]
                    if len(located):
                        # print('Hit country', title, v)
                        # print('{}/{} tz {}'.format(sheet_city, sheet_country, located[0].get('tz')))
                        pass
                    else:
                        # print('Missed country', title, v)
                        if sheet_country == 'tahiti':
                            self.tz_map[loc] = 'Pacific/Tahiti'
                            return
                        else:
                            self.tz_map[loc] = 'Australia/Sydney'
                            return
            if len(located):
                self.tz_map[loc] = located[0].get('tz')
                return located[0].get('tz')

    def run(self, id):
        self.eocstat_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='eventoccurstatus')

        # You will need to generate a credentials file
        creds = str(get_filepath('Quickstart-44dd51f59d5a.json'))

        credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, self.scope)

        gc = gspread.authorize(credentials)

        sheet = gc.open("Sport Fixtures for Superdesk Planning Tool")

        # Scan the worksheets skipping the first
        cities = app.locators.find_cities()
        for wks in sheet.worksheets()[1:]:
            # print(wks.title)
            dates = wks.col_values(1, value_render_option='UNFORMATTED_VALUE')
            all_vals = wks.get_all_values()
            for v in all_vals:
                self.get_time_zone(cities, v, wks.title)

            self._process_sheet(wks.title, dates, all_vals, wks.id)
            time.sleep(2)


superdesk.command('app:import_sport_calendar_doc', ImportSportCalendarDoc())
