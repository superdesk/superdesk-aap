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
from lxml import html
import requests
from datetime import datetime, timedelta
from flask import render_template_string
from superdesk import get_resource_service, config
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE

logger = logging.getLogger(__name__)


def _get_quality(value):
    if value is None:
        return ''
    num = int(value)
    if num <= 33:
        return 'Very good'
    if num <= 66:
        return 'Good'
    if num <= 99:
        return 'Fair'
    if num <= 149:
        return 'Poor'
    if num <= 199:
        return 'Very poor'
    return 'Hazardous'


def generate_pollution_story(item, **kwargs):
    """Retrieve the polution page, scrape it for the required values, apply to the item (template) passed and publish

    :param item:
    :param kwargs:
    :return:
    """
    values_map = {}
    # The pollution figures are scraped from the page below.
    # It seems that the second table, the class given to the first data item determines if the row contains
    # the regional value or just the site value, regional value rows seem to also contain a site value AQI
    # The results are stored into the values map
    url = 'https://airquality.environment.nsw.gov.au/aquisnetnswphp/getPage.php?reportid=1'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    rows = tree.xpath('/html/body/table[2]/tbody/tr')
    for row in rows:
        tds = row.xpath('./*')
        if tds[0].attrib.get('class', '') == 'region':
            if tds[-1].attrib.get('class', '').startswith('raqi'):
                location = tds[0].text.lower().replace(' ', '_').replace('-', '_')
                value = tds[-1].text
                values_map[location + '_value'] = value
                values_map[location + '_description'] = _get_quality(value)
            if tds[1].attrib.get('class', '') == 'site':
                location = tds[1].text.lower().replace(' ', '_').replace('-', '_')
                value = tds[-3].text
                values_map[location + '_value'] = value
                values_map[location + '_description'] = _get_quality(value)
        else:
            if tds[0].attrib.get('class', '') == 'site':
                location = tds[0].text.lower().replace(' ', '_').replace('-', '_')
                value = tds[-1].text
                values_map[location + '_value'] = value
                values_map[location + '_description'] = _get_quality(value)

    # Pull the date and time out from the page
    date = tree.xpath('/html/body/table[1]/tbody/tr/td[1]/text()[2]')
    time = tree.xpath('/html/body/table[1]/tbody/tr/td[1]/text()[3]')
    dt = datetime.strptime(date[0] + ' ' + time[0].split(' ')[2] + time[0].split(' ')[3].upper(), '%d %B %Y %I%p')
    values_map['time'] = dt.strftime('%H:%M')
    values_map['date'] = dt.strftime('%d/%m/%y')
    values_map['time_range'] = (dt - timedelta(hours=1)).strftime('%H:%M') + '-' + dt.strftime('%H:%M')

    # Attempt to extract the forecast from the page below
    url = 'https://airquality.environment.nsw.gov.au/aquisnetnswphp/getPage.php?reportid=9'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    # Extract the value
    values_map['sydney_forecast'] = str(tree.xpath('/html/body/center/table/tbody/tr[1]/td/p/b/text()')[0])
    # Get the day that the forecast is for
    forcast_day = str(tree.xpath('/html/body/center/table/tbody/tr[1]/td/p/text()[2]')[0])
    forecast_date = datetime.strptime(forcast_day, '%a %d %B %Y')
    if forecast_date.date() == datetime.now().date():
        values_map['forecast_day'] = 'today'
    elif forecast_date == (datetime.now() + timedelta(days=1)):
        values_map['forecast_day'] = 'tomorrow'

    body_html = render_template_string(item.get('body_html', ''), **values_map)
    headline = render_template_string(item.get('headline', ''), **values_map)
    anpa_take_key = render_template_string(item.get('anpa_take_key', ''), **values_map)
    get_resource_service('archive_publish').patch(id=item[config.ID_FIELD],
                                                  updates={ITEM_STATE: CONTENT_STATE.PUBLISHED,
                                                           'auto_publish': True,
                                                           'body_html': body_html,
                                                           'headline': headline,
                                                           'anpa_take_key': anpa_take_key})
    return get_resource_service('archive').find_one(req=None, _id=item[config.ID_FIELD])


name = 'weather pollution'
label = 'Weather Pollution'
callback = generate_pollution_story
access_type = 'backend'
action_type = 'direct'
