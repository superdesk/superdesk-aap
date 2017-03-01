# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015, 2016, 2017 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from bson.objectid import ObjectId
from superdesk.tests import TestCase
from .export_legal_archive_to_archived import ExportLegalArchiveToArchived
from superdesk import get_resource_service


class ExportLegalArchiveToArchivedTest(TestCase):
    def setUp(self):
        self.app.data.insert('desks', [{
            '_id': ObjectId('123456789abcdef123456789'),
            'name': 'COMMISSION'
        }])

        self.app.data.insert('legal_archive', [
            {
                '_id': 'urn:newsml:localhost:2016-07-19T10:55:52.804692:7504fd81-b423-4a8d-a98e-3cae0d18726a',
                'task': {'desk': 'COMMISSION'},
                'type': 'text'
            },
            {
                '_id': 'urn:newsml:localhost:2016-07-19T10:55:52.804692:7504fd81-b423-4a8d-a98e-3cae0d18726b',
                'task': {'desk': 'COMMISSION'},
                'type': 'text'
            },
            {
                '_id': 'urn:newsml:localhost:2016-07-19T10:55:52.804692:7504fd81-b423-4a8d-a98e-3cae0d18726c',
                'task': {'desk': 'COMMISSION'},
                'type': 'composite'
            },
            {
                '_id': 'urn:newsml:localhost:2016-07-19T10:55:52.804692:7504fd81-b423-4a8d-a98e-3cae0d18726d',
                'task': {'desk': 'Sports'},
                'type': 'text'
            }
        ])

        self.script = ExportLegalArchiveToArchived()

    def test_get_desk_id(self):
        desk_id = self.script._get_desk_id()
        self.assertEqual(desk_id, ObjectId('123456789abcdef123456789'))

    def test_get_desk_id_fail(self):
        self.script.default_desk = 'DoesntExist'
        desk_id = self.script._get_desk_id()
        self.assertIsNone(desk_id)

    def test_get_items(self):
        legal_archive_items = self.script._get_items()

        self.assertEqual(len(legal_archive_items), 2)
        self.assertEqual(
            legal_archive_items[0]['_id'],
            'urn:newsml:localhost:2016-07-19T10:55:52.804692:7504fd81-b423-4a8d-a98e-3cae0d18726a'
        )
        self.assertEqual(legal_archive_items[0]['type'], 'text')

    def test_generate_archived_item(self):
        desk_id = self.script._get_desk_id()
        legal_archive_items = self.script._get_items()
        archived_item = self.script._generate_archived_item(legal_archive_items[0], desk_id)

        self.assertEqual(archived_item['task']['desk'], desk_id)
        self.assertEqual(archived_item['item_id'], legal_archive_items[0]['_id'])

    def test_add_to_archived(self):
        desk_id = self.script._get_desk_id()
        legal_archive_items = self.script._get_items()

        items = list()
        for item in legal_archive_items:
            items.append(self.script._generate_archived_item(item, desk_id))

        archived_items = self.script._add_to_archived(items)

        self.assertEqual(len(archived_items), 2)

    def test_run(self):
        self.script.run()
        archived_service = get_resource_service('archived')
        archived_items = list(archived_service.get(req=None, lookup=None))

        self.assertEqual(len(archived_items), 2)
        self.assertEqual(archived_items[0]['task']['desk'], '123456789abcdef123456789')
        self.assertEqual(archived_items[1]['task']['desk'], '123456789abcdef123456789')
