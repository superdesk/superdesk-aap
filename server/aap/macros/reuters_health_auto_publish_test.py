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
from .reuters_health_auto_publish import reuters_health_auto_publish
import datetime


class ReutersHealthAutoPublishTest(TestCase):
    def test_reuters_health_story(self):
        firstcreated = datetime.datetime(2015, 10, 26, 11, 45, 19, 0)
        item = {
            "source": "Reuters",
            "state": "ingested",
            "_id": "tag:localhost:2017:77b03a97-df04-446e-a112-94941f1bb12c",
            "firstcreated": firstcreated,
            "subject": [
                {
                    "name": "lifestyle and leisure",
                    "qcode": "10000000"
                },
                {
                    "name": "politics",
                    "qcode": "11000000"
                },
                {
                    "name": "health",
                    "qcode": "07000000"
                }
            ],
            "place": [
                {
                    "name": "United States"
                }
            ],
            'body_html': '<p>DETROIT (Reuters) - General Motors Co <GM.N> Chief Financial Officer Chuck Stevens \
            said on Wednesday the macroeconomic challenges in Brazil will remain in the near term but the company \
            has \"huge upside leverage once the macro situation changes\" in South America\'s largest \
            economy.</p>\n<p>GM\'s car sales so far in October are up versus a year ago, Stevens said to reporters \
            after the No. 1 U.S. automaker reported third-quarter financial results.</p>\n<p>Stevens also \
            reaffirmed GM\'s past forecasts that it will show profit in Europe in 2016. It would be GM\'s first \
            profit in Europe since 1999.</p>\n<p> (Reporting by Bernie Woodall and Joseph White; \
            Editing by Chizu Nomiyamam and Jeffrey Benkoe)</p>'
        }

        reuters_health_auto_publish(item)
        self.assertEqual(item['subject'],
                         [{"name": "health", "qcode": "07000000"},
                         {"name": "lifestyle and leisure", "qcode": "10000000"},
                         {"name": "politics", "qcode": "11000000"}])
        self.assertEqual(item['place'], [])
        self.assertEqual(item['dateline']['located']['city'], 'Detroit')
        self.assertEqual(item['anpa_category'], [{'name': 'International News', 'qcode': 'i'}])

    def test_reuters_health_story_multiple_health_topic(self):
        firstcreated = datetime.datetime(2015, 10, 26, 11, 45, 19, 0)
        item = {
            "source": "Reuters",
            "state": "ingested",
            "_id": "tag:localhost:2017:77b03a97-df04-446e-a112-94941f1bb12c",
            "firstcreated": firstcreated,
            "subject": [
                {
                    "name": "lifestyle and leisure",
                    "qcode": "10000000"
                },
                {
                    "name": "politics",
                    "qcode": "11000000"
                },
                {
                    "name": "health",
                    "qcode": "07000000"
                },
                {
                    "name": "disease",
                    "qcode": "07001000"
                }
            ],
            "place": [
                {
                    "name": "United States"
                }
            ],
            'body_html': '<p>DETROIT (Reuters) - General Motors Co <GM.N> Chief Financial Officer Chuck Stevens \
            said on Wednesday the macroeconomic challenges in Brazil will remain in the near term but the company \
            has \"huge upside leverage once the macro situation changes\" in South America\'s largest \
            economy.</p>\n<p>GM\'s car sales so far in October are up versus a year ago, Stevens said to reporters \
            after the No. 1 U.S. automaker reported third-quarter financial results.</p>\n<p>Stevens also \
            reaffirmed GM\'s past forecasts that it will show profit in Europe in 2016. It would be GM\'s first \
            profit in Europe since 1999.</p>\n<p> (Reporting by Bernie Woodall and Joseph White; \
            Editing by Chizu Nomiyamam and Jeffrey Benkoe)</p>'
        }

        reuters_health_auto_publish(item)
        self.assertEqual(item['subject'],
                         [{"name": "health", "qcode": "07000000"},
                          {"name": "disease", "qcode": "07001000"},
                          {"name": "lifestyle and leisure", "qcode": "10000000"},
                          {"name": "politics", "qcode": "11000000"}])
        self.assertEqual(item['place'], [])
        self.assertEqual(item['dateline']['located']['city'], 'Detroit')
        self.assertEqual(item['anpa_category'], [{'name': 'International News', 'qcode': 'i'}])

    def test_aap_ingested_story(self):
        firstcreated = datetime.datetime(2015, 10, 26, 11, 45, 19, 0)
        item = {
            "source": "AAP",
            "state": "ingested",
            "_id": "tag:localhost:2017:77b03a97-df04-446e-a112-94941f1bb12c",
            "firstcreated": firstcreated,
            "anpa_category": [
                {
                    "name": "Finance",
                    "qcode": "f"
                }
            ],
            "subject": [
                {
                    "name": "lifestyle and leisure",
                    "qcode": "10000000"
                },
                {
                    "name": "politics",
                    "qcode": "11000000"
                },
                {
                    "name": "diplomacy",
                    "qcode": "11002000"
                }
            ],
            "place": [{"name": "United States"}],
            'body_html': '<p>DETROIT (Reuters) - General Motors Co <GM.N> Chief Financial Officer Chuck Stevens \
            said on Wednesday the macroeconomic challenges in Brazil will remain in the near term but the company \
            has \"huge upside leverage once the macro situation changes\" in South America\'s largest \
            economy.</p>\n<p>GM\'s car sales so far in October are up versus a year ago, Stevens said to reporters \
            after the No. 1 U.S. automaker reported third-quarter financial results.</p>\n<p>Stevens also \
            reaffirmed GM\'s past forecasts that it will show profit in Europe in 2016. It would be GM\'s first \
            profit in Europe since 1999.</p>\n<p> (Reporting by Bernie Woodall and Joseph White; \
            Editing by Chizu Nomiyamam and Jeffrey Benkoe)</p>'
        }

        reuters_health_auto_publish(item)
        self.assertEqual(item['subject'],
                         [{"name": "lifestyle and leisure", "qcode": "10000000"},
                          {"name": "politics", "qcode": "11000000"},
                          {"name": "diplomacy", "qcode": "11002000"}])
        self.assertEqual(item['place'], [{"name": "United States"}])
        self.assertEqual(item.get('dateline', {}).get('located', {}).get('city', ''), '')
        self.assertEqual(item['anpa_category'], [{"name": "Finance", "qcode": "f"}])

    def test_reuters_ingested_category(self):
        firstcreated = datetime.datetime(2015, 10, 26, 11, 45, 19, 0)
        item = {
            "source": "Reuters",
            "state": "ingested",
            "_id": "tag:localhost:2017:77b03a97-df04-446e-a112-94941f1bb12c",
            "anpa_category": [
                {
                    "name": "Finance",
                    "qcode": "f"
                }
            ],
            "firstcreated": firstcreated,
            "subject": [
                {
                    "name": "lifestyle and leisure",
                    "qcode": "10000000"
                },
                {
                    "name": "politics",
                    "qcode": "11000000"
                },
                {
                    "name": "diplomacy",
                    "qcode": "11002000"
                }
            ],
            "place": [
                {
                    "name": "United States"
                }
            ],
            'body_html': '<p>DETROIT (Reuters) - General Motors Co <GM.N> Chief Financial Officer Chuck Stevens \
            said on Wednesday the macroeconomic challenges in Brazil will remain in the near term but the company \
            has \"huge upside leverage once the macro situation changes\" in South America\'s largest \
            economy.</p>\n<p>GM\'s car sales so far in October are up versus a year ago, Stevens said to reporters \
            after the No. 1 U.S. automaker reported third-quarter financial results.</p>\n<p>Stevens also \
            reaffirmed GM\'s past forecasts that it will show profit in Europe in 2016. It would be GM\'s first \
            profit in Europe since 1999.</p>\n<p> (Reporting by Bernie Woodall and Joseph White; \
            Editing by Chizu Nomiyamam and Jeffrey Benkoe)</p>'
        }

        reuters_health_auto_publish(item)
        self.assertEqual(item['subject'],
                         [{"name": "lifestyle and leisure", "qcode": "10000000"},
                          {"name": "politics", "qcode": "11000000"},
                          {"name": "diplomacy", "qcode": "11002000"}])
        self.assertEqual(item['place'], [])
        self.assertEqual(item['dateline']['located']['city'], 'Detroit')
        self.assertEqual(item['anpa_category'], [{'name': 'International News', 'qcode': 'i'}])
