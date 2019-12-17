# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import unittest
from .strip_paragraphs import strip_paragraphs

body_html = '<p>Dandenong District Cricket Association-Turf 1</p><p>Round 6</p><p>Heinz Southern Districts 7/193 ' \
            'def St Mary''s 192,</p><p>Buckley Ridges 6/230 def Narre South 226,</p><p>Springvale South 2/156 def ' \
            'Hallam Kalora Park 7/152cc,</p><p>Berwick 5/106 def North Dandenong 105,</p><p>Dandenong District ' \
            'Cricket Association-Turf 2</p><p>Round 6</p><p>Dingley 7/211cc def Parkmore Pirates 125,</p><p>Lyndale ' \
            '170 def Narre North 130,</p><p>Dandenong West 4/114cc def Cranbourne 108,</p><p>Narre Warren 4/107 def ' \
            'Beaconsfield 106,</p><p>Dandenong District Cricket Association-Turf 3</p><p>Round 6</p><p>Parkfield ' \
            '1/135 def Silverton 6/132cc,</p><p>Springvale 9/209cc def Lynbrook 147,</p><p>Keysborough 8/122 def ' \
            'Fountain Gate 121,</p><p>Coomoora 7/244cc def Berwick Springs 7/134,</p>'


class StripParagrahpsTestCase(unittest.TestCase):
    def test_normal_story(self):
        article = {
            'body_html': body_html}

        strip_paragraphs(article)
        self.assertTrue(
            article['body_html'].startswith('<p>Dandenong District Cricket Association-Turf 1&nbsp;Round 6&nbsp;'))

    def test_with_breaks(self):
        article = {'body_html': '<div><p>one <b>two</b></p></div>'}
        strip_paragraphs(article)
        self.assertTrue(
            article['body_html'].startswith('<p>one two &nbsp;</p>'))
