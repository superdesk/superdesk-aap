# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import requests
import json
import re
from flask import current_app as app
import time
import logging
from flask import render_template_string
from superdesk import get_resource_service
from superdesk.utils import config

cpi_url = 'CPI/2.50.999901.20.Q'
cpi_token = '__CPI__'

unemployment_url = 'LF/0.14.3.1599.20.M'
unemployment_token = '__UNEMPLOYMENT__'

lending_url = 'HF/3.0.99.20.140_1.M'
lending_token = '__LENDING__'

retail_url = 'RT/0.1.20.20.M'
retail_trade_token = '__RETAIL_TRADE__'

bop_url = 'BOP/1.100.20.Q'
bop_token = '__BOP__'

token_map = {cpi_token: cpi_url, unemployment_token: unemployment_url, lending_token: lending_url,
             retail_trade_token: retail_url}

logger = logging.getLogger(__name__)


def expand_token(token, item, template_map):
    url_prefix = app.config.get('ABS_WEB_SERVICE_URL')
    abs_web_service_token = app.config.get('ABS_WEB_SERVICE_TOKEN')
    url_suffix = '/all?dimensionAtObservation=allDimensions&detail=DataOnly&APIKey='

    # convert the token in the item to one that is jinja compliant
    jinja_token = re.sub('\\.|/|\\+|#', '_', token)
    item['body_html'] = item.get('body_html').replace(token, jinja_token)
    item['headline'] = item.get('headline').replace(token, jinja_token)
    item['abstract'] = item.get('abstract').replace(token, jinja_token)

    # Get the token for the primary value
    temp_token = re.sub('\\.|/|\\+', '_', token)
    value_token = temp_token.split('#')[0] + '__' if '#' in token else temp_token

    # If we have handled the value we don't need to do it again
    if template_map.get(value_token):
        return

    data_identifier = token_map.get(token).split('#')[0] if '#' in token_map.get(token) else token_map.get(token)
    # logger.info('ABS request : {}'.format(url_prefix + data_identifier + url_suffix + abs_web_service_token))
    r = requests.get(url_prefix + data_identifier + url_suffix + abs_web_service_token, verify=False)
    if r.status_code == 200:
        # logger.info('Response Text [{}]'.format(r.text))
        try:
            response = json.loads(r.text)
        except:
            logger.error('Exception parsing json for {}'.format(data_identifier))
            return

        # get the number of dimensions in the dataset
        dimensions = len(response.get('structure').get('dimensions').get('observation'))
        # Assume that the time period is the last dimension get it's name
        last_period_name = response.get('structure').get('dimensions').get('observation')[-1].get('values')[-1].get(
            'name')
        # get the index into the dimensions of the last time period
        last_period_index = len(response.get('structure').get('dimensions').get('observation')[-1].get('values')) - 1
        # construct the dimension key of the last data item
        dimension_key = '0:' * (dimensions - 1) + str(last_period_index)

        raw_value = response['dataSets'][0]['observations'][dimension_key][0]
        if isinstance(raw_value, float):
            value = str(round(raw_value, 2))
        else:
            value = str(response['dataSets'][0]['observations'][dimension_key][0])
        template_map[value_token] = value

        # the token for the period
        template_map[value_token[:-1] + 'PERIOD__'] = last_period_name

        # calculate the change from the preceeding value
        last_period_index -= 1
        if last_period_index >= 0:
            # construct the dimension key of the last data item
            dimension_key = '0:' * (dimensions - 1) + str(last_period_index)

            prev_value = response['dataSets'][0]['observations'][dimension_key][0]
            if prev_value > raw_value:
                adjective = 'fell'
            elif prev_value < raw_value:
                adjective = 'rose'
            else:
                adjective = 'held steady'

            template_map[value_token[:-1] + 'ADJECTIVE__'] = adjective

            if isinstance(prev_value, float):
                value = str(round(prev_value, 2))
            else:
                value = str(response['dataSets'][0]['observations'][dimension_key][0])

            template_map[value_token[:-1] + 'PREV__'] = value

            prev_period_name = response.get('structure').get('dimensions').get('observation')[-1].get('values')[-2].get(
                'name')
            template_map[value_token[:-1] + 'PREVPERIOD__'] = prev_period_name
    else:
        logger.info('ABS API returned {} for {}'.format(r.status_code, data_identifier))
    time.sleep(.120)


def abs_expand(item, **kwargs):
    template_map = {}
    # find the primary tokens, delimitered double underscores
    tokens = re.findall('__(.*?)__', item['body_html'])
    for t in tokens:
        if '__' + t + '__' not in token_map:
            token_map['__' + t + '__'] = t
    for e in token_map:
        if e in item['body_html'] or e in item['headline'] or e in item['abstract']:
            expand_token(e, item, template_map)

    try:
        item['body_html'] = render_template_string(item.get('body_html', ''), **template_map)
        item['abstract'] = render_template_string(item.get('abstract', ''), **template_map)
        item['headline'] = render_template_string(item.get('headline', ''), **template_map)
    except Exception as ex:
        logger.warning(ex)

    # If the macro is being executed by a stage macro then update the item directly
    if 'desk' in kwargs and 'stage' in kwargs:
        update = {'body_html': item.get('body_html', ''),
                  'abstract': item.get('abstract', ''),
                  'headline': item.get('headline', '')}
        get_resource_service('archive').system_update(item[config.ID_FIELD], update, item)

        return get_resource_service('archive').find_one(req=None, _id=item[config.ID_FIELD])

    return item


name = 'Expand ABS indicator tokens into the story'
label = 'ABS indicator expand'
callback = abs_expand
access_type = 'frontend'
action_type = 'direct'
