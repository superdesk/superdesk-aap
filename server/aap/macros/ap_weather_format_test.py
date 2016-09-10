# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.tests import TestCase

from .ap_weather_format import ap_weather_format


class APWeatherTestCase(TestCase):
    vocab = [{'_id': 'locators', 'items': [{'qcode': 'US'}]}]

    def setUp(self):
        self.app.data.insert('vocabularies', self.vocab)

    def test_weather_story(self):
        text = '<pre>BC-WEA--Global Weather-Celsius,<\r\n' \
               '\t   NEW YORK (AP) _ Minimum and maximum temperatures in Celsius, precipitation in' \
               ' centimeters and weather conditions as recorded for the previous day and forecast for the' \
               'current and following day in each city as of 1400 GMT:<\r\n' \
               '\t   ;MIN;MAX;COND;PRECIP;MIN;MAX;COND;MIN;MAX;COND<\r\n' \
               '\t   Amsterdam;15;21;rn;3.0;17;25;clr;18;31;clr<\r\n' \
               '\t   Athens;21;34;clr;0.0;24;31;pc;23;31;pc<\r\n' \
               '\t   Atlanta;21;31;clr;0.0;22;32;pc;21;31;pc<\r\n' \
               '\t   Auckland;7;16;rn;0.0;12;14;rn;14;15;rn<\r\n' \
               '\t   Basra;29;48;clr;0.0;28;46;clr;27;48;clr<\r\n' \
               '\t   Bahrain;33;39;clr;0.0;33;38;pc;33;39;clr<\r\n' \
               '\t   Bangkok;25;35;rn;0.0;27;35;rn;27;34;rn<\r\n' \
               '\t   Barbados;26;31;pc;0.0;26;31;pc;26;29;rn<\r\n' \
               '\t   Barcelona;22;29;rn;0.0;19;28;clr;21;29;clr<\r\n' \
               '\t   Beijing;24;34;cdy;0.0;24;33;clr;17;28;pc<\r\n' \
               '\t   Beirut;25;31;clr;0.0;27;30;clr;27;31;clr<\r\n' \
               '\t   Belgrade;16;18;rn;7.0;16;24;cdy;15;27;clr<\r\n' \
               '\t   Berlin;11;23;pc;0.0;14;25;pc;14;27;pc<\r\n' \
               '      x - Indicates missing information.\r\n' \
               '\t      clr - clear\r\n' \
               '\t      pc - partly cloudy\r\n' \
               '\t      cdy - cloudy\r\n' \
               '\t      rn - rain\r\n' \
               '\t      sn - snow\r\n' \
               '\t      Source: Weather Underground<\r\n' \
               'END<\r\n' \
               '\t   </pre>'
        item = {'body_html': text, 'slugline': 'WEA--GlobalWeather-Ce', 'source': 'AP',
                'firstcreated': "2016-08-23T14:32:00.000Z"}
        res = ap_weather_format(item)
        self.assertTrue('   Barbados    26   31   partly cloudy' in res['body_html'])
