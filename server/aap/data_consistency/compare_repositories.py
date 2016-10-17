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
import requests
from superdesk.utc import utcnow
from eve.utils import ParsedRequest
import json
from superdesk.default_settings import ELASTICSEARCH_INDEX, ELASTICSEARCH_URL


class CompareRepositories(superdesk.Command):
    default_page_size = 500

    option_list = [
        superdesk.Option('--resource', '-r', dest='resource_name', required=True),
        superdesk.Option('--analysiscount', '-a', dest='analysis_count', required=True)
    ]

    resource_name = ''
    analysis_count = 100

    def get_mongo_items(self, consistency_record):
        # get the records from mongo in chunks
        projection = dict(superdesk.resources[self.resource_name].endpoint_schema['datasource']['projection'])
        superdesk.resources[self.resource_name].endpoint_schema['datasource']['projection'] = None
        service = superdesk.get_resource_service(self.resource_name)
        cursor = service.get_from_mongo(None, {})
        count = cursor.count()
        no_of_buckets = len(range(0, count, self.default_page_size))
        mongo_items = []
        updated_mongo_items = []
        request = ParsedRequest()
        request.projection = json.dumps({'_etag': 1, '_updated': 1})
        for x in range(0, no_of_buckets):
            skip = x * self.default_page_size
            print('Page : {}, skip: {}'.format(x + 1, skip))
            # don't get any new records since the elastic items are retrieved
            cursor = service.get_from_mongo(request, {'_created': {'$lte': consistency_record['started_at']}})
            cursor.skip(skip)
            cursor.limit(self.default_page_size)
            cursor = list(cursor)
            mongo_items.extend([(mongo_item['_id'], mongo_item['_etag']) for mongo_item in cursor])
            updated_mongo_items.extend([mongo_item['_id'] for mongo_item in cursor
                                       if mongo_item['_updated'] > consistency_record['started_at']])

        superdesk.resources[self.resource_name].endpoint_schema['datasource']['projection'] = projection
        return mongo_items, updated_mongo_items

    def get_mongo_item(self, id):
        service = superdesk.get_resource_service(self.resource_name)
        return list(service.get_from_mongo(None, {'_id': id}))[0]

    def get_elastic_item(self, id):
        resource = superdesk.get_resource_service(self.resource_name)
        query = {'query': {'filtered': {'filter': {'term': {'_id': id}}}}}
        request = ParsedRequest()
        request.args = {'source': json.dumps(query)}
        items = resource.get(req=request, lookup=None)
        return items[0]

    def get_elastic_items(self, elasticsearch_index, elasticsearch_url):
        # get the all hits from elastic
        post_data = {'fields': '_etag'}
        response = requests.post('{}/{}/{}'.format(elasticsearch_url,
                                                   elasticsearch_index,
                                                   '_search?size=250000&q=*:*'),
                                 params=post_data)
        elastic_results = response.json()["hits"]["hits"]
        elastic_items = [(elastic_item['_id'], elastic_item["fields"]['_etag'][0])
                         for elastic_item in elastic_results]
        return elastic_items

    def process_results(self,
                        consistency_record,
                        elastic_items,
                        mongo_items,
                        updated_mongo_items,
                        analyse_differences=True):
        # form the sets
        mongo_item_ids = list(map(list, zip(*mongo_items)))[0]
        mongo_item_ids_set = set(mongo_item_ids)
        elastic_item_ids = list(map(list, zip(*elastic_items)))[0]
        elastic_item_ids_set = set(elastic_item_ids)
        mongo_items_set = set(mongo_items)
        elastic_items_set = set(elastic_items)
        updated_mongo_items_set = set(updated_mongo_items)
        differences = []

        # items that exist both in mongo and elastic with the same etags
        shared_items = mongo_items_set & elastic_items_set
        # items that exist only in mongo but not in elastic
        mongo_only = mongo_item_ids_set - elastic_item_ids_set
        # items that exist only in elastic but not in mongo
        elastic_only = elastic_item_ids_set - mongo_item_ids_set
        # items that exist both in mongo and elastic with different etags
        # filter out the ones that has been updated since elastic is queried
        different_items = (elastic_items_set ^ mongo_items_set) - updated_mongo_items_set
        if len(different_items) > 0:
            different_items = set(list(map(list, zip(*list(different_items))))[0]) \
                - updated_mongo_items_set \
                - mongo_only \
                - elastic_only

            if analyse_differences:
                differences = self.analyse_differences(different_items)

        consistency_record['completed_at'] = utcnow()
        consistency_record['mongo'] = len(mongo_items)
        consistency_record['elastic'] = len(elastic_items)
        consistency_record['identical'] = len(shared_items)
        consistency_record['mongo_only'] = len(mongo_only)
        consistency_record['mongo_only_ids'] = list(mongo_only)
        consistency_record['elastic_only'] = len(elastic_only)
        consistency_record['elastic_only_ids'] = list(elastic_only)
        consistency_record['inconsistent'] = len(different_items)
        consistency_record['inconsistent_ids'] = list(different_items)
        consistency_record['differences'] = differences

    def analyse_differences(self, different_items):
        all_differences = []
        counter = 1

        for item in different_items:
            differences = []
            mongo_item = self.get_mongo_item(item)
            elastic_item = self.get_elastic_item(item)
            print('Analysing item# {}'.format(counter))
            self.compare_dicts(mongo_item, elastic_item, differences)
            all_differences.append({'_id': item, 'differences': differences})
            counter += 1
            if counter > self.analysis_count:
                break

        return all_differences

    def are_lists_equal(self, list_1, list_2):
        if len(list_1) > 0 and not isinstance(list_1[0], dict):
            return len(list(set(list_1) ^ set(list_2))) > 0
        else:
            return True

    def compare_dicts(self, dict_1, dict_2, differences=None):
        if differences is None:
            differences = list()

        diff_keys = list(set(dict_1.keys()) ^ set(dict_2.keys()))
        if len(diff_keys) > 0:
            # there are differences in keys so report them
            differences.extend(diff_keys)

        self.compare_dict_values(dict_1, dict_2, differences)

        return list(set(differences))

    def compare_dict_values(self, dict_1, dict_2, differences=None):
        if differences is None:
            differences = list()

        for key in dict_1.keys():
            if key in differences:
                continue

            if key not in dict_2:
                differences.append(key)
                continue

            if isinstance(dict_1[key], list):
                if not self.are_lists_equal(dict_1[key], dict_2[key]):
                    differences.append(key)
            elif isinstance(dict_1[key], dict):
                differences.extend(self.compare_dicts(dict_1[key], dict_2[key]))
            else:
                if not dict_1[key] == dict_2[key]:
                    differences.append(key)

    def run(self, resource_name,
            elasticsearch_url=ELASTICSEARCH_URL,
            elasticsearch_index=ELASTICSEARCH_INDEX,
            analysis_count=100):
        """
        Compares the records in mongo and elastic for a given collection
        Saves the results to "consistency" collection
        :param resource_name: Name of the collection i.e. ingest, archive, published, text_archive
        :param elasticsearch_url: url of the elasticsearch
        :param elasticsearch_index: name of the index
        :param analysis_count: number of inconsistencies to be analyzed
        :return: dictionary of findings
        """
        print('Comparing data in mongo:{} and elastic:{}'.format(resource_name, resource_name))
        consistency_record = {}
        consistency_record['started_at'] = utcnow()
        consistency_record['resource_name'] = resource_name
        self.resource_name = resource_name
        self.analysis_count = analysis_count

        elastic_items = self.get_elastic_items(elasticsearch_index, elasticsearch_url)
        print('Retreiving {} items from mongo'.format(len(elastic_items)))

        mongo_items, updated_mongo_items = self.get_mongo_items(consistency_record)
        self.process_results(consistency_record, elastic_items, mongo_items, updated_mongo_items)
        superdesk.get_resource_service('consistency').post([consistency_record])
        return consistency_record


superdesk.command('app:compare_repositories', CompareRepositories())
