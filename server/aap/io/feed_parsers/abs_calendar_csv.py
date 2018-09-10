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
from superdesk.io.feed_parsers import FileFeedParser
import csv
from datetime import datetime
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, GUID_FIELD, CONTENT_STATE
from superdesk.utc import utcnow, local_to_utc
from eve.utils import config
import superdesk
from copy import deepcopy

logger = logging.getLogger(__name__)


class ABSCalendarCSVParser(FileFeedParser):
    NAME = 'absCalendar'

    label = 'ABS Calendar CSV Parser'

    def can_parse(self, file_path):
        """
        Determines if the parser can likely be able to parse the file.
        :param file_path:
        :return:
        """
        try:
            with open(file_path, 'r', encoding='UTF-8') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    return True
                return False
        except Exception as ex:
            return False

    def _set_default_item(self):
        """
        Construct an item with the common values as required
        :return:
        """
        item = dict()
        item[ITEM_TYPE] = CONTENT_TYPE.EVENT
        item[GUID_FIELD] = ''
        eocstat_map = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='eventoccurstatus')
        item['occur_status'] = [x for x in eocstat_map.get('items', []) if
                                x['qcode'] == 'eocstat:eos5' and x.get('is_active', True)][0]
        item['occur_status'].pop('is_active', None)
        item['versioncreated'] = utcnow()
        item['state'] = CONTENT_STATE.INGESTED
        item['pubstatus'] = None
        calendars = superdesk.get_resource_service('vocabularies').find_one(req=None, _id='event_calendars')
        item['calendars'] = [c for c in calendars.get('items', []) if c.get('qcode').lower() == 'abs statistics']

        return item

    def parse(self, filename, provider=None):
        default_item = self._set_default_item()
        items = []
        with open(filename, 'r', encoding='UTF-8') as f:
            csv_reader = csv.reader(f)
            for row in list(csv_reader)[1:]:
                if not len(row):
                    continue
                item = deepcopy(default_item)
                item[GUID_FIELD] = ('urn:www.abs.gov.au:' + row[0].split(' ')[0] +
                                    row[0].split(',')[-1]).replace('/', '-').replace(' ', '-')
                if row[5] == 'true':
                    start = datetime.strptime('{} 11:30'.format(row[1]), '%d/%m/%Y %H:%M')
                    end = datetime.strptime('{} 11:30'.format(row[1]), '%d/%m/%Y %H:%M')
                    item['dates'] = {
                        'start': local_to_utc(config.DEFAULT_TIMEZONE, start),
                        'end': local_to_utc(config.DEFAULT_TIMEZONE, end),
                        'tz': config.DEFAULT_TIMEZONE,
                    }
                    item['name'] = ' '.join(row[0].split(' ')[1:])
                    item['definition_short'] = row[0]
                    items.append(item)
        return items


register_feed_parser(ABSCalendarCSVParser.NAME, ABSCalendarCSVParser())
