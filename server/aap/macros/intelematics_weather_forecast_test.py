# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from unittest import mock
from superdesk.tests import TestCase
from aap.macros.intelematics_weather_forecast import forecast_story
from apps.publish import init_app

fake_forecast = '<weather-services xmlns="http://www.sunatraffic.com.au" xmlns:xsi="http://www.w3.org/2001/XML' \
                'Schema-instance" xsi:schemaLocation="http://www.sunatraffic.com.au/DTD/weatherForecast.xsd">' \
                '<provider url="http://www.bom.gov.au">Bureau of Meteorology, Australian Government</provider>' \
                '<timestamp>2018-09-26T17:30:38.133+10:00</timestamp>' \
                '<forecast>' \
                '<state name="NSW" issue-time-local="2018-09-26T15:52:56.000+10:00">' \
                '<location>' \
                '<name>Sydney</name>' \
                '<lat>-33.8607</lat>' \
                '<long>151.205</long>' \
                '<chance-of-rain>45%</chance-of-rain>' \
                '<period index="0" start="2018-09-26T17:00:00.000+10:00" end="2018-09-27T00:00:00.000+10:00">' \
                '<icon>16</icon>' \
                '<min-temperature>10.0</min-temperature>' \
                '<max-temperature>17.0</max-temperature>' \
                '<precis>Shower or two. Possible storm.</precis>' \
                '<chance-of-rain>45%</chance-of-rain>' \
                '<amount-of-rain>0-1 mm</amount-of-rain>' \
                '</period>' \
                '<period index="1" start="2018-09-27T00:00:00.000+10:00" end="2018-09-28T00:00:00.000+10:00">' \
                '<icon>3</icon>' \
                '<min-temperature>10.0</min-temperature>' \
                '<max-temperature>21.0</max-temperature>' \
                '<precis>Mostly sunny.</precis>' \
                '<chance-of-rain>45%</chance-of-rain>' \
                '<amount-of-rain>0-1 mm</amount-of-rain>' \
                '</period>' \
                '<period index="2" start="2018-09-28T00:00:00.000+10:00" end="2018-09-29T00:00:00.000+10:00">' \
                '<icon>17</icon>' \
                '<min-temperature>12.0</min-temperature>' \
                '<max-temperature>26.0</max-temperature>' \
                '<precis>Possible shower developing.</precis>' \
                '<chance-of-rain>39%</chance-of-rain>' \
                '<amount-of-rain>0-2 mm</amount-of-rain>' \
                '</period>' \
                '<period index="3" start="2018-09-29T00:00:00.000+10:00" end="2018-09-30T00:00:00.000+10:00">' \
                '<icon>11</icon>' \
                '<min-temperature>13.0</min-temperature>' \
                '<max-temperature>18.0</max-temperature>' \
                '<precis>Shower or two.</precis>' \
                '<chance-of-rain>70%</chance-of-rain>' \
                '<amount-of-rain>3-7 mm</amount-of-rain>' \
                '</period>' \
                '<period index="4" start="2018-09-30T00:00:00.000+10:00" end="2018-10-01T00:00:00.000+10:00">' \
                '<icon>3</icon>' \
                '<min-temperature>10.0</min-temperature>' \
                '<max-temperature>18.0</max-temperature>' \
                '<precis>Partly cloudy.</precis>' \
                '<chance-of-rain>20%</chance-of-rain>' \
                '<amount-of-rain>0-1 mm</amount-of-rain>' \
                '</period>' \
                '<period index="5" start="2018-10-01T00:00:00.000+10:00" end="2018-10-02T00:00:00.000+10:00">' \
                '<icon>3</icon>' \
                '<min-temperature>10.0</min-temperature>' \
                '<max-temperature>19.0</max-temperature>' \
                '<precis>Mostly sunny.</precis>' \
                '<chance-of-rain>21%</chance-of-rain>' \
                '<amount-of-rain>0-1 mm</amount-of-rain>' \
                '</period>' \
                '<period index="6" start="2018-10-02T00:00:00.000+10:00" end="2018-10-03T00:00:00.000+10:00">' \
                '<icon>3</icon>' \
                '<min-temperature>10.0</min-temperature>' \
                '<max-temperature>21.0</max-temperature>' \
                '<precis>Partly cloudy.</precis>' \
                '<chance-of-rain>11%</chance-of-rain>' \
                '<amount-of-rain>0-1 mm</amount-of-rain>' \
                '</period>' \
                '<period index="7" start="2018-10-03T00:00:00.000+10:00" end="2018-10-04T00:00:00.000+10:00">' \
                '<icon>3</icon>' \
                '<min-temperature>11.0</min-temperature>' \
                '<max-temperature>22.0</max-temperature>' \
                '<precis>Partly cloudy.</precis>' \
                '<chance-of-rain>25%</chance-of-rain>' \
                '<amount-of-rain>0-1 mm</amount-of-rain>' \
                '</period>' \
                '</location>' \
                '</state>' \
                '</forecast>' \
                '</weather-services>'

fake_obs = '<weather-services xsi:schemaLocation="http://www.sunatraffic.com.au/DTD/weatherObservationsFeed.xsd" ' \
           'xmlns="http://www.sunatraffic.com.au" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' \
           '<provider url="http://www.bom.gov.au">Bureau of Meteorology, Australian Government</provider>' \
           '<timestamp>2018-09-26T12:15:57.883+10:00</timestamp>' \
           '<observations>' \
           '<state name="NSW">' \
           '<observation>' \
           '<time>2018-09-26T12:00:00.000+10:00</time>' \
           '<loc_name>Albion Park</loc_name>' \
           '<lat>-34.6</lat>' \
           '<long>150.8</long>' \
           '<temperature>11.0</temperature>' \
           '<app_temperature>9.5</app_temperature>' \
           '<humidity>89.0</humidity>' \
           '<wind-speed>7.0</wind-speed>' \
           '<wind-dir>SW</wind-dir>' \
           '<visibility>10.0</visibility>' \
           '</observation>' \
           '</state>' \
           '</observations>' \
           '</weather-services>'


def _fake_get_urls():
    return {'weather forecast': 'http://bogus.com.au/blah', 'current weather': 'http://bogus.com.au/halb'}


def _fake_get_forecast(url):
    if url == 'http://bogus.com.au/blah':
        return fake_forecast
    else:
        return fake_obs
    return None


class weatherTestCase(TestCase):
    def setUp(self):
        init_app(self.app)
        self.app.data.insert('archive', [{'_id': 1}])

    @mock.patch('aap.macros.intelematics_weather_forecast._get_urls', _fake_get_urls)
    @mock.patch('aap.macros.intelematics_weather_forecast._get_forecast', _fake_get_forecast)
    def test_forecast_story(self):
        item = forecast_story({'_id': 1, 'place': [{'qcode': 'NSW'}],
                               'body_html': '{{Sydney_0_amount_of_rain}} {{Albion_Park_obs_humidity}}'})
        self.assertEqual(item.get('body_html'), '0-1 mm 89.0')
