# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
import json

from apps.publish import init_app
from bson import ObjectId
from eve.utils import config
from superdesk.metadata.item import ITEM_TYPE, PACKAGE_TYPE
from superdesk.publish.subscribers import SUBSCRIBER_TYPES
from superdesk.tests import TestCase
from superdesk.utc import utcnow

from .aap_bulletinbuilder_formatter import AAPBulletinBuilderFormatter


class AapBulletinBuilderFormatterTest(TestCase):
    subscribers = [{"_id": "1", "name": "Test", "subscriber_type": SUBSCRIBER_TYPES.WIRE, "media_type": "media",
                    "is_active": True, "sequence_num_settings": {"max": 10, "min": 1},
                    "destinations": [{"name": "AAP Bulletin Builder", "delivery_type": "pull",
                                      "format": "AAP BULLETIN BUILDER"
                                      }]
                    }]

    desks = [
        {"name": "Sports"}, {"name": "New Zealand"}
    ]

    def setUp(self):
        self.app.data.insert('subscribers', self.subscribers)
        self.app.data.insert('desks', self.desks)
        init_app(self.app)
        self._formatter = AAPBulletinBuilderFormatter()

    def test_bulletin_builder_formatter(self):
        article = {
            config.ID_FIELD: '123',
            config.VERSION: 2,
            'source': 'AAP',
            'anpa_category': [{'qcode': 'a'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '02011001'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'preformatted',
            'body_html': 'The story body',
            'abstract': 'abstract',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId()
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        self.assertEqual(article[config.ID_FIELD], item.get('id'))
        self.assertEqual(article[config.VERSION], item.get('version'))
        self.assertEqual(article[ITEM_TYPE], item.get(ITEM_TYPE))
        self.assertEqual(article.get(PACKAGE_TYPE, ''), item.get(PACKAGE_TYPE))
        self.assertEqual(article['headline'], item.get('headline'))
        self.assertEqual(article['slugline'], item.get('slugline'))
        formatted_item = json.loads(item.get('data'))
        self.assertEqual(article['headline'], formatted_item['headline'])

    def test_strip_html(self):
        article = {
            config.ID_FIELD: '123',
            config.VERSION: 2,
            'source': 'AAP',
            'headline': 'This is a test headline&nbsp;<span></span>',
            'slugline': 'slugline',
            'abstract': '<p>abstract</p>',
            'type': 'text',
            'anpa_category': [{'qcode': 'a', 'name': 'Australian General News'}],
            'flags': {
                'marked_for_legal': True
            },
            'body_html': ('<p>The story&nbsp;<span></span>body line 1<br>Line 2</p>'
                          '<p>abcdefghi abcdefghi abcdefghi abcdefghi abcdefghi'
                          '<span> abcdefghi</span> abcdefghi abcdefghi more</p>'
                          '<table><tr><td>test</td></tr></table>')
        }

        body_text = ('The story body line 1 Line 2\r\n\r\n'
                     'abcdefghi abcdefghi abcdefghi abcdefghi abcdefghi'
                     ' abcdefghi abcdefghi abcdefghi more\r\n\r\n'
                     'test\r\n\r\n')

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['body_text'], body_text)
        self.assertEqual(test_article['abstract'], 'abstract')
        self.assertEqual(test_article['headline'], 'This is a test headline')
        self.assertEqual(test_article['slugline'], 'Legal: slugline')

    def test_strip_html_case1(self):
        article = {
            config.ID_FIELD: '123',
            config.VERSION: 2,
            'source': 'AAP',
            'headline': 'This is a test headline',
            'type': 'text',
            'body_html': ('<p>The story body line 1<br>Line 2</p>'
                          '<p>abcdefghi abcdefghi abcdefghi abcdefghi abcdefghi'
                          '<span> abcdefghi</span> abcdefghi abcdefghi more</p>'
                          '<table><tr><td>test</td></tr></table>')
        }

        body_text = ('The story body line 1 Line 2\r\n\r\n'
                     'abcdefghi abcdefghi abcdefghi abcdefghi abcdefghi'
                     ' abcdefghi abcdefghi abcdefghi more\r\n\r\n'
                     'test\r\n\r\n')

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['body_text'], body_text)

    def test_strip_html_case2(self):
        article = {
            config.ID_FIELD: '123',
            config.VERSION: 2,
            'source': 'AAP',
            'headline': 'This is a test headline',
            'type': 'text',
            'body_html': ('<p>This is third<br/> take.</p><br/><p>Correction in the third take.</p><br/>'
                          '<p>This is test.</p><br/><p><br/></p>')
        }

        body_text = ('This is third take.\r\n\r\n'
                     'Correction in the third take.\r\n\r\n'
                     'This is test.\r\n\r\n')

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['body_text'], body_text)

    def test_strip_html_with_linebreak(self):
        article = {
            config.ID_FIELD: '123',
            config.VERSION: 2,
            'source': 'AAP',
            'headline': 'This is a test headline',
            'type': 'text',
            'body_html': ('<p>This is \nthird<br> take.</p><br/><p>Correction\nin the third take.</p><br/>'
                          '<p>This is test.</p><br/><p><br/></p>')
        }

        body_text = ('This is third take.\r\n\r\n'
                     'Correction in the third take.\r\n\r\n'
                     'This is test.\r\n\r\n')

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['body_text'], body_text)

    def test_locator(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 's'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'preformatted',
            'body_html': 'The story body',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'place': [{'qcode': 'VIC', 'name': 'VIC'}]
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['headline'], 'This is a test headline')
        self.assertEqual(test_article['place'][0]['qcode'], 'CRIK')
        article['anpa_category'] = [{'qcode': 'a'}]
        article['place'] = [{'qcode': 'VIC', 'name': 'VIC'}]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['headline'], 'This is a test headline')
        self.assertEqual(test_article['place'][0]['qcode'], 'VIC')

    def test_body_footer(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 's'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'preserved',
            'body_html': 'The story body',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'body_footer': 'call helpline 999 if you are planning to quit smoking'
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)

        formatted_article = json.loads(item.get('data'))
        self.assertEqual(formatted_article['body_text'],
                         'The story body\r\ncall helpline 999 if you are planning to quit smoking')

    def test_strip_html_mixed_tags(self):
        html = '<div>This is mixed&nbsp;<span style=\\\"background-color: transparent;\\\">content' \
               ' <p>this is para1</p></div>' \
               '<p>This is&nbsp;&nbsp;&nbsp;mixed content<div> this is para2</div></p>'
        formatted_content = self._formatter.get_text_content(html)

        body_text = ('This is mixed content this is para1\r\n\r\n'
                     'This is mixed content this is para2\r\n\r\n')

        self.assertEqual(formatted_content, body_text)

    def test_takes_package(self):
        html = ('<p>Para1: A tropical cyclone is a rapidly rotating storm system</p>'
                '<p>Para2: Tropical refers to the geographical origin of these systems</p>'
                '<br>'
                '<p>Para3:Tropical refers to the geographical origin of these systems</p>'
                '<br>'
                '<p>Para4:Tropical refers to the geographical origin of these systems</p>')
        formatted_content = self._formatter.get_text_content(html)

        body_text = ('Para1: A tropical cyclone is a rapidly rotating storm system\r\n\r\n'
                     'Para2: Tropical refers to the geographical origin of these systems\r\n\r\n'
                     'Para3:Tropical refers to the geographical origin of these systems\r\n\r\n'
                     'Para4:Tropical refers to the geographical origin of these systems\r\n\r\n')

        self.assertEqual(formatted_content, body_text)

    def test_null_abstract_byline_key(self):
        article = {
            config.ID_FIELD: '123',
            config.VERSION: 2,
            'source': 'AAP',
            'headline': 'This is a test headline',
            'type': 'text',
            'anpa_take_key': None,
            'byline': None,
            'abstract': None,
            'body_html': ('<p>Hi</p>')
        }
        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['byline'], '')
        self.assertEqual(test_article['abstract'], '')

    def test_new_zealand_content_with_source_not_NZN(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 's'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'preserved',
            'body_html': 'The story body',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[1][config.ID_FIELD]
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['source'], 'NZN')

    def test_new_zealand_content_with_source_NZN(self):
        article = {
            'source': 'NZN',
            'anpa_category': [{'qcode': 's'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'preserved',
            'body_html': 'The story body',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[1][config.ID_FIELD]
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['source'], 'NZN')

    def test_AAP_content_from_Sports_Desk(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 's'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'preserved',
            'body_html': 'The story body',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[0][config.ID_FIELD]
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['source'], 'AAP')

    def test_NZN_content_from_Sports_Desk(self):
        article = {
            'source': 'NZN',
            'anpa_category': [{'qcode': 's'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'preserved',
            'body_html': 'The story body',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[0][config.ID_FIELD]
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['source'], 'NZN')

    def test_multiple_categories_ignore_features(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 'c'}, {'qcode': 's'}, {'qcode': 'a'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'HTML',
            'body_html': 'The story body',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[0][config.ID_FIELD]
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['source'], 'AAP')
        self.assertEqual(test_article['first_category']['qcode'], 's')
        self.assertEqual(len(test_article['anpa_category']), 2)
        self.assertEqual(test_article['anpa_category'][0]['qcode'], 's')
        self.assertEqual(test_article['anpa_category'][1]['qcode'], 'a')

    def test_single_category_allow_features(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 'c'}],
            'headline': 'This is a test headline',
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'HTML',
            'body_html': 'The story body',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[0][config.ID_FIELD]
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['source'], 'AAP')
        self.assertEqual(test_article['first_category']['qcode'], 'c')
        self.assertEqual(len(test_article['anpa_category']), 1)
        self.assertEqual(test_article['anpa_category'][0]['qcode'], 'c')

    def test_auto_publish_with_abstract(self):
        article = {
            'source': 'AP',
            'anpa_category': [{'qcode': 'c'}],
            'headline': 'This is a test headline',
            'abstract': 'This is a test abstract',
            'auto_publish': True,
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'HTML',
            'body_html': 'The story body',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[0][config.ID_FIELD]
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['source'], 'AP')
        self.assertEqual(test_article['abstract'], 'This is a test abstract')

    def test_auto_publish_without_abstract_ap_content(self):
        article = {
            'source': 'AP',
            'anpa_category': [{'qcode': 'c'}],
            'headline': 'This is a test headline',
            'auto_publish': True,
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'HTML',
            'body_html': '<p>Sydney (AP) - The story body text.</p><p>This is second paragraph</p>',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[0][config.ID_FIELD]
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['source'], 'AP')
        self.assertEqual(test_article['abstract'], 'The story body text.')
        self.assertEqual(test_article['body_text'], 'The story body text.\r\n\r\nThis is second paragraph')

    def test_auto_publish_without_abstract_Reuters_content(self):
        article = {
            'source': 'Reuters',
            'anpa_category': [{'qcode': 'c'}],
            'headline': 'This is a test headline',
            'auto_publish': True,
            'slugline': '123456789012345678901234567890',
            'byline': 'joe',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'HTML',
            'body_html': 'Sydney (Reuters) - The story body text.',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[0][config.ID_FIELD]
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['source'], 'Reuters')
        self.assertEqual(test_article['abstract'], 'The story body text.')
        self.assertEqual(test_article['slugline'], '123456789012345678901234567890')
        self.assertEqual(test_article['body_text'], 'The story body text.')

    def test_auto_publish_without_abstract_other_source(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 'c'}],
            'headline': 'This is a test headline',
            'auto_publish': True,
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'HTML',
            'body_html': 'Sydney, AAP - The story body text.',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[0][config.ID_FIELD]
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['source'], 'AAP')
        self.assertEqual(test_article['abstract'], 'This is a test headline')
        self.assertEqual(test_article['slugline'], 'slugline')
        self.assertEqual(test_article['body_text'], 'Sydney, AAP - The story body text.')

    def test_associated_item(self):
        article = {
            'source': 'AAP',
            'anpa_category': [{'qcode': 'c'}],
            'headline': 'This is a test headline',
            'auto_publish': True,
            'byline': 'joe',
            'slugline': 'slugline',
            'subject': [{'qcode': '15017000'}],
            'anpa_take_key': 'take_key',
            'unique_id': '1',
            'type': 'text',
            'format': 'HTML',
            'body_html': 'Sydney, AAP - The story body text.',
            'word_count': '1',
            'priority': '1',
            'firstcreated': utcnow(),
            'versioncreated': utcnow(),
            'lock_user': ObjectId(),
            'task': {
                'desk': self.desks[0][config.ID_FIELD]
            },
            'associations': {
                'featuremedia': {
                    'type': 'picture',
                    'description_text': '<div>Hello&nbsp;world</div>',
                    'headline': '<div>Hello&nbsp;world</div>',
                    'alt_text': '<div>Hello&nbsp;world</div>',
                    'byline': '<div>Hello&nbsp;world</div>',
                    'slugline': '<div>Hello&nbsp;world</div>'
                }
            }
        }

        subscriber = self.app.data.find('subscribers', None, None)[0]
        seq, item = self._formatter.format(article, subscriber)[0]
        item = json.loads(item)
        self.assertGreater(int(seq), 0)
        test_article = json.loads(item.get('data'))
        self.assertEqual(test_article['associations']['featuremedia']['description_text'], 'Hello world')
        self.assertEqual(test_article['associations']['featuremedia']['headline'], 'Hello world')
        self.assertEqual(test_article['associations']['featuremedia']['alt_text'], 'Hello world')
        self.assertEqual(test_article['associations']['featuremedia']['slugline'], 'Hello world')
        self.assertEqual(test_article['associations']['featuremedia']['byline'], 'Hello world')
