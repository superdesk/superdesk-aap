# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.io.feeding_services.http_service import HTTPFeedingService
from superdesk.io.registry import register_feeding_service
from superdesk.errors import IngestApiError
import requests
import json
from datetime import datetime
from superdesk import get_resource_service
import logging

logger = logging.getLogger(__name__)


class IntelematicsFuelHTTPFeedingService(HTTPFeedingService):
    """
    Retrieve fuel prices from the Intelematics API and store the results for later analysis
    """

    label = 'Intelematics Fuel API Feed'
    NAME = 'intelematics_api_feed'

    fields = [
        {
            'id': 'api_url', 'type': 'text', 'label': 'API URL',
            'placeholder': 'API URL', 'required': True
        },
        {
            'id': 'api_key', 'type': 'text', 'label': 'API Key',
            'placeholder': 'API Key', 'required': True
        },
        {
            'id': 'app_name', 'type': 'text', 'label': 'App Name',
            'placeholder': 'App Name', 'required': True
        },
        {
            'id': 'unique_user_id', 'type': 'text', 'label': 'Unique User Id',
            'placeholder': 'Unique User', 'required': True
        },
        {
            'id': 'market_definitions', 'type': 'text', 'label': 'Market Definitions',
            'placeholder': '[{\'market\': \'NAME\', \'radius\': \'NN\', \'lat\': \'NN\', \'lon\': NN }]',
            'required': True
        }
    ]
    # The limit for the number of servo's returned
    limit = '1000'
    key_header = 'X-IA-API-KEY'
    session_header = 'X-IA-SSO-TOKEN'
    headers = {"Content-type": "application/json", "Accept": "application/json", "Accept-Language": "ENG",
               "Accept-Country": "AUS", "limit": limit}
    session_token = None

    def _get_headers(self, provider):
        headers = self.headers
        if not self.session_token:
            headers[self.key_header] = provider.get('config', {}).get('api_key')
        else:
            headers[self.session_header] = self.session_token
        return headers

    def _get_token(self, provider):
        """
        Gets a Session token from the API and saves it in the ingest provider
        :return:
        """
        path = '/token?appName={}&userUniqueIdentifier={}'.format(provider.get('config', {}).get('app_name'),
                                                                  provider.get('config', {}).get('unique_user_id'))
        response = requests.get(provider.get('config', {}).get('api_url') + path, headers=self._get_headers(provider))

        response.raise_for_status()
        return json.loads(response.content.decode('UTF-8'))

    def _get_prices(self, provider, market):
        time = datetime.now()

        path = '/fuel?radius={}&fueltype=&brand=&lat={}' \
               '&lon={}&' \
               'gpsTime={}T00%3A00%3A00%2B0000&orderBy='.format(market.get('radius'), market.get('lat'),
                                                                market.get('lon'), time.isoformat()[:10])

        response = requests.get(provider.get('config', {}).get('api_url') + path, headers=self._get_headers(provider))
        response.raise_for_status()

        # If more available than our request then log an error, we can't request the next page without breaking the API
        # call frequency limit
        if int(response.headers.get('total')) > int(self.limit):
            logger.error('Request Limit is to small for market {}'.format(market.get('market')))

        return json.loads(response.content.decode('UTF-8'))

    def _update(self, provider, update):
        # Each update run will retrieve the data for a single "market"
        market_index = provider.get('private', {}).get('market_index', 0)
        markets = json.loads(provider.get('config', {}).get('market_definitions', []).replace('\'', '"'))
        market = markets[market_index]
        logger.info('Retrieving fuel data for the {} market'.format(market.get('market')))

        try:
            self.session_token = self._get_token(provider).get('id')
            prices = self._get_prices(provider, market)
            self._save(prices, market)
        except Exception as ex:
            raise IngestApiError.apiGeneralError(ex, self.provider)
        finally:
            # Save the next market to process
            market_index = (market_index + 1) % len(markets)
            get_resource_service('ingest_providers').system_update(provider.get('_id'),
                                                                   {'private': {'market_index': market_index}},
                                                                   provider)

        return None

    def _save(self, prices, market):
        service = get_resource_service('fuel')
        # Get the date for the current save
        today = datetime.now().isoformat()[:10]
        fuel_records = []
        for price in prices:
            #  Extract the servo id, address
            servo = price.get('fuelStation')
            servo_address = servo.get('address')
            servo_location = {'type': 'Point',
                              'coordinates': [servo.get('location').get('lon'), servo.get('location').get('lat')]}

            # Scan the fuel types available at the servo and extract them
            for fuelType in [f for f in servo.get('fuelTypes') if f.get('pricesAvailable')]:
                type_price = next(
                    iter([p for p in price.get('fuelPrice') if p.get('fuelType') == fuelType.get('value')]))
                # Construct the record
                fuel_record = {'sample_date': today, 'market': market.get('market'), 'address': servo_address,
                               'fuel_type': fuelType.get('value'),
                               'location': servo_location, 'price': type_price.get('price')}
                fuel_records.append(fuel_record)

        if len(fuel_records):
            # delete the old dataset for today
            service.delete(lookup={'market': market.get('market'), 'sample_date': today})
            # post the new ones
            service.post(fuel_records)


register_feeding_service(IntelematicsFuelHTTPFeedingService)
