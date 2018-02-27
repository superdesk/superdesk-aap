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


class AgendaPlanningFormatter(Formatter):
    def __init__(self):
        self.can_preview = False
        self.can_export = False

    # select '''' + lower(Code) + ''': ' + CONVERT(varchar(10), IDCategory) + ',' from tbl_AGN_Category
    category_map = {'courts': 1, 'entertainment': 2, 'finance': 3, 'national': 4, 'sport': 5, 'world': 6,
                    'politics': 9, 'holidays': 10, 'ann': 11}

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

    coverage_type_map = {'text': 1, 'photo': 2, 'video': 3, 'infographics': 5, 'live_video': 3}

    coverage_status_map = {'ncostat:int': 1, 'ncostat:notdec': 2, 'ncostat:notint': 3, 'ncostat:onreq': 2}

    def can_format(self, format_type, article):
        """
        Can format events or planning items that have associated coverages
        :param format_type:
        :param article:
        :return:
        """
        can_format_event = format_type == 'agenda_planning' and article.get('type') == 'event'
        can_format_planning = False
        if article.get('type') == 'planning':
            # The planning item must have a coverage in order to be published to agenda or have been published before
            # the dates are derived from the coverage as the planning item does not have dates
            if not article.get('unique_id') and (not article.get('coverages') or len(article.get('coverages')) == 0):
                can_format_planning = False
            else:
                can_format_planning = True

        return can_format_event or can_format_planning

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
        Set default values for the loaction related fields
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
        # If the item has a unique_id it is assumed to be the Agenda ID and the item has been published to Agenda
        if item.get('unique_id'):
            agenda_event['ID'] = item.get('unique_id')
            agenda_event['IsNew'] = False
        else:
            agenda_event['IsNew'] = True
        agenda_event['ExternalIdentifier'] = item.get('_id')
        agenda_event['Type'] = item.get('type')

        agenda_event['Title'] = item.get('name')
        agenda_event['Description'] = '<p>' + item.get('definition_short', '').replace('\n', '<br>') + '</p>'
        if item.get('definition_long', '') != '':
            agenda_event['Description'] = agenda_event['Description'] + '<p>' + item.get('definition_long', '').replace(
                '\n', '<br>') + '</p>'
        agenda_event['DescriptionFormat'] = 'html'
        agenda_event['SpecialInstructions'] = item.get('internal_note')

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
                    agenda_event['City'] = {'ID': self._get_city_id(location, country_id)}
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
                    agenda_event['City'] = {'ID': self._get_city_id(location)}
                agenda_event['Address'] = {'DisplayString': item.get('location')[0].get('name', '')}

        agenda_category = []
        if item.get('calendars') and len(item.get('calendars')) > 0:
            for c in item['calendars']:
                if self.category_map.get(c.get('qcode').lower()):
                    agenda_category.append({'ID': self.category_map.get(c.get('qcode').lower()), 'IsSelected': True})
            agenda_event['Categories'] = agenda_category if len(agenda_category) > 0 else [
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
                    agenda_role = self.coverage_type_map.get(coverage_type)
                    coverage_status = self.coverage_status_map.get(coverage.get('news_coverage_status').get('qcode'))
                    agenda_coverage = {'Role': {'ID': agenda_role}, 'CoverageStatus': {'ID': coverage_status}}
                    coverages.append(agenda_coverage)
        agenda_event['Coverages'] = coverages
        return agenda_event

    def _format_planning(self, item):
        """
        Format the passed palnning item for Agenda
        :param item:
        :return:
        """
        agenda_event = dict()
        # If the item has a unique_id it is assumed to be the Agenda ID and the item has been published to Agenda
        if item.get('unique_id'):
            agenda_event['ID'] = item.get('unique_id')
            agenda_event['IsNew'] = False
        else:
            agenda_event['IsNew'] = True
        agenda_event['ExternalIdentifier'] = item.get('_id')
        agenda_event['Type'] = item.get('type')

        agenda_event['Title'] = item.get('slugline')
        agenda_event['Description'] = '<p>' + item.get('description_text', '') + '</p>'
        agenda_event['DescriptionFormat'] = 'html'
        agenda_event['SpecialInstructions'] = item.get('internal_note')

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
            agenda_role = self.coverage_type_map.get(coverage_type)
            coverage_status = self.coverage_status_map.get(coverage.get('news_coverage_status').get('qcode'))
            agenda_coverage = {'Role': {'ID': agenda_role}, 'CoverageStatus': {'ID': coverage_status}}
            coverages.append(agenda_coverage)
        if len(coverages) > 0:
            agenda_event['Coverages'] = coverages
        else:
            # If not coverage we fall back the to bogus planning date
            start_date = item.get('_planning_date')
            end_date = item.get('_planning_date')

        self._set_dates(agenda_event, 'Australia/Sydney', start_date, end_date)

        # Hard coded for planning items as there are no values available
        self._set_default_location(agenda_event)

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
        elif item.get('pubstatus') == 'rescheduled':
            agenda_event['WorkflowState'] = {'ID': 6}
        elif item.get('pubstatus') == 'postponed':
            agenda_event['WorkflowState'] = {'ID': 5}
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
        if item.get('type', '') == 'planning':
            # If the planning item is associated with an event then we publish the event
            if item.get('event_item'):
                event = superdesk.get_resource_service('events').find_one(req=None, _id=item.get('event_item'))
                agenda_event = self._format_event(event)
            else:
                agenda_event = self._format_planning(item)
        else:
            agenda_event = self._format_event(item)

        return [(pub_seq_num, json.dumps(agenda_event, default=json_serialize_datetime_objectId))]

    def _get_city_id(self, location, country=16):
        service = superdesk.get_resource_service('agenda_city_map')
        entry = service.find({'country_id': int(country), 'name': location.get('address', {}).get('locality', '')})
        if not entry:
            entry = service.find({'country_id': int(country), 'name': location.get('address', {}).get('area', '')})
        if not entry:
            entry = service.find({'country_id': int(country), 'name': location.get('address', {}).get('name', '')})
        if entry:
            return entry.next().get('agenda_id') if entry.count() > 0 else 106
        return 106

    def _get_iptc_id(self, lookup_code):
        service = superdesk.get_resource_service('agenda_iptc_map')
        entry = service.find({'iptc_code': lookup_code})
        if entry:
            return entry.next().get('agenda_id') if entry else None
        return None

    def _get_country_id(self, country):
        service = superdesk.get_resource_service('agenda_country_map')
        entry = service.find({'name': country})
        if entry:
            return entry.next().get('agenda_id') if entry else None
        return None
