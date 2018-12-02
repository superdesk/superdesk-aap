# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import json
import superdesk
from superdesk.publish.formatters import Formatter
from superdesk.utils import json_serialize_datetime_objectId
from superdesk.utc import utc_to_local
from copy import deepcopy


class AgendaPlanningFormatter(Formatter):
    def __init__(self):
        self.can_preview = False
        self.can_export = False

    # select '''' + lower(Code) + ''': ' + CONVERT(varchar(10), IDCategory) + ',' from tbl_AGN_Category
    category_map = {'courts': 1, 'entertainment': 2, 'finance': 3, 'national': 4, 'sport': 5, 'world': 6,
                    'politics': 9, 'holidays': 10, 'ann': 11,
                    'awards': 2,
                    'birthdays': 2,
                    'company meetings': 3,
                    'community events': 4,
                    'cultural events': 2,
                    'conferences': 4,
                    'elections': 9,
                    'exhibitions': 2,
                    'festivals': 2,
                    'inaugurations & openings': 4,
                    'media opportunities': 4,
                    'observances': 4,
                    'press conferences': 4,
                    'promotional events': 2,
                    'reserve bank fixtures': 3,
                    'special events': 4,
                    'tournaments & competitions': 5,
                    'trade fairs & expos': 3,
                    'weddings': 2,
                    'abs statistics': 3,
                    'funerals and memorial services': 4,
                    'diplomatic and business summits': 9,
                    'speeches and addresses': 4,
                    'royal family events': 2,
                    'sportgeneral': 5,
                    'political events': 9,
                    'inquiries/royal commissons': 4,
                    'rallies, protests or demonstrations': 4,
                    'embargoed stories': 4,
                    'canberra events': 9,
                    'brisbane events': 4,
                    'darwin events': 4,
                    'hobart events': 4,
                    'adelaide events': 4,
                    'perth events': 4,
                    'sydney events': 4,
                    'melbourne events': 4,
                    'interviews/tv program': 3}

    region_map = {'act': 2,
                  'aus': 1,
                  'australia': 1,
                  'australian capital territory': 2,
                  'new south wales': 3,
                  'new zealand': 10,
                  'northern territory': 7,
                  'nsw': 3,
                  'nt': 7,
                  'nz': 10,
                  'oth': 11,
                  'qld': 8,
                  'queensland': 8,
                  'sa': 5,
                  'south australia': 5,
                  'tas': 9,
                  'tasmania': 9,
                  'vic': 4,
                  'victoria': 4,
                  'wa': 6,
                  'western australia': 6,
                  'world': 11}

    # If a place has been specifed this map is used to set the region
    place_region_map = {'ACT': 2, 'AFR': 11, 'ASIA': 11, 'CAN': 11, 'CHN': 11, 'CIS': 11, 'EUR': 11, 'FED': 1,
                        'IRE': 11, 'JPN': 11, 'MID': 11, 'NSW': 3, 'NT': 7, 'NZ': 10, 'PAC': 11, 'QLD': 8,
                        'SA': 5, 'SAM': 11, 'TAS': 9, 'UK': 11, 'US': 11, 'VIC': 4, 'WA': 6}

    # If a place has been specified but no location then the city is set with this map
    place_city_map = {'ACT': 59, 'NSW': 106, 'NT': 62, 'QLD': 50, 'SA': 41, 'TAS': 76, 'VIC': 87, 'WA': 95}

    coverage_type_map = {'text': 1, 'picture': 2, 'video': 3, 'graphic': 5, 'live_video': 3, 'video_explainer': 6,
                         'live_blog': 4, 'audio': 3}

    coverage_status_map = {'ncostat:int': 1, 'ncostat:notdec': 2, 'ncostat:notint': 3, 'ncostat:onreq': 2}

    def can_format(self, format_type, article):
        """
        Can format events or planning items
        :param format_type:
        :param article:
        :return:
        """
        can_format = article.get('type') == 'event' or article.get('type') == 'planning'
        return format_type == 'agenda_planning' and can_format

    def _set_dates(self, agenda_event, tz, start, end):
        """
        Translate the date formats to those used by Agenda
        :param agenda_event:
        :param tz:
        :param start:
        :param end:
        :return:
        """
        datefromlocal = utc_to_local(tz, start)
        datetolocal = utc_to_local(tz, end)

        if datefromlocal is None:
            return

        agenda_event['DateFrom'] = datefromlocal.strftime('%Y-%m-%d')
        # If the to date is different to the from date
        if datefromlocal.strftime('%Y-%m-%d') != datetolocal.strftime('%Y-%m-%d'):
            agenda_event['DateTo'] = datetolocal.strftime('%Y-%m-%d')

        from_time = datefromlocal.strftime('%H:%M')
        to_time = datetolocal.strftime('%H:%M')

        # All day events in Agenda only have a Date
        if not from_time == '00:00' and not to_time == '24:59' and datefromlocal.strftime(
                '%Y-%m-%d') == datetolocal.strftime('%Y-%m-%d'):
            agenda_event['TimeFrom'] = from_time
            agenda_event['TimeTo'] = to_time

        # Need to get the UTC offset
        offset_str = datefromlocal.strftime('%z')
        agenda_event['TimeFromZone'] = offset_str[0:3] + ':' + offset_str[3:5]
        offset_str = datetolocal.strftime('%z')
        agenda_event['TimeToZone'] = offset_str[0:3] + ':' + offset_str[3:5]

    def _set_default_location(self, agenda_event):
        """
        Set default values for the loaction related fields in case we can't derived anything better
        :param agenda_event:
        :return:
        """
        agenda_event['Region'] = {'ID': 3}
        agenda_event['Country'] = {'ID': 16}
        agenda_event['City'] = {'ID': 106}

    def _format_event(self, item):
        """
        Format the passed event item for Agenda
        :param item:
        :return:
        """
        agenda_event = dict()

        agenda_event['Title'] = item.get('name')
        agenda_event['Description'] = '<p>' + item.get('definition_short', '').replace('\n', '<br>') + '</p>'
        if item.get('definition_long', '') != '':
            agenda_event['Description'] = agenda_event['Description'] + '<p>' + item.get('definition_long', '').replace(
                '\n', '<br>') + '</p>'
        agenda_event['DescriptionFormat'] = 'html'
        agenda_event['SpecialInstructions'] = item.get('internal_note') if len(item.get('internal_note', '')) <= 1000\
            else item.get('internal_note')[:1000]

        self._set_dates(agenda_event, item.get('dates').get('tz'), item.get('dates').get('start'),
                        item.get('dates').get('end'))

        self._set_default_location(agenda_event)

        if len(item.get('location', [])) > 0:
            location_service = superdesk.get_resource_service('locations')
            location = location_service.find_one(req=None, guid=item.get('location')[0]['qcode'])
            if location:
                # if the country is not Australia the region is World
                if location.get('address', {}).get('country') and location.get('address', {}).get('country') \
                        != 'Australia':
                    agenda_event['Region'] = {'ID': 11}
                    country_id = self._get_country_id(location.get('address', {}).get('country').lower())
                    agenda_event['Country'] = {'ID': country_id}
                    self._set_city(agenda_event, location, country_id)
                else:
                    # country is Australia
                    agenda_event['Country'] = {'ID': 16}
                    # The state may be in the locality, usualy if the location was seeded.
                    region = self.region_map.get(location.get('address', {}).get('locality', '').lower())
                    if not region:
                        # try to get the state from the nominatim response, if available
                        region = self.region_map.get(
                            location.get('address', {}).get('external', {}).get('nominatim', {}).get('address', {}).get(
                                'state', '').lower())
                    if not region:
                        region = 3
                    agenda_event['Region'] = {'ID': region}
                    self._set_city(agenda_event, location)

                address = [location.get('name', ''),
                           next(iter(location.get('address', {}).get('line', ['']) or []), ''),
                           location.get('address', {}).get('area', ''),
                           location.get('address', {}).get('locality', ''),
                           location.get('address', {}).get('postal_code', ''),
                           location.get('address', {}).get('country', '')]

                agenda_event['Address'] = {'DisplayString': ', '.join(str(x) for x in address if x != '')}

        # if we can derive a region from the place that overrides the default or any derived from the location
        if len(item.get('place', [])) > 0:
            agenda_event['Region'] = {'ID': self.place_region_map.get(item.get('place')[0].get('qcode').upper(), 3)}
            # if there is no location set the city based on the place
            if len(item.get('location', [])) == 0:
                agenda_event['City'] = {'ID': self.place_city_map.get(item.get('place')[0].get('qcode').upper(), 106)}

        agenda_category = []
        if item.get('calendars') and len(item.get('calendars')) > 0:
            for c in item['calendars']:
                if self.category_map.get(c.get('qcode').lower()):
                    agenda_category.append({'ID': self.category_map.get(c.get('qcode').lower()), 'IsSelected': True})
            agenda_event['Categories'] = [dict(t) for t in {tuple(d.items()) for d in agenda_category}] if len(
                agenda_category) > 0 else [
                {'ID': 4, 'IsSelected': True}]
        else:
            agenda_event['Categories'] = [{'ID': 4, 'IsSelected': True}]

        agenda_topics = []
        for s in item.get('subject', []):
            # Agenda map does not have leading 0's
            lookup_code = s.get('qcode') if s.get('qcode')[0] != '0' else s.get('qcode')[1:]
            agenda_iptc_id = self._get_iptc_id(lookup_code)
            if agenda_iptc_id:
                agenda_topics.append({"Topic": {"ID": agenda_iptc_id}})
            else:
                lookup_code = s.get('parent') if s.get('parent')[0] != '0' else s.get('parent')[1:]
                agenda_iptc_id = self._get_iptc_id(lookup_code)
                if agenda_iptc_id:
                    agenda_topics.append({"Topic": {"ID": agenda_iptc_id}})
        agenda_event['Topics'] = agenda_topics

        # Always AAP
        agenda_event['Agencies'] = [{'ID': 1, 'IsSelected': True}]
        agenda_event['Visibility'] = {'ID': 1}
        agenda_event['EntrySchedule'] = {'ID': None}
        self._workflow_state(item, agenda_event)

        # track down any associated planning and coverage
        coverages = []
        plannings = superdesk.get_resource_service('events').get_plannings_for_event(item)
        for planning in plannings:
            # Only include the coverages if the planning item is published
            if planning.get('pubstatus') == 'usable':
                for coverage in planning.get('coverages', []):
                    coverage_type = coverage.get('planning', {}).get('g2_content_type', 'text')
                    agenda_role = self.coverage_type_map.get(coverage_type, 1)
                    coverage_status = self.coverage_status_map.get(coverage.get('news_coverage_status').get('qcode'))
                    agenda_coverage = {'Role': {'ID': agenda_role}, 'CoverageStatus': {'ID': coverage_status}}
                    user_id = coverage.get('assigned_to', {}).get('user')
                    if user_id:
                        agenda_coverage['Resources'] = [{'ID': user_id}]
                    coverages.append(agenda_coverage)
        agenda_event['Coverages'] = coverages

        if len(item.get('event_contact_info', [])):
            contact = superdesk.get_resource_service('contacts').find_one(req=None,
                                                                          _id=item.get('event_contact_info')[0])
            if contact and contact.get('is_active') and contact.get('public'):
                name = '{} {} {}'.format(contact.get('honorific', ''), contact.get('first_name', ''),
                                         contact.get('last_name', ''))
                if contact.get('job_title', '') != '':
                    name += ' {}'.format(contact.get('job_title'))
                if contact.get('organisation', '') != '':
                    name += ' ({})'.format(contact.get('organisation'))
                if len(contact.get('contact_email', [])):
                    for email in contact.get('contact_email'):
                        name += ' {}'.format(email)
                if len(contact.get('contact_phone', [])):
                    for phone in contact.get('contact_phone'):
                        if phone.get('public', True):
                            name += ' Tel: {}'.format(phone.get('number'))
                if len(contact.get('mobile', [])):
                    for phone in contact.get('mobile'):
                        if phone.get('public', True):
                            name += ' Mob: {}'.format(phone.get('number'))

                agenda_event['Contact'] = {'DisplayString': name}
        return agenda_event

    def _format_planning(self, item):
        """
        Format the passed palnning item for Agenda
        :param item:
        :return:
        """
        agenda_event = dict()

        agenda_event['Title'] = item.get('slugline')
        agenda_event['Description'] = '<p>' + item.get('description_text', '') + '</p>'
        agenda_event['DescriptionFormat'] = 'html'
        agenda_event['SpecialInstructions'] = item.get('internal_note') if len(item.get('internal_note', '')) <= 1000\
            else item.get('internal_note')[:1000]

        start_date = None
        end_date = None
        coverages = []
        for coverage in item.get('coverages', []):
            coverage_type = coverage.get('planning', {}).get('g2_content_type', 'text')
            if start_date is None:
                start_date = coverage.get('planning', {}).get('scheduled')
            else:
                if coverage.get('planning', {}).get('scheduled') < start_date:
                    start_date = coverage.get('planning', {}).get('scheduled')
            if end_date is None:
                end_date = coverage.get('planning', {}).get('scheduled')
            else:
                if coverage.get('planning', {}).get('scheduled') > end_date:
                    end_date = coverage.get('planning', {}).get('scheduled')
            agenda_role = self.coverage_type_map.get(coverage_type, 1)
            coverage_status = self.coverage_status_map.get(coverage.get('news_coverage_status').get('qcode'))
            agenda_coverage = {'Role': {'ID': agenda_role}, 'CoverageStatus': {'ID': coverage_status}}
            user_id = coverage.get('assigned_to', {}).get('user')
            if user_id:
                agenda_coverage['Resources'] = [{'ID': user_id}]
            coverages.append(agenda_coverage)
        if len(coverages) > 0:
            agenda_event['Coverages'] = coverages
        else:
            # If not coverage we fall back the to bogus planning date
            start_date = item.get('planning_date')
            end_date = item.get('planning_date')

        self._set_dates(agenda_event, 'Australia/Sydney', start_date, end_date)

        # Hard coded for planning items as there are no values available
        self._set_default_location(agenda_event)

        # if we can derive a region from the place that overrides the default or any derived from the location
        if len(item.get('place', [])) > 0:
            agenda_event['Region'] = {'ID': self.place_region_map.get(item.get('place')[0].get('qcode').upper(), 3)}
            agenda_event['City'] = {'ID': self.place_city_map.get(item.get('place')[0].get('qcode').upper(), 106)}

        # Always AAP
        agenda_event['Agencies'] = [{'ID': 1, 'IsSelected': True}]
        # Visibility controls if the entry is visible externally on Agenda
        # maybe should use the not for publication flag.
        agenda_event['Visibility'] = {'ID': 1}
        agenda_event['EntrySchedule'] = {'ID': None}
        agenda_event['Categories'] = [{'ID': 4, 'IsSelected': True}]
        self._workflow_state(item, agenda_event)

        return agenda_event

    def _workflow_state(self, item, agenda_event):
        """
        Map the status of the event/planning item to the agenda values
        :param agenda_event:
        :return:
        """

        # Allowed values in Agenda are :-
        # 1 ForApproval
        # 2 Published
        # 3 Spiked
        # 4 Draft
        # 5 Postponed
        # 6 Rescheduled
        # 7 Cancelled

        if item.get('pubstatus') == 'cancelled' or item.get('occur_status', {}).get('qcode', '') == 'eocstat:eos6':
            agenda_event['WorkflowState'] = {'ID': 7}
        elif item.get('state') == 'rescheduled':
            agenda_event['WorkflowState'] = {'ID': 6}
        elif item.get('state') == 'postponed':
            agenda_event['WorkflowState'] = {'ID': 5}
        elif item.get('state') == 'spiked':
            agenda_event['WorkflowState'] = {'ID': 3}
        else:
            agenda_event['WorkflowState'] = {'ID': 2}

    def format(self, item, subscriber, codes=None):
        """
        Given an item that is either an event or planning item, format the reasponse for Agenda
        :param item:
        :param subscriber:
        :param codes:
        :return:
        """
        pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)
        format_item = deepcopy(item)
        # If the item has a unique_id it is assumed to be the Agenda ID and the item has been published to Agenda
        agenda_id = format_item.get('unique_id')
        if format_item.get('type', '') == 'planning':
            # If the planning item is associated with an event then we publish the event
            if format_item.get('event_item'):
                service = superdesk.get_resource_service('events')
                format_item = service.find_one(req=None, _id=format_item.get('event_item'))
                agenda_event = self._format_event(format_item)
                # If the planning item has an agenda id but the event item does not we set the id into the event
                if agenda_id and not format_item.get('unique_id'):
                    service.system_update(format_item.get('event_item'), {'unique_id': agenda_id}, format_item)
            else:
                agenda_event = self._format_planning(format_item)
        else:
            # not published to agenda before
            if not agenda_id:
                # Check if the event has a published child planning item, the id of that is promoted to the event
                service = superdesk.get_resource_service('events')
                plannings = service.get_plannings_for_event(format_item)
                for planning in plannings:
                    if planning.get('unique_id'):
                        agenda_id = planning.get('unique_id')
                        break
                if agenda_id:
                    # Set the agenda id, this will get picked up at transmit time and will update the existing agenda
                    # item.
                    service.system_update(format_item.get('_id'), {'unique_id': agenda_id}, format_item)

            agenda_event = self._format_event(format_item)

        agenda_event['Type'] = format_item.get('type')
        agenda_event['ExternalIdentifier'] = format_item.get('_id')

        # Pass the id of the user that is publishing the item, so we can spoof the user in the update to agenda
        agenda_event['PublishingUser'] = format_item.get('version_creator', format_item.get('original_creator'))

        return [(pub_seq_num, json.dumps(agenda_event, default=json_serialize_datetime_objectId))]

    def _get_city_id(self, location, country=16):
        service = superdesk.get_resource_service('agenda_city_map')
        entry = service.find({'country_id': int(country), 'name': location.get('address', {}).get('locality', '')})
        if not entry or entry.count() <= 0:
            entry = service.find({'country_id': int(country), 'name': location.get('address', {}).get('area', '')})
        if not entry or entry.count() <= 0:
            entry = service.find({'country_id': int(country), 'name': location.get('address', {}).get('name', '')})
        if entry:
            return entry.next().get('agenda_id') if entry.count() > 0 else None
        return None

    def _set_city(self, agenda_event, location, country=16):
        """If no city id could be determined from the city map then pass what should be the City as a string

        :param agenda_event:
        :param location:
        :param country:
        :return:
        """
        city_id = self._get_city_id(location, country)
        if city_id is None:
            agenda_event['City'] = {'DisplayString': location.get('address').get('area') or
                                    location.get('address').get('locality')}
        else:
            agenda_event['City'] = {'ID': city_id}

    def _get_iptc_id(self, lookup_code):
        service = superdesk.get_resource_service('agenda_iptc_map')
        entry = service.find({'iptc_code': lookup_code})
        if entry and entry.count() > 0:
            return entry.next().get('agenda_id') if entry else None
        return None

    def _get_country_id(self, country):
        service = superdesk.get_resource_service('agenda_country_map')
        entry = service.find({'name': country})
        if entry and entry.count() > 0:
            return entry.next().get('agenda_id') if entry else None
        return 16
