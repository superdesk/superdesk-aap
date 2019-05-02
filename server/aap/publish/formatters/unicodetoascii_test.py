# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from unittest import TestCase

from .unicodetoascii import to_ascii, clean_string


class ToAsciiConverterTest(TestCase):
    def TestCase(self):
        self.assertEqual(to_ascii('a'), 'a')
        self.assertEqual(to_ascii('aÀ'), 'aA')
        self.assertEqual(to_ascii('aÀÄ'), 'aAA')
        self.assertEqual(to_ascii('Æ'), 'AE')
        self.assertEqual(to_ascii('Ð'), 'D')
        self.assertEqual(to_ascii('Î'), 'I')
        self.assertEqual(to_ascii('ô'), 'o')
        self.assertEqual(to_ascii('Ɯ'), 'W')
        self.assertEqual(to_ascii('Ɔ'), 'O')
        self.assertEqual(to_ascii('ȹ'), 'qp')
        self.assertEqual(to_ascii('´'), '\'')
        self.assertEqual(to_ascii('`'), '`')
        self.assertEqual(to_ascii('"'), '"')
        # self.assertEqual(to_ascii('ʹ'), 'ʹ')
        self.assertEqual(to_ascii('ʻ'), '`')
        self.assertEqual(to_ascii('ʼ'), '\'')
        self.assertEqual(to_ascii('ʺ'), '"')
        self.assertEqual(to_ascii('̀'), '')
        self.assertEqual(to_ascii('ˮ'), '"')
        self.assertEqual(to_ascii(None), '')
        self.assertEqual(to_ascii(''), '')


class CleanStringTest(TestCase):
    def TestClean(self):
        self.assertEqual(clean_string('ˮ'), '"')
        self.assertEqual(clean_string('´'), '\'')
        self.assertEqual(clean_string('`'), '`')
        self.assertEqual(clean_string('"'), '"')
        self.assertEqual(to_ascii('ʹ'), '\'')
        self.assertEqual(clean_string('ʻ'), '\'')
        self.assertEqual(clean_string('ʼ'), '\'')
        self.assertEqual(clean_string('ʺ'), '"')
        self.assertEqual(clean_string('̀'), '\'')
        self.assertEqual(clean_string('ˮ'), '"')
