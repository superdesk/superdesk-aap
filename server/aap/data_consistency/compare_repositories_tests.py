# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import superdesk
from eve.utils import ParsedRequest
from superdesk.tests import TestCase
from superdesk import get_resource_service
from aap.data_consistency.compare_repositories import CompareRepositories
from aap.data_consistency import init_app as consistency_init
from eve.methods.common import resolve_document_etag
from bson.objectid import ObjectId


class CompareRepositoriesTestCase(TestCase):
    def setUp(self):
        self.app.data.insert('desks', [{
            '_id': ObjectId('123456789abcdef123456789'),
            'name': 'COMMISSION'
        }])

    def test_compare_repos(self):
        with self.app.app_context():
            req = ParsedRequest()
            req.args = {}
            req.max_results = 25

            data = [{'headline': 'test {}'.format(i), 'slugline': 'rebuild {}'.format(i), 'state': 'in_progress',
                     'task': {'desk': ObjectId('123456789abcdef123456789')},
                     'type': 'text' if (i % 2 == 0) else 'picture'} for i in range(1, 100)]
            resolve_document_etag(data, 'archive')
            superdesk.app.data._search_backend('archive').bulk_insert('archive', data)
            get_resource_service('archive').post(data)
            consistency_init(self.app)

            items = get_resource_service('archive').get(req, {})
            self.assertEquals(198, items.count())

            consistency_record = CompareRepositories().run('archive',
                                                           self.app.config['ELASTICSEARCH_URL'],
                                                           self.app.config['ELASTICSEARCH_INDEXES'].get('archive'))
            self.assertEquals(consistency_record['mongo'], 99)
            self.assertEquals(consistency_record['elastic'], 198)
            self.assertEquals(consistency_record['identical'], 99)
            self.assertEquals(consistency_record['mongo_only'], 0)
            self.assertEquals(consistency_record['elastic_only'], 99)
            self.assertEquals(consistency_record['inconsistent'], 0)

    def test_processing_results_all_equal(self):
        consistency_record = {}
        elastic_items = [('item-1', 'abc'), ('item-2', 'xyz')]
        mongo_items = [('item-1', 'abc'), ('item-2', 'xyz')]
        updated_mongo_items = []

        CompareRepositories().process_results(consistency_record,
                                              elastic_items,
                                              mongo_items,
                                              updated_mongo_items,
                                              analyse_differences=False)

        self.assertEquals(consistency_record['mongo'], 2)
        self.assertEquals(consistency_record['elastic'], 2)
        self.assertEquals(consistency_record['identical'], 2)
        self.assertEquals(consistency_record['mongo_only'], 0)
        self.assertEquals(consistency_record['elastic_only'], 0)
        self.assertEquals(consistency_record['inconsistent'], 0)

    def test_processing_results_all_different(self):
        consistency_record = {}
        elastic_items = [('item-1', 'abc'), ('item-2', 'xyz')]
        mongo_items = [('item-1', 'abcd'), ('item-2', 'wxyz')]
        updated_mongo_items = []
        compare_repos = CompareRepositories()
        compare_repos.resource_name = 'archive'

        compare_repos.process_results(consistency_record,
                                      elastic_items,
                                      mongo_items,
                                      updated_mongo_items,
                                      analyse_differences=False)

        self.assertEquals(consistency_record['mongo'], 2)
        self.assertEquals(consistency_record['elastic'], 2)
        self.assertEquals(consistency_record['identical'], 0)
        self.assertEquals(consistency_record['mongo_only'], 0)
        self.assertEquals(consistency_record['elastic_only'], 0)
        self.assertEquals(consistency_record['inconsistent'], 2)

    def test_processing_results_mongo_has_updated_items(self):
        consistency_record = {}
        elastic_items = [('item-1', 'abc'), ('item-2', 'xyz')]
        mongo_items = [('item-1', 'abcd'), ('item-2', 'wxyz')]
        updated_mongo_items = ['item-1']

        CompareRepositories().process_results(consistency_record,
                                              elastic_items,
                                              mongo_items,
                                              updated_mongo_items,
                                              analyse_differences=False)

        self.assertEquals(consistency_record['mongo'], 2)
        self.assertEquals(consistency_record['elastic'], 2)
        self.assertEquals(consistency_record['identical'], 0)
        self.assertEquals(consistency_record['mongo_only'], 0)
        self.assertEquals(consistency_record['elastic_only'], 0)
        self.assertEquals(consistency_record['inconsistent'], 1)

    def test_processing_results_distinct_items_exists(self):
        consistency_record = {}
        elastic_items = [('item-1', 'abc'), ('item-2', 'xyz'), ('item-3', 'xyz')]
        mongo_items = [('item-1', 'abc'), ('item-2', 'xyz'), ('item-4', 'xyz')]
        updated_mongo_items = []

        CompareRepositories().process_results(consistency_record,
                                              elastic_items,
                                              mongo_items,
                                              updated_mongo_items,
                                              analyse_differences=False)

        self.assertEquals(consistency_record['mongo'], 3)
        self.assertEquals(consistency_record['elastic'], 3)
        self.assertEquals(consistency_record['identical'], 2)
        self.assertEquals(consistency_record['mongo_only'], 1)
        self.assertEquals(consistency_record['elastic_only'], 1)
        self.assertEquals(consistency_record['inconsistent'], 0)
