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
from .preserve_format import preserve


class PreserveFormatTestCase(unittest.TestCase):

    def test_story_with_p_tags(self):
        text = '<p>A</p>' \
               '<p>B</p>' \
               '<p>C</p>' \
               '<p>D</p>' \

        item = {'body_html': text}
        res, diff = preserve(item)
        self.assertEqual(item['body_html'], '<pre>A\nB\nC\nD\n</pre>')

    def test_story_with_p_br_tags(self):
        text = '<p>A</p>' \
               '<p>B<br></p>' \
               '<p>C</p>' \
               '<p><br></p>' \
               '<p>D</p>' \

        item = {'body_html': text}
        res, diff = preserve(item)
        self.assertEqual(item['body_html'], '<pre>A\nB\nC\n\nD\n</pre>')

    def test_story_with_p_br_tags2(self):
        text = '<p>A</p>' \
               '<p>B<br></p>' \
               '<br>' \
               '<p>C</p>' \
               '<p><br></p>' \
               '<p>D</p>' \

        item = {'body_html': text}
        res, diff = preserve(item)
        self.assertEqual(item['body_html'], '<pre>A\nB\n\nC\n\nD\n</pre>')

    def test_story_with_div_p_tags(self):
        text = '<div><p>A</p>' \
               '<p>B<br></p>' \
               '<br>' \
               '<p><span style=\"background-color: transparent;\">C</span></p>' \
               '<p><br></p>' \
               '<p>D</p></div>' \

        item = {'body_html': text}
        res, diff = preserve(item)
        self.assertEqual(item['body_html'], '<pre>A\nB\n\n\nC\n\nD\n</pre>')

    def test_story_with_pre_tags(self):
        text = '<pre>A\n</pre>' \
               '<pre>B\n</pre>' \
               '<pre>C\n</pre>' \
               '<pre>D\n</pre>' \

        item = {'body_html': text}
        res, diff = preserve(item)
        self.assertEqual(item['body_html'], '<pre>A\nB\nC\nD\n</pre>')

    def test_story_with_pre_p_tags(self):
        text = '<pre>A\n</pre>' \
               '<p>B</p>' \
               '<pre>C\n</pre>' \
               '<pre>D\n</pre>' \

        item = {'body_html': text}
        res, diff = preserve(item)
        self.assertEqual(item['body_html'], '<pre>A\nB\nC\nD\n</pre>')

    def test_story_with_pre_p_span_tags(self):
        text = '<pre><p>A</p></pre>' \
               '<p>B<br></p>' \
               '<p><span style=\"background-color: transparent;\">C</span></p>' \
               '<p><br></p>' \
               'D\n</pre>' \

        item = {'body_html': text}
        res, diff = preserve(item)
        self.assertEqual(item['body_html'], '<pre>A\nB\nC\n\nD\n</pre>')

    def test_story_with_div_pre_tags(self):
        text = '<pre><div><p>A</p>' \
               '<p>B<br></p>' \
               '<br>' \
               '<p><span style=\"background-color: transparent;\">C</span></p>' \
               '<p><br></p>' \
               '<p>D</p></div></pre>' \

        item = {'body_html': text}
        res, diff = preserve(item)
        self.assertEqual(item['body_html'], '<pre>AB\n\nC\nD\n</pre>')
