# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015, 2016, 2017 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
import json
import logging
from datetime import timedelta

import superdesk
from superdesk.utc import utcnow, get_date
from eve.utils import ParsedRequest, config
from superdesk.publish.transmitters.http_push import HTTPPushService
from superdesk.publish.formatters.ninjs_newsroom_formatter import NewsroomNinjsFormatter
from superdesk.utils import json_serialize_datetime_objectId

logger = logging.getLogger(__name__)


class NewsroomExportFormatter(NewsroomNinjsFormatter):
    def __init__(self):
        self.format_type = 'Newsroom Export'
        self.can_export = False
        self.can_preview = False

    def format(self, article, subscriber, codes=None):
        try:
            ninjs = self._transform_to_ninjs(article, subscriber)
            return json.dumps(ninjs, default=json_serialize_datetime_objectId)
        except:
            logger.exception("Failed to format the item {}.".format(article.get(config.ID_FIELD)))


class NewsroomHTTPPush(HTTPPushService):
    def transmit(self, queue_item):
        try:
            self._transmit(queue_item, None)
            logger.info('Successfully transmitted item {}'.format(queue_item.get('item_id')))
        except:
            logger.exception("Failed to transmit the item {}.".format(queue_item.get('item_id')))


class ExportToNewsroom(superdesk.Command):
    option_list = [
        superdesk.Option('--url', '-b', dest='url', required=True),
        superdesk.Option('--start_date', '-s', dest='start_date', required=False),
        superdesk.Option('--end_date', '-e', dest='end_date', required=False),
        superdesk.Option('--page_size', '-p', dest='page_size', required=False),
    ]

    default_page_size = 500
    default_start_date = utcnow() - timedelta(days=180)
    default_end_date = utcnow()

    def run(self, url, start_date=None, end_date=None, page_size=None):
        try:
            if start_date:
                self.default_start_date = get_date(start_date)
                self.default_end_date = get_date(end_date)

            if page_size:
                self.default_page_size = int(page_size)

            self.export(url)
        except:
            logger.exception('Failed to run the command.')

    def export(self, url):
        try:
            transmitter = NewsroomHTTPPush()
            for items in self._get_archived_data():
                for item in items:
                    queue_item = self._format_item(item, url)
                    transmitter.transmit(queue_item)
        except:
            logger.exception('Failed to export data.')

    def _get_archived_data(self):
        req = self._get_request(self.default_start_date, self.default_end_date)
        service = superdesk.get_resource_service('search')
        cursor = service.get(req=req, lookup=None)
        count = cursor.count()
        no_of_pages = 0
        version_created = None
        if count:
            no_of_pages = len(range(0, count, self.default_page_size))
            version_created = cursor[0]['versioncreated']

        for page in range(0, no_of_pages):
            logger.info('Fetching archived and published items'
                        'for page number: {}. queue_id: {}'. format((page + 1), version_created))
            req = self._get_request(version_created, self.default_end_date if no_of_pages - 1 == page else None)
            service = superdesk.get_resource_service('search')
            cursor = service.get(req=req, lookup=None)
            items = list(cursor)
            if len(items) > 0:
                version_created = items[len(items) - 1]['versioncreated']
            logger.info('Fetched No. of Items: {} for page: {} '
                        'For export to newsroom.'.format(len(items), (page + 1)))
            yield items

    def _format_item(self, item, url):
        queue_item = {
            'formatted_item': NewsroomExportFormatter().format(item, None),
            'item_id': item.get('item_id'),
            'item_version': item.get(config.version),
            'destination': {
                'name': 'Newsroom Export',
                'format': 'ninjs',
                'config': {
                    'resource_url': '{}/push'.format(url),
                    'assets_url': '{}/push_binary'.format(url)
                },
                'delivery_type': 'http_push'
            },
        }
        return queue_item

    def _get_request(self, start_date, end_date=None):
        date_range = {
            'gte': start_date.strftime('%Y-%m-%dT00:00:00%z')
        }

        if end_date:
            date_range['lt'] = end_date.strftime('%Y-%m-%dT00:00:00%z')

        query = {
            'query': {
                'filtered': {
                    'query': {
                        'bool': {
                            'must': [
                                {'range': {'expiry': {'lt': self.default_end_date.strftime('%Y-%m-%dT00:00:00%z')}}},
                                {'range': {'versioncreated': date_range}},
                                {'term': {'type': 'text'}}
                            ],
                            'must_not': [
                                {
                                    'terms': {
                                        'task.desk': [
                                            '5785c6f7a5398f12510ea67f',
                                            '5779f0fea5398f03377794ed',
                                            '578d6f8ea5398f06614bee1a',
                                            '576b617ca5398f65d22aad91',
                                            '576ccf97a5398f65cfa55f2e',
                                            '576cd04cca6a93509529796d'
                                        ]
                                    }
                                },
                                {
                                    'and': [
                                        {'type': {'value': 'published'}},
                                        {'term': {'task.desk': '5728402eca6a9348ef1189e9'}}
                                    ]
                                }
                            ]
                        }
                    }
                }
            },
            'from': 0,
            'size': self.default_page_size,
            'sort': [{'versioncreated': 'asc'}]
        }

        req = ParsedRequest()
        req.args = {'source': json.dumps(query), 'repo': 'archived,published'}
        return req


superdesk.command('content:export_to_newsroom', ExportToNewsroom())
