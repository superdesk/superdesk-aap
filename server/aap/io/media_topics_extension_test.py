
from unittests import TestCase
from aap.io.media_topics_extension import init_app


class TopicTest(TestCase):
    def test_all_subjects_map_to_a_media_topic(self):
        init_app(self.app)
        for (k, _v) in sorted(self.app.subjects.subjects.items()):
            topic = self.app.mediatopics.get_media_topic(k)
            # topics codes starting from 99 are AAP specific
            if not k.startswith('99'):
                self.assertIsNotNone(topic)
                # print(k, v, '\t---->\t',topic,
                # self.app.mediatopics.get_media_topic_item(topic).get('prefLabel').get('en-GB'))
            else:
                self.assertINone(topic)

    def test_get_items(self):
        init_app(self.app)
        items = self.app.mediatopics.get_items()
        for i in items:
            subject = self.app.mediatopics.get_subject_code(i.get('qcode'))
            self.assertIsNotNone(subject)
            # print(i.get('qcode'), i.get('name'), '\t---->\t', subject, self.app.subjects.subjects.get(subject))

    def test_get_media_topics(self):
        init_app(self.app)
        items = self.app.mediatopics.get_media_topics()
        for i in items.keys():
            subject = self.app.mediatopics.get_subject_code(i)
            self.assertIsNotNone(subject)
            # print(i, v.get('prefLabel').get('en-GB'), '\t---->\t', subject, self.app.subjects.subjects.get(subject))

    def test_media_topic_to_subject(self):
        init_app(self.app)
        subject = self.app.mediatopics.get_subject_code('medtop:20000070')
        self.assertEqual(subject, '16004000')

    def test_subject_to_media_topic(self):
        # The standard mapping maps hip hop to music
        topic = self.app.mediatopics.get_media_topic('01011007')
        self.assertEqual(topic, 'medtop:20000018')
        init_app(self.app)
        # AAP overrides to it to point to hip hop to hip hop
        topic = self.app.mediatopics.get_media_topic('01011007')
        self.assertEqual(topic, 'medtop:20001184')

    def test_get_media_topic_item(self):
        init_app(self.app)
        topic = self.app.mediatopics.get_media_topic_item('medtop:20000070')
        self.assertEqual(topic['type'], ['http://www.w3.org/2004/02/skos/core#Concept'])
