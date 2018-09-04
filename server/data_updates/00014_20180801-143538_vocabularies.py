# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : superdesk
# Creation: 2018-08-01 14:35

from superdesk.commands.data_updates import DataUpdate
from superdesk import get_resource_service
from eve.utils import config


class DataUpdate(DataUpdate):
    resource = 'vocabularies'

    vocabs = [{
        '_id': 'assignment_priority',
        'field_type': None,
        'display_name': 'Assignment Priority',
        'type': 'manageable',
        'unique_field': 'qcode',
        'items': [
            {
                'is_active': True,
                'name': 'High',
                'qcode': 1
            },
            {
                'is_active': True,
                'name': 'Medium',
                'qcode': 2
            },
            {
                'is_active': True,
                'name': 'Low',
                'qcode': 3
            }
        ],
        'schema': {'qcode': {'type': 'integer'}, 'name': {'type': 'string'}}
    },
        {
            '_id': 'contact_job_titles',
            'display_name': 'Contact Job titles/roles',
            'type': 'manageable',
            'unique_field': 'qcode',
            'schema': {'qcode': {'type': 'string'}, 'name': {'type': 'string'}},
            'items': [
                {
                    'name': 'Director',
                    'is_active': True,
                    'qcode': 'director'
                },
                {
                    'name': 'Media Advisor',
                    'is_active': True,
                    'qcode': 'media_advisor'
                },
                {
                    'name': 'Publicity Officer',
                    'is_active': True,
                    'qcode': 'publicity_officer'
                },
                {
                    'name': 'Spokesperson',
                    'is_active': True,
                    'qcode': 'spokesperson'
                },
                {
                    'name': 'Spokeswoman',
                    'is_active': True,
                    'qcode': 'spokeswoman'
                },
                {
                    'name': 'President',
                    'is_active': True,
                    'qcode': 'president'
                },
                {
                    'name': 'CEO',
                    'is_active': True,
                    'qcode': 'ceo'
                },
                {
                    'name': 'Vice President',
                    'is_active': True,
                    'qcode': 'vice_presedent'
                },
                {
                    'name': 'Chairman',
                    'is_active': True,
                    'qcode': 'chairman'
                },
                {
                    'name': 'Carer',
                    'is_active': True,
                    'qcode': 'carer'
                },
                {
                    'name': 'General Secretary',
                    'is_active': True,
                    'qcode': 'general_secretary'
                },
                {
                    'name': 'Media Officer',
                    'is_active': True,
                    'qcode': 'media_officer'
                },
                {
                    'name': 'Mayor',
                    'is_active': True,
                    'qcode': 'mayor'
                },
                {
                    'name': 'Lord Mayor',
                    'is_active': True,
                    'qcode': 'lord_mayor'
                },
                {
                    'name': 'Director of Media',
                    'is_active': True,
                    'qcode': 'director_of_media'
                },
                {
                    'name': 'Media Contact',
                    'is_active': True,
                    'qcode': 'media_contact'
                },
                {
                    'name': 'Spokesman',
                    'is_active': True,
                    'qcode': 'spokesman'
                },
                {
                    'name': 'Communications Advisor',
                    'is_active': True,
                    'qcode': 'communications_advisor'
                }
            ]},
        {
            '_id': 'contact_mobile_usage',
            'display_name': 'Contact mobile usage',
            'type': 'manageable',
            'unique_field': 'qcode',
            'items': [
                {
                    'is_active': True,
                    'qcode': 'Confidential',
                    'name': 'Confidential number',
                    'public': False
                },
                {
                    'is_active': True,
                    'qcode': 'Business',
                    'name': 'Business number',
                    'public': True
                }
            ],
            'schema': {
                'name': {'type': 'string'},
                'qcode': {'type': 'string'},
                'public': {
                    'type': 'bool',
                    'label': 'Make public'
                }
            },
            'helper_text': 'Indicates if the contact mobile number is to be made public outside the system'},
        {
            '_id': 'contact_phone_usage',
            'display_name': 'Contact phone usage',
            'type': 'manageable',
            'unique_field': 'qcode',
            'items': [
                {
                    'is_active': True,
                    'name': 'Confidential number',
                    'qcode': 'Confidential',
                    'public': False
                },
                {
                    'is_active': True,
                    'name': 'Business number',
                    'qcode': 'Business',
                    'public': True
                }
            ],
            'schema': {
                'name': {'type': 'string'},
                'public': {
                    'label': 'Make public',
                    'type': 'bool'
                },
                'qcode': {'type': 'string'}
            },
            'helper_text': 'Indicates if the contact phone number is to be made public outside the system'},
        {
            '_id': 'contact_states',
            'items': [
                {
                    'name': 'NSW',
                    'is_active': True,
                    'qcode': 'NSW'
                },
                {
                    'name': 'VIC',
                    'is_active': True,
                    'qcode': 'VIC'
                },
                {
                    'name': 'TAS',
                    'is_active': True,
                    'qcode': 'TAS'
                },
                {
                    'name': 'WA',
                    'is_active': True,
                    'qcode': 'WA'
                },
                {
                    'name': 'QLD',
                    'is_active': True,
                    'qcode': 'QLD'
                },
                {
                    'name': 'NT',
                    'is_active': True,
                    'qcode': 'NT'
                },
                {
                    'name': 'ACT',
                    'is_active': True,
                    'qcode': 'ACT'
                }
            ],
            'type': 'manageable',
            'unique_field': 'qcode',
            'schema': {
                'name': {'type': 'string'},
                'qcode': {'type': 'string'}
            },
            'display_name': 'Contact Region',
            'helper_text': 'The administrative state or region for the address of a contact'},
        {
            '_id': 'coverage_providers',
            'helper_text': 'News coverage providers',
            'schema': {
                'qcode': {'type': 'string'},
                'name': {'type': 'string'}
            },
            'items': [
                {
                    'qcode': 'agencies',
                    'is_active': True,
                    'name': 'Agencies'
                },
                {
                    'qcode': 'stringer',
                    'is_active': True,
                    'name': 'Stringer'
                },
                {
                    'qcode': 'reuters',
                    'is_active': True,
                    'name': 'Reuters'
                },
                {
                    'qcode': 'associatedpress',
                    'is_active': True,
                    'name': 'Associated Press'
                }
            ],
            'display_name': 'Coverage Providers',
            'type': 'manageable'},
        {
            '_id': 'event_calendars',
            'display_name': 'Event Calendars',
            'type': 'manageable',
            'unique_field': 'qcode',
            'schema': {'qcode': {'type': 'string'}, 'name': {'type': 'string'}},
            'items': [
                {
                    'name': 'Anniversaries',
                    'qcode': 'ann',
                    'is_active': True
                },
                {
                    'name': 'Awards',
                    'qcode': 'Awards',
                    'is_active': True
                },
                {
                    'name': 'Birthdays',
                    'qcode': 'Birthdays',
                    'is_active': True
                },
                {
                    'name': 'Company Meetings',
                    'qcode': 'Company Meetings',
                    'is_active': True
                },
                {
                    'name': 'Community Events',
                    'qcode': 'Community Events',
                    'is_active': True
                },
                {
                    'name': 'Cultural Events',
                    'qcode': 'Cultural Events',
                    'is_active': True
                },
                {
                    'name': 'Entertainment',
                    'qcode': 'entertainment',
                    'is_active': True
                },
                {
                    'name': 'Conferences',
                    'qcode': 'Conferences',
                    'is_active': True
                },
                {
                    'name': 'Court Proceedings',
                    'qcode': 'courts',
                    'is_active': True
                },
                {
                    'name': 'Elections',
                    'qcode': 'Elections',
                    'is_active': True
                },
                {
                    'name': 'Exhibitions',
                    'qcode': 'Exhibitions',
                    'is_active': True
                },
                {
                    'name': 'Festivals',
                    'qcode': 'Festivals',
                    'is_active': True
                },
                {
                    'name': 'Holidays',
                    'qcode': 'holidays',
                    'is_active': True
                },
                {
                    'name': 'Inaugurations & Openings',
                    'qcode': 'Inaugurations & Openings',
                    'is_active': True
                },
                {
                    'name': 'Media Opportunities',
                    'qcode': 'Media Opportunities',
                    'is_active': True
                },
                {
                    'name': 'Observances',
                    'qcode': 'Observances',
                    'is_active': True
                },
                {
                    'name': 'Parliamentary Sittings',
                    'qcode': 'politics',
                    'is_active': True
                },
                {
                    'name': 'Press Conferences',
                    'qcode': 'Press Conferences',
                    'is_active': True
                },
                {
                    'name': 'Promotional Events',
                    'qcode': 'Promotional Events',
                    'is_active': True
                },
                {
                    'name': 'Reserve Bank Fixtures',
                    'qcode': 'Reserve Bank Fixtures',
                    'is_active': True
                },
                {
                    'name': 'Special Events',
                    'qcode': 'Special Events',
                    'is_active': True
                },
                {
                    'name': 'Sport Fixtures',
                    'qcode': 'sport',
                    'is_active': True
                },
                {
                    'name': 'Tournaments & Competitions',
                    'qcode': 'Tournaments & Competitions',
                    'is_active': True
                },
                {
                    'name': 'Trade Fairs & Expos',
                    'qcode': 'Trade Fairs & Expos',
                    'is_active': True
                },
                {
                    'name': 'Weddings',
                    'qcode': 'Weddings',
                    'is_active': True
                },
                {
                    'name': 'Finance Events',
                    'qcode': 'finance',
                    'is_active': True
                },
                {
                    'name': 'World Events',
                    'qcode': 'world',
                    'is_active': True
                }
            ]},
        {
            '_id': 'eventoccurstatus',
            'display_name': 'Event Occurence Status',
            'type': 'manageable',
            'unique_field': 'qcode',
            'schema': {'qcode': {'type': 'string'}, 'name': {'type': 'string'}, 'label': {'type': 'string'}},
            'items': [
                {
                    'is_active': True,
                    'name': 'Unplanned event',
                    'qcode': 'eocstat:eos0',
                    'label': 'Unplanned'
                },
                {
                    'is_active': True,
                    'name': 'Planned, occurence planned only',
                    'qcode': 'eocstat:eos1',
                    'label': 'Tentative'
                },
                {
                    'is_active': True,
                    'name': 'Planned, occurence highly uncertain',
                    'qcode': 'eocstat:eos2',
                    'label': 'Unlikely'
                },
                {
                    'is_active': True,
                    'name': 'Planned, May occur',
                    'qcode': 'eocstat:eos3',
                    'label': 'Possible'
                },
                {
                    'is_active': True,
                    'name': 'Planned, occurence highly likely',
                    'qcode': 'eocstat:eos4',
                    'label': 'Very likely'
                },
                {
                    'is_active': True,
                    'name': 'Planned, occurs certainly',
                    'qcode': 'eocstat:eos5',
                    'label': 'Confirmed'
                },
                {
                    'is_active': True,
                    'name': 'Planned, then cancelled',
                    'qcode': 'eocstat:eos6',
                    'label': 'Cancelled'
                }
            ]},
        {
            '_id': 'g2_content_type',
            'display_name': 'Coverage content types',
            'type': 'manageable',
            'unique_field': 'qcode',
            'schema': {'qcode': {'type': 'string'}, 'name': {'type': 'string'}},
            'items': [
                {
                    'is_active': True,
                    'name': 'Text',
                    'qcode': 'text'
                },
                {
                    'is_active': True,
                    'name': 'Picture',
                    'qcode': 'picture'
                },
                {
                    'is_active': True,
                    'name': 'Video',
                    'qcode': 'video'
                },
                {
                    'is_active': True,
                    'name': 'Audio',
                    'qcode': 'audio'
                },
                {
                    'is_active': True,
                    'name': 'Graphic',
                    'qcode': 'graphic'
                },
                {
                    'is_active': True,
                    'name': 'Live video',
                    'qcode': 'live_video'
                },
                {
                    'is_active': True,
                    'name': 'Live blog',
                    'qcode': 'live_blog'
                }
            ]},
        {
            '_id': 'newscoveragestatus',
            'display_name': 'News Coverage Status',
            'type': 'manageable',
            'unique_field': 'qcode',
            'schema': {'qcode': {'type': 'string'}, 'name': {'type': 'string'}, 'label': {'type': 'string'}},
            'items': [
                {
                    'is_active': True,
                    'qcode': 'ncostat:int',
                    'name': 'coverage intended',
                    'label': 'coverage intended'
                },
                {
                    'is_active': True,
                    'qcode': 'ncostat:notdec',
                    'name': 'coverage not decided yet',
                    'label': 'coverage not decided yet'
                },
                {
                    'is_active': True,
                    'qcode': 'ncostat:notint',
                    'name': 'coverage not intended',
                    'label': 'coverage not intended'
                },
                {
                    'is_active': True,
                    'qcode': 'ncostat:onreq',
                    'name': 'coverage upon request',
                    'label': 'coverage upon request'
                }
            ]},
        {
            '_id': 'annotation_types',
            'display_name': 'Annotation Types',
            'type': 'manageable',
            'unique_field': 'qcode',
            'items': [
                {'is_active': True, 'name': 'Regular', 'qcode': 'regular'},
                {'is_active': True, 'name': 'Remark', 'qcode': 'remark'}
            ],
            'schema': {
                'name': {},
                'qcode': {}
            }}]

    def forwards(self, mongodb_collection, mongodb_database):
        for vocab in self.vocabs:
            v = get_resource_service(self.resource).find_one(req=None, _id=vocab.get('_id'))
            if v:
                print('{} vocabulary already exists in the system.'.format(vocab.get('_id')))
            else:
                print('Injecting {}'.format(vocab.get('_id')))
                get_resource_service(self.resource).post([vocab])
                print('Injected {}\n\n\n'.format(vocab.get('_id')))

        print(mongodb_collection.update_many({'_id': {'$in': ['genre',
                                                              'priority',
                                                              'replace_words',
                                                              'annotation_types']}},
                                             {'$set': {
                                                 'unique_field': "qcode"
                                             }}))
        print(mongodb_collection.update_many({'unique_field': {'$exists': False},
                                              'schema.qcode': {'$exists': True}},
                                             {'$set': {
                                                 'unique_field': "qcode"
                                             }}))
        for vocabulary in mongodb_collection.find({'_id': {'$in': ['priority']}}):
            schema = vocabulary.get('schema', {})
            qcode = schema.get('qcode', {})
            qcode['type'] = 'integer'
            schema['qcode'] = qcode
            schema['name'] = {}
            schema['color'] = {}
            print(mongodb_collection.update({'_id': vocabulary.get(config.ID_FIELD)},
                                            {'$set': {'schema': schema}}))

        for vocabulary in mongodb_collection.find({'_id': {'$in': ['urgency']}}):
            schema = vocabulary.get('schema', {})
            qcode = schema.get('qcode', {})
            qcode['type'] = 'integer'
            schema['qcode'] = qcode
            schema['name'] = {'type': 'string'}
            print(mongodb_collection.update({'_id': vocabulary.get(config.ID_FIELD)},
                                            {'$set': {'schema': schema}}))

        for vocabulary in mongodb_collection.find({'_id': {'$in': ['iptc_category_map']}}):
            schema = {'category': {'type': 'string'}, 'name': {'type': 'string'}, 'qcode': {'type': 'string'}}
            print(mongodb_collection.update({'_id': vocabulary.get(config.ID_FIELD)},
                                            {'$set': {'schema': schema, 'unique_field': 'qcode'}}))

        vocabulary = mongodb_collection.find({'_id': 'crop_sizes'})
        if vocabulary.count():
            schema = {'width': {'type': 'integer'}, 'name': {'type': 'string'}, 'height': {'type': 'integer'}}
            print(mongodb_collection.update({'_id': vocabulary[0].get(config.ID_FIELD)},
                                            {'$set': {'schema': schema, 'unique_field': 'name'}}))

        vocabulary = mongodb_collection.find({'_id': 'rightsinfo'})
        if vocabulary.count():
            schema = {'copyrightNotice': {'type': 'string'}, 'copyrightHolder': {'type': 'string'},
                      'usageTerms': {'type': 'string'}}
            print(mongodb_collection.update({'_id': vocabulary[0].get(config.ID_FIELD)},
                                            {'$set': {'schema': schema, 'unique_field': 'name'}}))

        for vocabulary in mongodb_collection.find({'_id': {'$in': ['geographical_restrictions', 'keywords', 'genre']}}):
            schema = {'qcode': {'type': 'string'}, 'name': {'type': 'string'}}
            print(mongodb_collection.update({'_id': vocabulary.get(config.ID_FIELD)},
                                            {'$set': {'schema': schema, 'unique_field': 'qcode'}}))

        vocabulary = mongodb_collection.find({'_id': 'categories'})
        if vocabulary.count():
            schema = {'name': {'type': 'string'}, 'subject': {'type': 'string'}, 'qcode': {'type': 'string'}}
            print(mongodb_collection.update({'_id': vocabulary[0].get(config.ID_FIELD)},
                                            {'$set': {'schema': schema, 'unique_field': 'qcode'}}))

        vocabulary = mongodb_collection.find({'_id': 'footers'})
        if vocabulary.count():
            schema = {'name': {'type': 'string'}, 'value': {'type': 'string'}}
            print(mongodb_collection.update({'_id': vocabulary[0].get(config.ID_FIELD)},
                                            {'$set': {'schema': schema, 'unique_field': 'name'}}))

        vocabulary = mongodb_collection.find({'_id': 'bom_products'})
        if vocabulary.count():
            schema = {'qcode': {'type': 'string'}, 'name': {'type': 'string'}}
            print(mongodb_collection.update({'_id': vocabulary[0].get(config.ID_FIELD)},
                                            {'$set': {'schema': schema, 'unique_field': 'qcode', '_etag': ''}}))
            print(mongodb_collection.update({'_id': vocabulary[0].get(config.ID_FIELD)},
                                            {'$unset': {'service': 1}}))

        for vocabulary in mongodb_collection.find({}):
            if 'schema' in vocabulary:
                schema = vocabulary['schema']
                for field in ['name', 'qcode']:
                    if field in vocabulary['schema'] and type(vocabulary['schema']) == dict:
                        schema[field]['required'] = True
                mongodb_collection.update({'_id': vocabulary.get(config.ID_FIELD)},
                                          {'$set': {'schema': schema}})

        v = get_resource_service(self.resource).find_one(req=None, _id='subscriber_types')
        if v:
            upd = False
            for f in v.get('items'):
                x = [fmtr for fmtr in f['formats'] if fmtr.get('qcode') == 'agenda_planning']
                if not len(x):
                    f['formats'].append({'name': 'Agenda', 'qcode': 'agenda_planning'})
                    upd = True
                x = [fmtr for fmtr in f['formats'] if fmtr.get('qcode') == 'json_event']
                if not len(x):
                    f['formats'].append({'name': 'JSON Event', 'qcode': 'json_event'})
                    upd = True
                x = [fmtr for fmtr in f['formats'] if fmtr.get('qcode') == 'json_planning']
                if not len(x):
                    f['formats'].append({'name': 'JSON Planning', 'qcode': 'json_planning'})
                    upd = True
                x = [fmtr for fmtr in f['formats'] if fmtr.get('qcode') == 'aap ticker']
                if not len(x):
                    f['formats'].append({'name': 'AAP Ticker', 'qcode': 'aap ticker'})
                    upd = True
            if upd:
                get_resource_service(self.resource).put(v.get(config.ID_FIELD), v)
        upd = False
        v = get_resource_service(self.resource).find_one(req=None, _id='type')
        if v:
            event = [ev for ev in v.get('items') if ev.get('qcode') == 'event']
            if not len(event):
                v['items'].append({'name': 'Event', 'qcode': 'event', 'is_active': True})
                upd = True
            planning = [pl for pl in v.get('items') if pl.get('qcode') == 'planning']
            if not len(planning):
                v['items'].append({'name': 'Planning', 'qcode': 'planning', 'is_active': True})
                upd = True
            featured = [pf for pf in v.get('items') if pf.get('qcode') == 'planning_featured']
            if not len(featured):
                v['items'].append({'name': 'Featured Stories', 'qcode': 'planning_featured', 'is_active': True})
                upd = True
            if upd:
                get_resource_service(self.resource).put(v.get(config.ID_FIELD), v)

    def backwards(self, mongodb_collection, mongodb_database):
        raise NotImplementedError()
