# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author : superdesk
# Creation: 2019-01-23 11:08

from superdesk.commands.data_updates import DataUpdate as Update
from superdesk import get_resource_service

SINGLE = 'single selection'
MULTI = 'multi selection'
NONE = 'do not show'

selection_map = {
    'genre': SINGLE,
    'urgency': SINGLE,
    'locators': SINGLE,
    'priority': SINGLE,
    'footers': SINGLE,

    'iptc_category_map': MULTI,
    'keywords': MULTI,
    'categories': MULTI,
    'default_categories': MULTI,
    'company_codes': MULTI,

    'desk_types': NONE,
    'subscriber_types': NONE,
    'crop_sizes': NONE,
    'type': NONE,
    'signal': NONE,
    'replace_words': NONE,
    'product_types': NONE,
    'bom_products': NONE,
    'contact_job_titles': NONE,
    'contact_mobile_usage': NONE,
    'contact_phone_usage': NONE,
    'annotation_types': NONE,
    'g2_content_type': NONE,
    'geographical_restrictions': NONE,
    'rightsinfo': NONE,
    'assignment_priority': NONE,
    'regions': NONE,
    'countries': NONE,
    'coverage_providers': NONE,
    'eventoccurstatus': NONE,
    'newscoveragestatus': NONE,
    'event_calendars': NONE
}


class DataUpdate(Update):

    resource = 'vocabularies'

    def forwards(self, mongodb_collection, mongodb_database):
        vocabularies_service = get_resource_service('vocabularies')
        for vocabulary in vocabularies_service.get(req=None, lookup=None):
            vocab_id = vocabulary['_id']

            mongodb_collection.update({'_id': vocab_id}, {
                '$set': {'selection_type': selection_map.get(vocab_id) or MULTI},
                '$unset': {'single_value': 1}
            })

    def backwards(self, mongodb_collection, mongodb_database):
        vocabularies_service = get_resource_service('vocabularies')
        for vocabulary in vocabularies_service.get(req=None, lookup=None):
            single_value = vocabulary.get('selection_type') == 'single selection'
            mongodb_collection.update({'_id': vocabulary['_id']}, {
                '$set': {'single_value': single_value},
                '$unset': {'selection_type': 1}
            })
