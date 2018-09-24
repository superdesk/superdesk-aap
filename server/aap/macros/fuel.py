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
from flask import render_template_string
from datetime import datetime
from flask import current_app as app
from apps.prepopulate.app_initialize import get_filepath
import json


logger = logging.getLogger(__name__)


# These are the markets (cities) that we expect that data is available for
MARKETS = ["Perth", "Sydney", "Melbourne", "Brisbane", "Adelaide"]


def get_areas():
    """
    Read the GeoJson file that outlines a list of named polygons describing the areas we can extract the prices from
    :return:
    """
    areas = []
    path = get_filepath('fuel_geojson.json')
    try:
        with path.open('r') as f:
            areas = json.load(f)
    except Exception as ex:
        logger.error('Exception loading fuel_geojson.json : {}'.format(ex))
    return areas


def fuel_story(item, **kwargs):
    def _get_today():
        """
        Get the current days thumbprint
        :return:
        """
        return datetime.now().isoformat()[:10]

    # groupin clause for the requests
    group = {
        "$group":
            {
                "_id": "$fuel_type",
                "avg": {"$avg": "$price"},
                "min": {"$min": "$price"},
                "max": {"$max": "$price"}
            }
    }

    area = get_areas()
    fuel_map = dict()

    for market in MARKETS:
        pipeline = [{
            "$match": {
                "market": market,
                "sample_date": _get_today()
            }
        }, group]

        fuel_types = list(app.data.mongo.aggregate('fuel', pipeline, {}))
        for i in fuel_types:
            fuel_map[market.lower() + '_avg_' + i.get('_id').lower().replace('-', '')] = '%.1f' % i.get('avg')
            fuel_map[market.lower() + '_min_' + i.get('_id').lower().replace('-', '')] = '%.1f' % i.get('min')
            fuel_map[market.lower() + '_max_' + i.get('_id').lower().replace('-', '')] = '%.1f' % i.get('max')

    for feature in area.get('features'):
        area_name = feature['properties']['name']
        logger.info('Available area {}'.format(area_name))
        coords = feature.get('geometry').get('coordinates')
        pipeline = [{
            "$match": {
                "sample_date": _get_today(),
                "location": {
                    "$geoWithin": {
                        "$geometry": {
                            "type": "Polygon",
                            "coordinates": coords
                        }
                    }
                }
            }
        }, group]
        fuel_types = list(app.data.mongo.aggregate('fuel', pipeline, {}))
        for i in fuel_types:
            fuel_map[area_name.lower() + '_avg_' + i.get('_id').lower().replace('-', '')] = '%.1f' % i.get('avg')
            fuel_map[area_name.lower() + '_min_' + i.get('_id').lower().replace('-', '')] = '%.1f' % i.get('min')
            fuel_map[area_name.lower() + '_max_' + i.get('_id').lower().replace('-', '')] = '%.1f' % i.get('max')

    item['body_html'] = render_template_string(item.get('body_html', ''), **fuel_map)
    return item


name = 'fuel injection'
label = 'Fuel Injection'
callback = fuel_story
access_type = 'frontend'
action_type = 'direct'
