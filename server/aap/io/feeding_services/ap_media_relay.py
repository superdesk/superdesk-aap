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
from superdesk.io.feeding_services import APMediaFeedingService
from superdesk.io.registry import register_feeding_service
from superdesk.errors import IngestApiError
import json
from superdesk.ftp import ftp_connect
import requests
from io import BytesIO
import superdesk
import ftplib
from aap.publish.formatters.unicodetoascii import to_ascii
from superdesk.utc import utcnow
from datetime import timedelta, datetime


logger = logging.getLogger(__name__)


class APMediaRelayFeedingService(APMediaFeedingService):
    NAME = 'ap media relay api'

    label = 'AP Media Relay API'

    fields = [
        {
            'id': 'api_url', 'type': 'text', 'label': 'AP Media API URL',
            'required': True, 'default_value': 'https://api.ap.org/media/v/content/feed'
        },
        {
            'id': 'products_url', 'type': 'text', 'label': 'AP Media API Products URL',
            'required': True, 'default_value': 'https://api.ap.org/media/v/account/plans'
        },
        {
            'id': 'apikey', 'type': 'text', 'label': 'API Key',
            'placeholder': 'API key for access to the API', 'required': True
        },
        {
            'id': 'productList', 'type': 'text', 'label': 'Product List',
            'placeholder': 'Use coma separated product id''s for multiple products, empty for all ', 'required': False
        },
        {
            'id': 'availableProducts', 'type': 'text', 'label': 'All Available Products',
            'readonly': True
        },
        {
            'id': 'recoverytime', 'type': 'text', 'label': 'Number of hours to recover', 'default_value': '',
            'placeholder': 'Specifying a number of hours will restart the feed from that time'
        },
        {
            'id': 'filenametemplate', 'type': 'text', 'label': 'File name template',
            'placeholder': 'Template to overide the original filename of the file pushed to FTP "AAP-%Y%m%d-%H%M%S"'
        },
        {
            'id': 'next_link', 'type': 'text', 'label': 'Next Link',
            'readonly': True
        },
        {
            'id': 'ftp_server', 'type': 'text', 'label': 'Relay FTP Server Address',
            'required': True, 'default_value': 'ftp.aap.com.au'
        },
        {
            'id': 'ftp_user', 'type': 'text', 'label': 'Relay FTP User Name',
            'default_value': 'ap-sd-test'
        },
        {
            'id': 'ftp_password', 'type': 'text', 'label': 'Relay FTP Server Password',
            'default_value': ''
        },
        {
            'id': 'ftp_path', 'type': 'text', 'label': 'FTP Server file path',
            'default_value': '', 'placeholder': 'Path to push the files to on the FTP server'
        }
    ]

    def config_test(self, provider=None):
        self._get_products(provider)
        original = superdesk.get_resource_service('ingest_providers').find_one(req=None, _id=provider.get('_id'))
        # If there has been a change in the required products or recovery time then reset the next link
        if original and (original.get('config', {}).get('productList', '') != provider.get('config', {}).get(
                'productList', '') or
                original.get('config', {}).get('recoverytime', '') !=
                provider.get('config', {}).get('recoverytime', '')):
            provider['config']['next_link'] = None

    def _update(self, provider, update):
        self.HTTP_URL = provider.get('config', {}).get('api_url', '')
        self.provider = provider

        # Set the apikey parameter we're going to use it on all calls
        params = dict()
        params['apikey'] = provider.get('config', {}).get('apikey')

        # Use the next link if one is available in the config
        if provider.get('config', {}).get('next_link'):
            r = self.get_url(url=provider.get('config', {}).get('next_link'), params=params,
                             verify=False, allow_redirects=True)
            r.raise_for_status()
        else:
            id_list = provider.get('config', {}).get('productList', '').strip()
            recovery_time = provider.get('config', {}).get('recoverytime', '1').strip()
            if recovery_time == '':
                recovery_time = '1'
            start = (utcnow() - timedelta(hours=int(recovery_time))).isoformat()[:19] + 'Z'
            # If there has been a list of products defined then we format them for the request, if not all
            # allowed products will be returned.
            if id_list:
                # we remove spaces and empty values from id_list to do a clean list
                id_list = ' OR '.join([id_.strip() for id_ in id_list.split(',') if id_.strip()])
                params['q'] = 'productid:(' + id_list + ') AND mindate:>{}'.format(start)
            else:
                params['q'] = 'mindate:>{}'.format(start)
            params['page_size'] = '100'

            r = self.get_url(params=params, verify=False, allow_redirects=True)
            r.raise_for_status()
        try:
            response = json.loads(r.text)
        except Exception:
            raise IngestApiError.apiRequestError(Exception('error parsing response'))

        nextLink = response.get('data', {}).get('next_page')
        # Got the same next link as last time so nothing new
        if nextLink == provider.get('config', {}).get('next_link'):
            logger.info('Nothing new from AP Media')
            return []

        if len(response.get('data', {}).get('items', [])) > 0:
            try:
                sequence_number = int(provider.get('config', {}).get('sequence', 0))
                with ftp_connect({'username': provider.get('config', {}).get('ftp_user', ''),
                                  'password': provider.get('config', {}).get('ftp_password', ''),
                                  'host': provider.get('config', {}).get('ftp_server', ''),
                                  'path': provider.get('config', {}).get('ftp_path', '')}) as ftp:
                    for item in response.get('data', {}).get('items', []):
                        try:
                            if item['item']['type'] == 'picture':
                                image_ref = item['item']['renditions']['main']['href']
                                if provider.get('config', {}).get('filenametemplate', '') == '':
                                    filename = to_ascii(item['item']['renditions']['main']['originalfilename'])
                                else:
                                    # The filename is generated by applying the date format string in the template
                                    filename = datetime.now().strftime(
                                        provider.get('config', {}).get('filenametemplate', ''))
                                    # and appending the sequence number
                                    filename += '-' + str(sequence_number).zfill(4) + '.jpg'
                                    sequence_number = (sequence_number + 1) % 10000

                                logger.info(
                                    'file: {} versioncreated: {}'.format(filename, item['item']['versioncreated']))
                                r = requests.get(url=image_ref,
                                                 params={'apikey': provider.get('config', {}).get('apikey')})
                                r.raise_for_status()
                                try:
                                    ftp.storbinary('STOR {}'.format(filename), BytesIO(r.content))
                                except ftplib.all_errors as e:
                                    logger.error(e)

                        # Any exception processing an indivisual item is swallowed
                        except Exception as ex:
                            logger.exception(ex)
            except Exception as ex:
                logger.exception(ex)

        # Save the link for next time
        upd_provider = provider.get('config')
        upd_provider['next_link'] = nextLink
        upd_provider['recoverytime'] = ''
        upd_provider['sequence'] = str(sequence_number)
        update['config'] = upd_provider

        return None


register_feeding_service(APMediaRelayFeedingService)
