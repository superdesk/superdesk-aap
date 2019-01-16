# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from unittests import AAPTestCase
from .brisbane_public_transport import expand_brisbane_transport
from httmock import urlmatch, HTTMock
from superdesk.utc import utcnow


class SydneyBusesTestCase(AAPTestCase):
    def setUp(self):
        self.setupRemoteSyncMock(self)

    def setupRemoteSyncMock(self, context):
        context.mock = HTTMock(*[self.get_api, self.get_link])
        context.mock.__enter__()

    @urlmatch(scheme='https', netloc='translink.com.au',
              path='/service-updates/rss')
    def get_api(self, p1, p2, p3=None):
        data = '<?xml version="1.0" encoding="UTF-8"?> \
            <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" ' \
               'xmlns:slash="http://purl.org/rss/1.0/modules/slash/"> \
              <channel> \
                <title>TransLink service notices feed</title> \
                <description>Current and upcoming service notices or the TransLink public transport ' \
               'network</description> \
                <pubDate>Wed, 16 Jan 2019 04:59:05 +0000</pubDate> \
                <generator>Zend_Feed_Writer 2 (http://framework.zend.com)</generator> \
                <link>https://translink.com.au/service-updates</link> \
                <atom:link rel="self" type="application/rss+xml" href="https://translink.com.au/service-updates/rss"/> \
                <item> \
                  <title>Cleveland line suspended: Lindum - Cleveland </title> \
                  <description><![CDATA[(Major) Cleveland line suspended: Lindum - Cleveland .  ' \
               'Effective from: 2019-01-16T14:27:00+10:00]]></description> \
                  <link>https://translink.com.au/service-updates/214261</link> \
                  <guid>https://translink.com.au/service-updates/214261</guid> \
                  <category><![CDATA[Current]]></category> \
                  <category><![CDATA[major]]></category> \
                  <slash:comments>0</slash:comments> \
                </item> \
              </channel> \
            </rss>'

        date = utcnow().strftime('%Y-%m-%dT%H:%M:%S+10:00')
        data = data.replace('2019-01-16T14:27:00+10:00', date)
        return {'status_code': 200,
                'content': data.encode('utf-8')}

    @urlmatch(scheme='https', netloc='translink.com.au',
              path='/service-updates/214261')
    def get_link(self, p1, p2, p3=None):
        data = '<html><body><div class="templateinsert"><p>Content</p></div><div id="affected-services">' \
               '<div><h3>Train</div></h3></div></body></html>'
        return {'status_code': 200,
                'content': data.encode('utf-8')}

    def test_brisbane_public_transport(self):
        item = expand_brisbane_transport({'body_html': '{{train_alerts}}'})
        self.assertEqual(item.get('body_html'), '<p>Cleveland line suspended: Lindum - Cleveland </p>'
                                                '<p>Content</p><hr>')
