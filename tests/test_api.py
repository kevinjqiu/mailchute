from webtest import TestApp
from tests.base import BaseTestCase
from nose.tools import eq_

from mailchute import db
from mailchute.api.resource import app


class TestGetIncomingEmail(BaseTestCase):
    def setup(self):
        self.app = TestApp(app)

    def test_no_incoming_email_for_inbox(self):
        response = self.app.get('/inbox/foo@bar.com/')
        eq_('200 OK', response.status)
        eq_({'incoming_emails': []}, response.json)

    def test_with_incoming_email(self):
        self.create_incoming_email(
            sender='foobar@example.com',
            recipient='foo@bar.com',
            raw_message='RAW')
        response = self.app.get('/inbox/foo@bar.com/')

        response.json['incoming_emails'][0]['created_at'] = '$NOW'
        response.json['incoming_emails'][0]['raw_message_id'] = '$UUID'

        eq_('200 OK', response.status)
        eq_(1, len(response.json['incoming_emails']))
        eq_(response.json['incoming_emails'][0]['recipient'],
            'foo@bar.com')
        eq_(response.json['incoming_emails'][0]['sender'],
            'foobar@example.com')
