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
import traceback

import xml.etree.ElementTree as ET
from superdesk.io.feeding_services.http_service import HTTPFeedingService
from superdesk.io.registry import register_feeding_service
from superdesk.errors import IngestApiError
from superdesk.logging import logger
from superdesk.utc import utcnow


class AAPSportsHTTPFeedingService(HTTPFeedingService):
    label = 'AAP Sports Results Feed'
    NAME = 'aap_sports_http'
    ERRORS = [IngestApiError.apiTimeoutError().get_error_description(),
              IngestApiError.apiRedirectError().get_error_description(),
              IngestApiError.apiRequestError().get_error_description(),
              IngestApiError.apiUnicodeError().get_error_description(),
              IngestApiError.apiParseError().get_error_description(),
              IngestApiError.apiGeneralError().get_error_description()]

    """
    Defines the collection service to be used with this ingest feeding service.
    """
    service = 'events'

    def _update(self, provider, update):
        self.provider = provider
        parser = self.get_feed_parser(provider)

        # get the current year, it is used to filter fixtures for this year and next
        year = int(utcnow().year) % 100
        config = provider.get('config', {})
        content = self._request(config.get('login_url').format(config.get('username'), config.get('password')))
        # get the configured sports
        configured_sports = config.get('sports').split(',')
        xml = ET.fromstring(content)
        if xml.attrib['Status_Code'] == 'OK':
            session = xml.attrib['Status_Session']
            content = self._request(config.get('fixtures_url').format(session, '', '', ''))
            xml = ET.fromstring(content)
            for s in xml.findall('.//Sports/Sport'):
                sport_id = s.attrib['SportID']
                if sport_id not in configured_sports:
                    continue
                sport_name = s.attrib['SportName']
                content = self._request(config.get('fixtures_url').format(session, sport_id, '', ''))
                sport_xml = ET.fromstring(content)
                for c in sport_xml.findall('.//Competition'):
                    comp_id = c.attrib.get('Comp_ID')
                    comp_name = c.attrib.get('Comp_Name')
                    content = self._request(config.get('fixtures_url').format(session, sport_id, comp_id, ''))
                    comp_xml = ET.fromstring(content)
                    for season in comp_xml.findall('.//Season'):
                        season_id = season.attrib.get('SeasonID')
                        if str(year) in season_id or str(year + 1) in season_id:
                            content = self._request(
                                config.get('fixtures_url').format(session, sport_id, comp_id, season_id))
                            fixture_xml = ET.fromstring(content)
                            logger.info('Parsing {}/{} {}/{}'.format(sport_id, sport_name, comp_id, comp_name))
                            items = parser.parse({'fixture_xml': fixture_xml, 'sport_id': sport_id,
                                                  'sport_name': sport_name, 'comp_name': comp_name, 'comp_id': comp_id},
                                                 provider)
                            if len(items) > 0:
                                yield items

    def _request(self, url):
        try:
            response = requests.get(url, params={}, timeout=120)
        except requests.exceptions.Timeout as ex:
            # Maybe set up for a retry, or continue in a retry loop
            raise IngestApiError.apiTimeoutError(ex, self.provider)
        except requests.exceptions.TooManyRedirects as ex:
            # Tell the user their URL was bad and try a different one
            raise IngestApiError.apiRedirectError(ex, self.provider)
        except requests.exceptions.RequestException as ex:
            # catastrophic error. bail.
            raise IngestApiError.apiRequestError(ex, self.provider)
        except Exception as error:
            traceback.print_exc()
            raise IngestApiError.apiGeneralError(error, self.provider)

        if response.status_code == 404:
            raise LookupError('Not found')

        return response.content


register_feeding_service(AAPSportsHTTPFeedingService.NAME, AAPSportsHTTPFeedingService(),
                         AAPSportsHTTPFeedingService.ERRORS)
