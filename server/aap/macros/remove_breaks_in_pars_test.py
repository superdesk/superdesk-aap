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
from .remove_breaks_in_pars import remove_breaks


class PreserveFormatTestCase(unittest.TestCase):

    def test_para_with_one_break(self):
        text = '<p>A<br>B</p>'

        item = {'body_html': text}
        remove_breaks(item)
        self.assertEqual(item['body_html'], '<p>A B</p>')

    def test_para_with_one_break2(self):
        text = '<p>A B</p><br>C'

        item = {'body_html': text}
        remove_breaks(item)
        self.assertEqual(item['body_html'], '<p>A B</p> C')
        pass

    def test_para_no_html(self):
        text = 'test test'

        item = {'body_html': text}
        remove_breaks(item)
        self.assertEqual(item['body_html'], 'test test')
        pass

    def test_pre_tag(self):
        text = '<pre>A <br> B</pre>'

        item = {'body_html': text}
        remove_breaks(item)
        self.assertEqual(item['body_html'], '<pre>A   B</pre>')
        pass
