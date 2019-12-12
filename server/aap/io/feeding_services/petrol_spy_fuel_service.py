from superdesk.io.feeding_services.http_service import HTTPFeedingService
from superdesk.io.registry import register_feeding_service
from superdesk.errors import IngestApiError
import requests
import json
from datetime import datetime
import time
from superdesk import get_resource_service
import logging

logger = logging.getLogger(__name__)


class PetrolSpyFuelHTTPFeedingService(HTTPFeedingService):
    label = 'Petrol Spy Fuel API Feed'
    NAME = 'petrol_spy_api_feed'

    fields = [
        {
            'id': 'api_url', 'type': 'text', 'label': 'API URL',
            'placeholder': 'API URL', 'required': True
        },
        {
            'id': 'market_definitions', 'type': 'text', 'label': 'Market Definitions',
            'placeholder': '[{\'market\': \'NAME\', \'neLat\': \'NN\', \'neLng\': \'NN\', \'swLat\': NN '
                           ', \'swLng\': NN, \'deltaLat\': NN}]',
            'required': True
        }
    ]
    headers = {"Content-type": "application/json", "Accept": "application/json",
               "User-Agent": "AustralianAssociatedPress"}

    # Map the fuel types to values consistent with the existing ones.
    type_map = {"U91": "ULP",
                "U98": "PULP-98",
                "LPG": "LPG",
                "E10": "E10",
                "U95": "PULP-95",
                "DIESEL": "DSL",
                "PremDSL": "PDSL",
                "E85": "E85",
                "BIODIESEL": "BDSL"}

    def _get_prices(self, provider, market):
        # Longitude remains constant, we make slices with the latitude
        neLng = market.get('neLng')
        swLng = market.get('swLng')

        neLat = market.get('neLat')
        swLat = market.get('swLat')

        # Thickness of the slice
        deltaLat = market.get('deltaLat')

        latE = neLat
        latW = neLat - deltaLat

        servoList = []

        while latE >= swLat:
            path = '?neLat={}&neLng={}&swLat={}&swLng={}'.format(latE, neLng, latW, swLng)

            response = requests.get(provider.get('config', {}).get('api_url') + path, headers=self.headers)
            response.raise_for_status()

            returned = json.loads(response.content.decode('UTF-8'))

            if returned.get('header', {}).get('type') == 'error':
                logger.error('Error response from Petrol Spy {}'.format(
                    returned.get('message', {}).get('error', {}).get('message')))

            latE = latE - deltaLat
            latW = latW - deltaLat

            logger.info('latE: {} LatW: {} Size : {}'.format(latE, latW, returned.get('header', {}).get('size')))
            servoList = servoList + returned.get('message', {}).get('list', [])
            time.sleep(2)

        return servoList

    def _save(self, servos, market):
        service = get_resource_service('fuel')
        # Get the date for the current save
        today = datetime.now().isoformat()[:10]
        fuel_records = []
        for servoEntry in servos:
            #  Extract the servo id, address
            servo_address = {'street': servoEntry.get('address'),
                             'state': servoEntry.get('state'),
                             'country': servoEntry.get('country'),
                             'suburb': servoEntry.get('suburb')}
            servo_location = {'type': 'Point',
                              'coordinates': [servoEntry.get('location').get('x'), servoEntry.get('location').get('y')]}

            # Scan the fuel types available at the servo and extract them
            for fuelType in servoEntry.get("prices", []).keys():
                if not servoEntry.get('prices').get(fuelType).get('relevant'):
                    continue
                # Construct the record
                if self.type_map.get(fuelType):
                    fuel_record = {'sample_date': today, 'market': market.get('market'), 'address': servo_address,
                                   'fuel_type': self.type_map.get(fuelType),
                                   'location': servo_location,
                                   'price': servoEntry.get('prices').get(fuelType).get('amount')}
                    fuel_records.append(fuel_record)

        if len(fuel_records):
            # delete the old dataset for today
            service.delete(lookup={'market': market.get('market'), 'sample_date': today})
            # post the new ones
            service.post(fuel_records)

    def _update(self, provider, update):
        # Each update run will retrieve the data for a single "market"
        market_index = provider.get('private', {}).get('market_index', 0)
        markets = json.loads(provider.get('config', {}).get('market_definitions', []).replace('\'', '"'))
        market = markets[market_index]
        logger.info('Retrieving fuel data for the {} market'.format(market.get('market')))

        try:
            servoList = self._get_prices(provider, market)
            self._save(servoList, market)
        except Exception as ex:
            raise IngestApiError.apiGeneralError(ex, self.provider)
        finally:
            # Save the next market to process
            market_index = (market_index + 1) % len(markets)
            get_resource_service('ingest_providers').system_update(provider.get('_id'),
                                                                   {'private': {'market_index': market_index}},
                                                                   provider)


register_feeding_service(PetrolSpyFuelHTTPFeedingService)
