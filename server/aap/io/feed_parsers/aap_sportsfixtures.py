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
from superdesk.io.registry import register_feed_parser
from superdesk.io.feed_parsers import XMLFeedParser
from datetime import datetime, timedelta
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, GUID_FIELD, CONTENT_STATE
from superdesk.utc import utcnow, local_to_utc
from eve.utils import config
import superdesk
from geopy.geocoders import Nominatim
import time
from superdesk.io.iptc import subject_codes


class AAPSportsFixturesParser(XMLFeedParser):
    NAME = 'aapFixtures'

    label = 'AAP Sports Fixtures Parser'

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

    # Map sport id to sport name, iptc code and a prefix used for the short description
    sport_map = {'1': {'name': 'Rugby League', 'iptc': '15048000', 'prefix': 'RL:'},
                 '2': {'name': 'Rugby Union', 'iptc': '15049000', 'prefix': 'RU:'},
                 '3': {'name': 'Cricket', 'iptc': '15017000', 'prefix': 'CRIK:'},
                 '4': {'name': 'Soccer', 'iptc': '15054000', 'prefix': 'SOC:'},
                 '8': {'name': 'Golf', 'iptc': '15027000', 'prefix': 'GOLF:'},
                 '10': {'name': 'AFL', 'iptc': '15084000', 'prefix': 'AFL:'},
                 '11': {'name': 'Tennis', 'iptc': '15065000', 'prefix': 'TEN:'},
                 '12': {'name': 'Motor Racing', 'iptc': '15039000', 'prefix': 'MOT:'},
                 '14': {'name': 'Ice Hockey', 'iptc': '15031000', 'prefix': 'NHL:'},
                 '15': {'name': 'Baseball', 'iptc': '15007000', 'prefix': 'BASE:'},
                 '27': {'name': 'Gridiron', 'iptc': '15003000', 'prefix': 'NFL:'},
                 '28': {'name': 'MotorCycle Racing', 'iptc': '15041000', 'prefix': 'MOTORCYCLING:'}}

    def __init__(self):
        self.geolocator = Nominatim(user_agent='Superdesk Planning')
        self.not_found = set()

    def can_parse(self, xml):
        return xml.tag == 'Response'

    def parse(self, fixture, provider=None):
        self._clear_values()
        self.eocstat_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='eventoccurstatus')
        self.fixture = fixture
        items = []
        xml = fixture.get('fixture_xml')
        if xml.attrib.get('Status_Code') == 'OK':
            if xml.find('.//Fixtures') is not None:
                self._parse_fixtures(xml, items)
                logging.info('locations not found {}'.format(self.not_found))
            elif xml.find('.//Fixture_List') is not None:
                self._parse_fixture_list(fixture, items)
            return items
        else:
            logging.warning('Failed to retrieve fixture {}'.format(fixture))
        return []

    def _can_ingest_item(self, item):
        """
        Determine if the item has already been ingested, if it has and it's been updated by a user it returns false.
        :param item:
        :return:
        """
        service = superdesk.get_resource_service('events')
        old = service.find_one(req=None, guid=item['guid'])
        # If the item already exists
        if old is not None:
            # if it has been updated by a user
            if 'version_creator' in old:
                return False
            else:
                return True
        else:
            item['firstcreated'] = utcnow()
            return True

    def _set_default_item(self, sport_id, comp_id, match_id):
        """
        Construct an item with the common values as required
        :param sport_id:
        :param comp_id:
        :param match_id:
        :return:
        """
        item = dict()
        item[ITEM_TYPE] = CONTENT_TYPE.EVENT
        item[GUID_FIELD] = 'urn:aapsportsfixtures:{}:{}:{}'.format(sport_id, comp_id, match_id)
        item['anpa_category'] = [{'qcode': 't'}] if comp_id.startswith('dom') else [{'qcode': 's'}]
        item['subject'] = [{'qcode': self.sport_map.get(sport_id, {}).get('iptc', ''),
                            'name': subject_codes.get(self.sport_map.get(sport_id, {}).get('iptc', ''), '')}]
        item['occur_status'] = [x for x in self.eocstat_map.get('items', []) if
                                x['qcode'] == 'eocstat:eos5' and x.get('is_active', True)][0]
        item['occur_status'].pop('is_active', None)
        item['versioncreated'] = utcnow()
        item['state'] = CONTENT_STATE.INGESTED
        item['pubstatus'] = None
        calendars = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='event_calendars')
        item['calendars'] = [c for c in calendars.get('items', []) if c.get('qcode').lower() == 'sport']

        return item

    def _parse_fixtures(self, xml, items):
        self._parse_sport(xml)
        self._parse_series(xml)
        self._parse_teams(xml)
        self._parse_venues(xml)
        self._parse_rounds(xml, items)

    def _parse_fixture_list(self, fixture, items):
        xml = fixture.get('fixture_xml')
        start_date = xml.find('.//Fixture_List/Competition/Competition_Details').attrib.get('Start_Date', '')
        end_date = xml.find('.//Fixture_List/Competition/Competition_Details').attrib.get('End_Date', '')
        comp_type = xml.find('.//Fixture_List/Competition/Competition_Details').attrib.get('Comp_Type', '')
        # A fixture list that the competition details provide the start and end date
        if start_date != '' and end_date != '':
            start = datetime.strptime('{} 00:00'.format(start_date), '%Y-%m-%d %H:%M')
            end = datetime.strptime('{} 23:59'.format(end_date), '%Y-%m-%d %H:%M')
            if datetime.now() < end:
                item = self._set_default_item(fixture.get('sport_id'), fixture.get('comp_id'), '-1')
                if self._can_ingest_item(item):
                    item['name'] = '{} {}'.format(self.sport_map.get(fixture.get('sport_id', {}), {}).get('prefix', ''),
                                                  fixture.get('comp_name'))
                    item['slugline'] = item['name']
                    item['definition_short'] = xml.find('.//Fixture_List/Competition/Competition_Details').attrib.get(
                        'Gender', '')
                    item['dates'] = {
                        'start': local_to_utc(config.DEFAULT_TIMEZONE, start),
                        'end': local_to_utc(config.DEFAULT_TIMEZONE, end),
                        'tz': config.DEFAULT_TIMEZONE,
                    }
                    items.append(item)
        else:
            # A fixture list that we need to pull out each match to determine the match date etc.
            for match in xml.find('.//Fixture_List/Competition/Competition_Fixtures'):
                start_date = match.find('.//Match_Details').attrib.get('Match_Date', '')
                start_time = match.find('.//Match_Details').attrib.get('Match_Time', '')
                try:
                    when = datetime.strptime('{} {}'.format(start_date, start_time), '%Y-%m-%d %H:%M:%S')
                except Exception as ex:
                    continue
                if datetime.now() < when:
                    match_id = match.find('.//Match_Details').attrib.get('Match_ID', '')
                    # Some match id's are not yet available
                    if match_id[-1] == '-':
                        continue
                    match_no = match.find('.//Match_Details').attrib.get('Match_No', '')
                    teamA_name = match.findall('.//Teams/Team_Details')[0].attrib.get('Team_Name', '')
                    teamB_name = match.findall('.//Teams/Team_Details')[1].attrib.get('Team_Name', '')
                    teamA_short = match.findall('.//Teams/Team_Details')[0].attrib.get('Team_Short', '')
                    teamB_short = match.findall('.//Teams/Team_Details')[1].attrib.get('Team_Short', '')
                    venue_name = match.find('.//Venue').attrib.get('Venue_Name', '')
                    venue_location = match.find('.//Venue').attrib.get('Venue_Location', '')
                    item = self._set_default_item(fixture.get('sport_id'), fixture.get('comp_id'), match_id)
                    if self._can_ingest_item(item):
                        item['slugline'] = '{} {}'.format(
                            self.sport_map.get(fixture.get('sport_id', {}), {}).get('prefix', ''), teamA_short)
                        item['name'] = '{} {} V {}'.format(
                            self.sport_map.get(fixture.get('sport_id', {}), {}).get('prefix', ''), teamA_short,
                            teamB_short)
                        item['definition_short'] = '{} match {} {} V {}'.format(fixture.get('comp_name', ''), match_no,
                                                                                teamA_name, teamB_name)

                        # kludge for cricket
                        if fixture.get('sport_id') == '3':
                            if 'test' in comp_type.lower():
                                delta = timedelta(days=5)
                            elif 'shef' in comp_type.lower():
                                delta = timedelta(days=4)
                            elif 't20' in comp_type.lower():
                                delta = timedelta(hours=4)
                            elif 'odi' in comp_type.lower() or 'odd' in comp_type.lower():
                                delta = timedelta(hours=8)
                            else:
                                delta = timedelta(hours=8)
                        else:
                            delta = timedelta(hours=2)
                        item['dates'] = {
                            'start': local_to_utc(config.DEFAULT_TIMEZONE, when),
                            'end': local_to_utc(config.DEFAULT_TIMEZONE, when) + delta,
                            'tz': config.DEFAULT_TIMEZONE,
                        }
                        # add location
                        self._set_location(item, '{}, {}'.format(venue_name, venue_location))
                        items.append(item)

    def _clear_values(self):
        self.sport = ''
        self.series = ''
        self.category = ''
        self.teams = None
        self.venues = None
        self.round = ''
        self.season = ''
        self.fixture = None

    def _parse_sport(self, xml):
        sport = xml.find('.//Fixtures')
        if sport is not None:
            self.sport = sport.attrib.get('Sport', 'Unknown Sport')

    def _parse_series(self, xml):
        series = xml.find('.//Fixtures/Series')
        if series is not None:
            self.series = series.attrib.get('Name', '')
            if series.attrib.get('ID', 'dom').startswith('dom'):
                self.category = 't'
            else:
                self.category = 's'
            self.season = series.attrib.get('Season', '')

    def _parse_teams(self, xml):
        self.teams = dict()
        for team in xml.findall('.//Fixtures/Teams/Team'):
            self.teams[team.attrib.get('ID')] = {'name': team.attrib.get('Name'), 'short': team.attrib.get('Short')}

    def _parse_venues(self, xml):
        self.venues = dict()
        for venue in xml.findall('.//Fixtures/Venues/Venue'):
            self.venues[venue.attrib.get('ID')] = {'name': venue.attrib.get('Name'),
                                                   'location': venue.attrib.get('Location'),
                                                   'country': venue.attrib.get('Country')}

    def _parse_rounds(self, xml, items):
        for round in xml.findall('.//Fixtures/Rounds/Round'):
            self.round = round.attrib.get('Description')
            self._parse_matches(round, items)

    def _parse_matches(self, xml, items):
        for match in xml.findall('.//Matches/Match'):
            try:
                date = match.attrib.get('Date')
                time = match.attrib.get('Start_Time')
                try:
                    when = datetime.strptime('{} {}'.format(date, time), '%Y-%m-%d %H:%M')
                except Exception as ex:
                    continue
                if datetime.now() < when:
                    teamA = self.teams.get(match.attrib.get('TeamA_ID')).get('name')
                    teamB = self.teams.get(match.attrib.get('TeamB_ID')).get('name')
                    item = self._set_default_item(self.fixture.get('sport_id'), self.fixture.get('comp_id'),
                                                  match.attrib.get('Fixture_ID'))
                    if self._can_ingest_item(item):
                        item['slugline'] = '{} {}'.format(
                            self.sport_map.get(self.fixture.get('sport_id', {}), {}).get('prefix', ''),
                            self.teams.get(match.attrib.get('TeamA_ID')).get('short'))
                        item['name'] = '{} {} V {}'.format(
                            self.sport_map.get(self.fixture.get('sport_id', {}), {}).get('prefix', ''),
                            self.teams.get(match.attrib.get('TeamA_ID')).get('short'),
                            self.teams.get(match.attrib.get('TeamB_ID')).get('short'))
                        item['definition_short'] = '{}/{}/{} {} V {}'.format(self.sport, self.series, self.round, teamA,
                                                                             teamB)
                        item['dates'] = {
                            'start': local_to_utc(config.DEFAULT_TIMEZONE, when),
                            'end': local_to_utc(config.DEFAULT_TIMEZONE, when) + timedelta(hours=2),
                            'tz': config.DEFAULT_TIMEZONE,
                        }
                        # add location
                        self._set_location(item, '{}, {}'.format(
                            self.venues.get(match.attrib.get('Venue_ID')).get('name'),
                            self.venues.get(match.attrib.get('Venue_ID')).get('location')))
                        items.append(item)
            except Exception as ex:
                logging.exception(ex)

    def _set_location_not_found(self, item, location_string):
        item['location'] = [{
            'name': location_string,
            'qcode': '',
            'geo': ''
        }]
        self.not_found.add(location_string)

    def _set_location(self, item, location_string):

        # If the locations is not yet determined
        if location_string.startswith('TBC') or location_string == ', ':
            item['location'] = []
            return

        # lookup the location string as unique name in the location collection, if this is found then we use that
        locations_service = superdesk.get_resource_service('locations')
        location = locations_service.find_one(req=None, unique_name=location_string)
        if location:
            item['location'] = [{
                'name': location.get('name', location_string),
                'qcode': location.get('guid')
            }]
            return

        # if we have not looked before and not found it
        if location_string not in self.not_found:
            # if it is not found then look it up using the web service
            try:
                geo_locations = self.geolocator.geocode(location_string, exactly_one=False, addressdetails=True,
                                                        language='en')
            except Exception as ex:
                logging.exception(ex)
                geo_locations = None

            time.sleep(2)
        else:
            geo_locations = None

        if geo_locations is None:
            self._set_location_not_found(item, location_string)
            return

        # Find any locations that are of type stadium
        stadiums = [s for s in geo_locations if s.raw['type'] == 'stadium']
        if len(stadiums) == 0:
            stadiums = [s for s in geo_locations if s.raw['type'] == 'pitch']
            if len(stadiums) == 0:
                stadiums = [s for s in geo_locations if s.raw['type'] == 'sports_centre']
                if len(stadiums) == 0:
                    self._set_location_not_found(item, location_string)
                    return
        stadium = stadiums[0]

        location = dict()
        location['unique_name'] = location_string
        location['name'] = stadium.raw.get('display_name', location_string)
        location['position'] = {'longitude': stadium.point.longitude, 'latitude': stadium.point.latitude,
                                'altitude': stadium.point.altitude}
        localities = [l for l in self.localityHierarchy if stadium.raw.get('address', {}).get(l)]
        areas = [a for a in self.areaHierarchy if stadium.raw.get('address', {}).get(a)]
        location['address'] = {
            'locality': stadium.raw.get('address', {}).get(localities[0], '') if len(localities) > 0 else '',
            'area': stadium.raw.get('address', {}).get(areas[0], '') if len(areas) > 0 else '',
            'country': stadium.raw.get('address', {}).get('country', ''),
            'postal_code': stadium.raw.get('address', {}).get('postcode', ''),
            'external': {'nominatim': stadium.raw}
        }

        ret = locations_service.post([location])
        location = locations_service.find_one(req=None, _id=ret[0])
        item['location'] = [{
            'name': location.get('name', location_string),
            'qcode': location.get('guid')
        }]


register_feed_parser(AAPSportsFixturesParser.NAME, AAPSportsFixturesParser())
