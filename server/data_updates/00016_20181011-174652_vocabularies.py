# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author : superdesk
# Creation: 2018-10-11 17:46

from os import path
import aap
from flask import json

from superdesk.commands.data_updates import BaseDataUpdate


class DataUpdate(BaseDataUpdate):

    resource = 'vocabularies'

    def forwards(self, mongodb_collection, mongodb_database):
        dirname = path.dirname(path.realpath(aap.__file__))
        vocab_path = path.normpath(path.join(dirname, "../data", "vocabularies.json"))
        with open(vocab_path, 'r') as f:
            vocabs = {
                item["_id"]: item
                for item in json.loads(f.read())
                if item["_id"] in ["regions", "countries"]
            }

        if not mongodb_collection.find({"_id": "regions"}):
            mongodb_collection.insert(vocabs["regions"])
        else:
            mongodb_collection.update(
                {"_id": "regions"},
                {"$set": {"items": vocabs["regions"]["items"]}}
            )

        if not mongodb_collection.find({"_id": "countries"}):
            mongodb_collection.insert(vocabs["countries"])
        else:
            mongodb_collection.update(
                {"_id": "countries"},
                {"$set": {"items": vocabs["countries"]["items"]}}
            )

        mongodb_collection.remove("contact_states")

    def backwards(self, mongodb_collection, mongodb_database):
        mongodb_collection.remove("regions")
        mongodb_collection.remove("countries")
        mongodb_collection.insert(
            [
                {
                    "_id": "contact_states",
                    "helper_text": "The administrative state or region of an address",
                    "schema": {
                        "name": {

                        },
                        "qcode": {

                        }
                    },
                    "type": "manageable",
                    "display_name": "State / Region",
                    "unique_field": "qcode",
                    "items": [
                        {
                            "qcode": "NSW",
                            "name": "NSW",
                            "is_active": True
                        },
                        {
                            "qcode": "VIC",
                            "name": "VIC",
                            "is_active": True
                        },
                        {
                            "qcode": "TAS",
                            "name": "TAS",
                            "is_active": True
                        },
                        {
                            "qcode": "WA",
                            "name": "WA",
                            "is_active": True
                        },
                        {
                            "qcode": "QLD",
                            "name": "QLD",
                            "is_active": True
                        },
                        {
                            "qcode": "NT",
                            "name": "NT",
                            "is_active": True
                        },
                        {
                            "qcode": "ACT",
                            "name": "ACT",
                            "is_active": True
                        }
                    ]
                }
            ]
        )
