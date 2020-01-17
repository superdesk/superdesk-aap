# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk import get_resource_service
import logging
from eve.utils import ParsedRequest
import json
from datetime import datetime
import pytz
from flask import current_app as app
from apps.prepopulate.app_initialize import get_filepath

logger = logging.getLogger(__name__)


def golf_collation(item, **kwargs):
    """
    Collates a number of Golf results into a single story.
    It uses the location of the input item to filter the included stories.
    It expects the name of the golf course (links) to be in the slugline
    Stories will be included based on the order of the slugline
    If grouping result into regions it expect the region name to be in the anpa_take_key of the input item
    :param item:
    :param kwargs:
    :return:
    """

    def get_desk():
        """
        Search for a desk on the system with the name "Copytakers"
        :return:
        """
        logger.info('Fetching the ObjectID for the desk "Copytakers".')
        query = {'name': 'Copytakers'}
        req = ParsedRequest()
        req.where = json.dumps(query)

        desk_service = get_resource_service('desks')
        desk_item = list(desk_service.get_from_mongo(req=req, lookup=None))
        if not desk_item:
            raise('Failed to find the a desk called "Copytakers".')

        desk_id = desk_item[0]['_id']
        logger.info('ObjectID for the desk Copytakers is {}.'.format(desk_id))
        return desk_item[0]

    def get_hold_stages(desk_id):
        """
        Get any stages on the passed desk that have the word Hold in their name
        :param desk_id:
        :return:
        """
        lookup = {'$and': [{'name': {'$regex': 'Hold', '$options': 'i'}}, {'desk': str(desk_id)}]}
        stages = get_resource_service('stages').get(req=None, lookup=lookup)
        return stages

    def get_result_items(location, desk_id, stage_ids, midnight_utc):
        """
        Need to find all stories the need to be collated
        The subject should be golf
        The place should match that of the story the macro is being run against
        The slugline should not start with 'Golf Results' (output story will have this slugline)
        The story should be updated/created since midnight
        Should be on the copy takers desk maybe hold stage?
        Not spiked
        Not already a collated story
        :param location:
        :param desk_id:
        :param stage_ids:
        :param midnight_utc:
        :return:
        """
        query = {
            "query": {
                "filtered": {
                    "filter": {
                        "bool": {
                            "must": [
                                {"term": {"place.qcode": location.get("qcode")}},
                                {"term": {"subject.qcode": "15027000"}},
                                {"term": {"task.desk": str(desk_id)}},
                                {"terms": {"task.stage": stage_ids}},
                                {
                                    "range": {
                                        "versioncreated": {
                                            "gte": midnight_utc
                                        }
                                    }
                                }
                            ],
                            "must_not": [
                                {"term": {"state": "spiked"}},
                                {"query": {
                                    "match_phrase_prefix": {
                                        "slugline": "Golf Results"
                                    }
                                }}
                            ]
                        }
                    }
                }
            },
            "sort": [{"slugline": "asc"}],
            "size": 200
        }

        req = ParsedRequest()
        repos = 'archive'
        req.args = {'source': json.dumps(query), 'repo': repos}
        return get_resource_service('search').get(req=req, lookup=None)

    if 'place' not in item or len(item.get('place')) != 1:
        raise Exception('The story you''re running the macro on must have a single place defined')
    location = item.get('place')[0]

    # Read the file that groups golf courses into regions
    path = get_filepath('golf_links.json')
    try:
        with path.open('r') as f:
            regions = json.load(f)
    except Exception as ex:
        logger.error('Exception loading golf_links.json : {}'.format(ex))

    copytakers_desk = get_desk()

    # Attempt to get the hold stages for the Copytakers desk
    stages = get_hold_stages(copytakers_desk.get('_id'))
    stage_ids = [str(s.get('_id')) for s in stages]
    if len(stage_ids) == 0:
        raise Exception('No hold stages found on desk "{}"'.format(copytakers_desk.get('name')))

    # Get the local midnight in UTC
    midnight_utc = datetime.now(pytz.timezone(app.config['DEFAULT_TIMEZONE']))\
        .replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc).isoformat()[:19] + 'z'

    # List of golf courses to include, if grouping by region
    links = None
    # A flag that indicates if all regions are to be included
    collated_grouped = False

    # Get any any entry from the golf links file for the state defined in the location of the item story
    state_regions = [s for s in regions.get('states') if s.get('state') == location.get('qcode')]
    if len(state_regions):
        state_region = state_regions[0]
        # Match the value in the take key to any region in the links file
        region = [r for r in state_region.get('regions') if
                  item.get('anpa_take_key', '') and r.get('name', '').lower() == item.get('anpa_take_key', '').lower()]
        if len(region):
            links = region[0].get('links', [])
        else:
            # If no match is found then it is assumed that a collated story of all regions is to be produced.
            collated_grouped = True

    items = list(get_result_items(location, copytakers_desk.get('_id'), stage_ids, midnight_utc))
    body = ''
    if collated_grouped:
        # keep a set of the golf links that have been include so as not to include them multiple times
        include_links = set()
        for region in state_region.get('regions'):
            body += '<p>' + region.get('name') + '</p>'
            for i in items:
                for l in region.get('links'):
                    if l.lower().startswith(i.get('slugline', '').lower()) and l not in include_links:
                        body += i.get('body_html')
                        include_links.add(l)
    else:
        for i in items:
            if links:
                for l in links:
                    if l.lower().startswith(i.get('slugline', '').lower()):
                        body += i.get('body_html')
            else:
                body += i.get('body_html')

    if not links:
        dayname = datetime.now(pytz.timezone(app.config['DEFAULT_TIMEZONE'])).strftime('%A')
        item['anpa_take_key'] = location.get('state', '') + ' ' + dayname

    item['body_html'] = body
    item['slugline'] = 'Golf Results'

    return item


name = 'Golf collation'
label = 'Golf collation'
callback = golf_collation
access_type = 'frontend'
action_type = 'direct'
group = 'Copytakers'
