import superdesk
from geopy.geocoders import Nominatim
# import time
# from aap.io.feed_parsers.aap_sportsfixtures import AAPSportsFixturesParser
from apps.prepopulate.app_initialize import get_filepath


class LocationSeedCommand(superdesk.Command):
    """Seeds the location collection from the data held in a CSV text file
    """

    def __init__(self):
        self.geolocator = Nominatim(user_agent='Superdesk Planning', country_bias='au')

    # def retrieve_likely_locations(self, Name, Street, Suburb, State):
    #   try:
    #       results = self.geolocator.geocode(Name + ' ' + Suburb, exactly_one=True, addressdetails=True, language='en')
    #       time.sleep(2)
    #       if results:
    #           return results
    #       return None
    #   except Exception as ex:
    #       logging.exception(ex)
    #       return None

    def create_location(self, location_string, name, street, suburb, state, postcode, country='Australia'):
        locations_service = superdesk.get_resource_service('locations')
        location = locations_service.find_one(req=None, unique_name=location_string)
        if not location:
            location = dict()
            location['original_source'] = 'Seeded'
            location['unique_name'] = location_string
            location['name'] = name
            location['address'] = {
                'line': [street, state, suburb],
                'country': country if country and country != '' else 'Australia',
                'postal_code': postcode
            }
            locations_service.post([location])
        else:
            location['address'] = {
                'line': [street, state, suburb],
                'country': country if country and country != '' else 'Australia',
                'postal_code': postcode
            }
            locations_service.patch(location.get('_id'), updates=location)

    # def create_from_nomatim(self, nomatim, location_string):
    #     locations_service = superdesk.get_resource_service('locations')
    #     location = locations_service.find_one(req=None, unique_name=location_string)
    #     if not location:
    #         print('Creating from Nominatim')
    #         location = dict()
    #         location['unique_name'] = location_string
    #         location['name'] = nomatim.raw.get('display_name', location_string)
    #         location['position'] = {'longitude': nomatim.point.longitude, 'latitude': nomatim.point.latitude,
    #                                 'altitude': nomatim.point.altitude}
    #       localities = [l for l in AAPSportsFixturesParser.localityHierarchy if nomatim.raw.get('address', {}).get(l)]
    #         areas = [a for a in AAPSportsFixturesParser.areaHierarchy if nomatim.raw.get('address', {}).get(a)]
    #         location['address'] = {
    #             'locality': nomatim.raw.get('address', {}).get(localities[0], '') if len(localities) > 0 else '',
    #             'area': nomatim.raw.get('address', {}).get(areas[0], '') if len(areas) > 0 else '',
    #             'country': nomatim.raw.get('address', {}).get('country', ''),
    #             'postal_code': nomatim.raw.get('address', {}).get('postcode', ''),
    #             'external': {'nominatim': nomatim.raw}
    #         }
    #         ret = locations_service.post([location])
    #     else:
    #         print('Updating from Nominatim')
    #         location['position'] = {'longitude': nomatim.point.longitude, 'latitude': nomatim.point.latitude,
    #                                 'altitude': nomatim.point.altitude}
    #       localities = [l for l in AAPSportsFixturesParser.localityHierarchy if nomatim.raw.get('address', {}).get(l)]
    #         areas = [a for a in AAPSportsFixturesParser.areaHierarchy if nomatim.raw.get('address', {}).get(a)]
    #         location['address'] = {
    #             'locality': nomatim.raw.get('address', {}).get(localities[0], '') if len(localities) > 0 else '',
    #             'area': nomatim.raw.get('address', {}).get(areas[0], '') if len(areas) > 0 else '',
    #             'country': nomatim.raw.get('address', {}).get('country', ''),
    #             'postal_code': nomatim.raw.get('address', {}).get('postcode', ''),
    #             'external': {'nominatim': nomatim.raw}
    #         }
    #         locations_service.patch(location.get('_id'), updates=location)

    def run(self):
        path = get_filepath('locations.csv')
        with path.open('rt') as f:
            lines = f.readlines()
        for line in lines:
            cols = line.split(',')
            name = cols[0].strip()
            street = cols[1].strip()
            suburb = cols[2].strip()
            state = cols[3].strip()
            country = cols[4].strip()
            postcode = cols[5].strip()
            print('Name:{} Street:{}, Suburb":{}, State:{} Country:{} Postcode:{}'.format(name,
                                                                                          street, suburb, state,
                                                                                          country, postcode))
            location_string = '{} {} {} {} {} {}'.format(name, street, suburb, state, postcode, country)
#            ret = self.retrieve_likely_locations(cols[5], cols[7], cols[8], cols[9])
#            if ret:
#                self.create_from_nomatim(ret, location_string)
#            else:
            self.create_location(location_string, name, street, suburb, state, postcode, country)


superdesk.command('app:location_seed', LocationSeedCommand())
