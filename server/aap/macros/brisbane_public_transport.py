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
import requests
from lxml import etree
from io import StringIO
from flask import render_template_string
import re
import datetime as datetime
from superdesk.utc import utcnow
from lxml import html
from superdesk.utils import config
from superdesk import get_resource_service
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE


logger = logging.getLogger(__name__)


def expand_brisbane_transport(item, **kwargs):
    """Makes a request to the translink service update rss feed to extract any relevant notices

    :param item:
    :param kwargs:
    :return:
    """
    bus_story = StringIO()
    train_story = StringIO()
    ferry_story = StringIO()
    tram_story = StringIO()

    incidents_map = dict()

    response = requests.get('https://translink.com.au/service-updates/rss', headers={'Accept': 'application/rss+xml'})
    response.raise_for_status()
    rss = etree.fromstring(response.content)
    for rssitem in rss.findall('./channel/item'):
        title = rssitem.find('title').text
        description = rssitem.find('description').text
        link = rssitem.find('link').text
        catlist = []
        for cat in rssitem.findall('./category'):
            catlist.append(cat.text)

        diff = 100
        # Try to extract the start date and time from the description and calculate the diff to the current time
        # as we only want incidents that have recently started
        regex = r"Effective from: (\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\+(\d{2}):(\d{2})"
        match = re.search(regex, description)
        if match:
            tstr = match.group(0).replace('Effective from: ', '')[:22] + \
                match.group(0).replace('Effective from: ', '')[23:]
            from_date = datetime.datetime.strptime(tstr, '%Y-%m-%dT%H:%M:%S%z')
            now = utcnow()
            diff = abs((from_date - now).days)
            # short_description = description.split('Effective from: ')[0]

        # Only accept current items
        if catlist[0].lower() == 'current' and catlist[1].lower() in ('major', 'minor', 'informative') and diff <= 2:
            # Follow the link to try to get more details
            page = requests.get(link)
            tree = html.fromstring(page.content)
            # Try to find the node that contains the details of the entry
            content = tree.xpath('.//div[@class="templateinsert"]')[0] if len(tree.xpath(
                './/div[@class="templateinsert"]')) else None

            # Try to find the node that
            mode = tree.xpath('.//div[@id="affected-services"]/div/h3')
            if not mode:
                logger.warning('Could not determine the transport mode from {}'.format(link))
                continue
            transport_mode = mode[0].text

            if content is not None:
                stuff = ''.join(content.itertext())
                if transport_mode == 'Bus':
                    bus_story.write('<p>{}</p><p>{}</p><hr>'.format(title, stuff))
                elif transport_mode == 'Train':
                    train_story.write('<p>{}</p><p>{}</p><hr>'.format(title, stuff))
                elif transport_mode == 'Ferry':
                    ferry_story.write('<p>{}</p><p>{}</p><hr>'.format(title, stuff))
                elif transport_mode == 'Tram':
                    tram_story.write('<p>{}</p><p>{}</p><hr>'.format(title, stuff))
            else:
                content = tree.xpath('.//div[@class="bs-callout bs-callout-info"]')[0].getnext() if len(
                    tree.xpath('.//div[@class="bs-callout bs-callout-info"]')) else None
                stuff = ''
                while content is not None:
                    stuff += '<br>' + ' '.join(content.itertext())
                    content = content.getnext()

                if transport_mode == 'Bus':
                    bus_story.write('<p>{}</p><p>{}</p><hr>'.format(title, stuff))
                elif transport_mode == 'Train':
                    train_story.write('<p>{}</p><p>{}</p><hr>'.format(title, stuff))
                elif transport_mode == 'Ferry':
                    ferry_story.write('<p>{}</p><p>{}</p><hr>'.format(title, stuff))
                elif transport_mode == 'Tram':
                    tram_story.write('<p>{}</p><p>{}</p><hr>'.format(title, stuff))
                else:
                    logger.warning('Could not find expected content node in {}'.format(link))
                    if transport_mode == 'Bus':
                        bus_story.write('<p>{}</p>'.format(title))
                    elif transport_mode == 'Train':
                        train_story.write('<p>{}</p>'.format(title))
                    elif transport_mode == 'Ferry':
                        ferry_story.write('<p>{}</p>'.format(title))
                    elif transport_mode == 'Tram':
                        tram_story.write('<p>{}</p>'.format(title))

    incidents_map['bus_alerts'] = bus_story.getvalue()
    incidents_map['train_alerts'] = train_story.getvalue()
    incidents_map['ferry_alerts'] = ferry_story.getvalue()
    incidents_map['tram_alerts'] = tram_story.getvalue()
    bus_story.close()
    train_story.close()
    ferry_story.close()
    train_story.close()

    item['body_html'] = render_template_string(item.get('body_html', ''), **incidents_map)

    # If the macro is being executed by a scheduled template then publish the item as well
    if 'desk' in kwargs and 'stage' in kwargs:
        update = {'body_html': item.get('body_html', '')}
        get_resource_service('archive').system_update(item[config.ID_FIELD], update, item)

        get_resource_service('archive_publish').patch(id=item[config.ID_FIELD],
                                                      updates={ITEM_STATE: CONTENT_STATE.PUBLISHED,
                                                      'auto_publish': True})
        return get_resource_service('archive').find_one(req=None, _id=item[config.ID_FIELD])

    return item


name = 'QLD Public Transport'
label = 'QLD Public Transport'
callback = expand_brisbane_transport
access_type = 'frontend'
action_type = 'direct'
group = 'AM Desk'
