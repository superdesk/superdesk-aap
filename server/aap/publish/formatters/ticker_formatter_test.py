# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk.tests import TestCase
from .ticker_formatter import TickerFormatter


class TickerFormatterTest(TestCase):

    def testHTMLFormatted(self):

        article = {'body_html': '<p>I was here</p>'}

        f = TickerFormatter()
        resp = f.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        item = resp['encoded_item']
        self.assertEqual(item, b'\x02\x81\xb0I was here\x03')

    def testPRESERVEDFormatted(self):
        article = {'body_html': '<pre>I was here</pre>'}

        f = TickerFormatter()
        resp = f.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        item = resp['encoded_item']
        self.assertEqual(item, b'\x02\x81\xb0I was here\x03')

    def testWithABreakFormatted(self):
        article = {'body_html': '<pre>I was\nhere</pre>'}

        f = TickerFormatter()
        resp = f.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        item = resp['encoded_item']
        self.assertEqual(item, b'\x02\x81\xb0I was here\x03')

    def testComplexHTMLFormatted(self):
        article = {'body_html': '<div>Kathmandu Holdings has lodged a claim in the New Zealand High'
                                ' Court for the recovery of costs associated with last year\'s takeover bid from '
                                'Briscoe Group.</div><div>Kathmandu Holdings has lodged a claim in the New Zealand '
                                'High Court for the recovery of costs associated with last year\'s takeover bid from '
                                'Briscoe Group.</div><div><br></div><div>Kathmandu incurred costs in relation to the '
                                'takeover bid. After an initial request for payment on November 20, 2015 and subsequent'
                                ' correspondence, Briscoe made a payment of $637,711.65 on May 25, 2016 without '
                                'prejudice to its position on what sum Kathmandu is entitled to recover.</div><div>'
                                '<br></div><div>Kathmandu considers the full amount claimed is recoverable and has '
                                'issued legal proceedings for the balance of monies owed.</div>'}

        f = TickerFormatter()
        resp = f.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        item = resp['encoded_item']
        self.assertEqual(item[:31], b'\x02\x81\xb0Kathmandu Holdings has lodge')

    def testRealisticExample(self):
        article = {'body_html': '<pre>JUDGE RULES ON COLLEEN MCCULLOUGH ESTATE ** &#x27;VALUES&#x27; TEST AN OPTION, '
                                'SAYS TURNBULL ** AUSTRALIA PUSHING FOR PRAKASH EXTRADITION ** PLASTIC TOYS WON&#x27;T '
                                'GO TO LANDFILL: COLES ** TRUMP PLANS TO INVITE PUTIN TO WASHINGTON ** CHELSEA ARRIVE '
                                'IN PERTH FOR GLORY CLASH ** DOUBLE JEOPARDY MURDER CHARGE FOR QLD MAN ** TITANS '
                                'SECURE HIPGRAVE FOR TWO MORE YEARS ** QUEENSLANDERS UNHAPPY WITH ECONOMIC GROWTH ** '
                                'VIC PREMIER CALLED TO FESS UP ABOUT RORTS ** UNEMPLOYMENT RATE STAYS AT 5.4% IN JUNE '
                                '** SANTOS CUTS DEBT, FLAGS DIVIDEND CHANGES ** </pre>'}
        f = TickerFormatter()
        resp = f.format(article, {'_id': 1, 'name': 'Test Subscriber'})[0]
        item = resp['encoded_item']
        self.assertEqual(item, b"\x02\x81\xb0JUDGE RULES ON COLLEEN MCCULLOUGH ESTATE ** 'VALUES' TEST AN OPTION, "
                               b"SAYS TURNBULL ** AUSTRALIA PUSHING FOR PRAKASH EXTRADITION ** PLASTIC TOYS WON'T GO "
                               b"TO LANDFILL: COLES ** TRUMP PLANS TO INVITE PUTIN TO WASHINGTON ** CHELSEA ARRIVE IN "
                               b"PERTH FOR GLORY CLASH ** DOUBLE JEOPARDY MURDER CHARGE FOR QLD MAN ** TITANS SECURE "
                               b"HIPGRAVE FOR TWO MORE YEARS ** QUEENSLANDERS UNHAPPY WITH ECONOMIC GROWTH ** VIC "
                               b"PREMIER CALLED TO FESS UP ABOUT RORTS ** UNEMPLOYMENT RATE STAYS AT 5.4% IN JUNE ** "
                               b"SANTOS CUTS DEBT, FLAGS DIVIDEND CHANGES ** \x03")
