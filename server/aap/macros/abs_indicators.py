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

cpi_url = 'CPI/2.50.999901.20.Q'
cpi_token = '{{CPI}}'

unemployment_url = 'LF/0.14.3.1599.20.M'
unemployment_token = '{{UNEMPLOYMENT}}'

lending_url = 'HF/3.0.99.20.140_1.M'
lending_token = '{{LENDING}}'

retail_url = 'RT/0.1.20.20.M'
retail_trade_token = '{{RETAIL_TRADE}}'

token_map = {cpi_token: cpi_url, unemployment_token: unemployment_url, lending_token: lending_url,
             retail_trade_token: retail_url}

logger = logging.getLogger(__name__)


def expand_token(token, item):
    url_prefix = app.config.get('ABS_WEB_SERVICE_URL')
    abs_web_service_token = app.config.get('ABS_WEB_SERVICE_TOKEN')
    url_suffix = '/all?dimensionAtObservation=allDimensions&detail=DataOnly&APIKey='

    # logger.info('ABS request : {}'.format(url_prefix + token_map.get(token) + url_suffix + abs_web_service_token))
    r = requests.get(url_prefix + token_map.get(token) + url_suffix + abs_web_service_token, verify=False)
    if r.status_code == 200:
        # logger.info('Response Text [{}]'.format(r.text))
        try:
            response = json.loads(r.text)
        except:
            logger.error('Exception parsing json')
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
        item['body_html'] = item.get('body_html').replace(token, value)
        item['headline'] = item.get('headline').replace(token, value)
        item['abstract'] = item.get('abstract').replace(token, value)

        # the token for the period
        token = token.replace('}}', '#PERIOD}}')
        item['body_html'] = item.get('body_html').replace(token, last_period_name)
        item['headline'] = item.get('headline').replace(token, last_period_name)
        item['abstract'] = item.get('abstract').replace(token, last_period_name)

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
            token = token.replace('#PERIOD}}', '#ADJECTIVE}}')
            item['body_html'] = item.get('body_html').replace(token, adjective)
            item['headline'] = item.get('headline').replace(token, adjective)
            item['abstract'] = item.get('abstract').replace(token, adjective)
    else:
        logger.info('ABS API returned {}'.format(r.status_code))
    time.sleep(.120)


def abs_expand(item, **kwargs):
    # find the primary tokens
    tokens = re.findall('{{(.[^#]*?)}}', item['body_html'])
    for t in tokens:
        if '{{' + t + '}}' not in token_map:
            token_map['{{' + t + '}}'] = t
    for e in token_map:
        if e in item['body_html'] or e in item['headline'] or e in item['abstract']:
            expand_token(e, item)
    return item


name = 'Expand ABS indicator tokens into the story'
label = 'ABS indicator expand'
callback = abs_expand
access_type = 'frontend'
action_type = 'interactive'
