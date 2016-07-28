from superdesk.emails import send_user_status_changed_email, send_activity_emails, send_email, \
    send_article_killed_email
from test_factory import SuperdeskTestCase
from unittest.mock import patch
from superdesk.utc import utcnow


class SendEmailTestCase(SuperdeskTestCase):

    def test_send_email(self):
        with self.app.app_context():
            with self.app.mail.record_messages() as outbox:
                assert len(outbox) == 0
                send_user_status_changed_email(['test@sd.io'], 'created')
                assert len(outbox) == 1
                assert outbox[0].subject == 'Your Superdesk account is created'

    def test_send_activity_emails_error(self):
        recipients = ['foo', 'bar']
        activities = [
            {'message': 'error', 'data': {'foo': 1}},
            {'message': 'error', 'data': {'bar': 1}},
        ]
        with patch.object(send_email, 'delay', return_value=None) as sent:
            with self.app.app_context():
                send_activity_emails(activities[0], recipients)
                self.assertEqual(1, sent.call_count)
                send_activity_emails(activities[0], recipients)
                self.assertEqual(1, sent.call_count)
                send_activity_emails(activities[1], recipients)
                self.assertEqual(2, sent.call_count)
                send_activity_emails(activities[1], recipients)
                self.assertEqual(2, sent.call_count)

    def test_send_email_kill_for_NZN(self):
        with self.app.app_context():
            with self.app.mail.record_messages() as outbox:
                assert len(outbox) == 0
                article = {
                    'headline': 'headline',
                    'place': [{'qcode': 'NSW', 'name': 'NSW'}],
                    'slugline': 'slugline',
                    'dateline': {
                        'located': {
                            'city': 'Test, Test'
                        },
                        'text': 'Test, Test, July 9 AAP -'
                    },
                    'body_html': 'body',
                    'desk_name': 'New Zealand',
                    'city': 'Test, Test'
                }
                send_article_killed_email(article, ['test@sd.io'], utcnow())
                self.assertEqual(len(outbox), 1)
                self.assertEqual(outbox[0].subject, 'Transmission from circuit: E_KILL_')
                self.assertIn('body', outbox[0].body)

    def test_send_email_kill_for_AAP(self):
        with self.app.app_context():
            with self.app.mail.record_messages() as outbox:
                assert len(outbox) == 0
                article = {
                    'headline': 'headline',
                    'place': [{'qcode': 'NSW', 'name': 'NSW'}],
                    'slugline': 'slugline',
                    'dateline': {
                        'located': {
                            'city': 'Test, Test'
                        },
                        'text': 'Test, Test, July 9 AAP -'
                    },
                    'body_html': 'body',
                    'desk_name': 'Sports',
                    'city': 'Test, Test'
                }
                send_article_killed_email(article, ['test@sd.io'], utcnow())
                self.assertEqual(len(outbox), 1)
                self.assertEqual(outbox[0].subject, 'Transmission from circuit: E_KILL_')
                self.assertIn('body', outbox[0].body)
