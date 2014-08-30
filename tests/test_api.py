import pytest
import webtest

from webtest import TestApp
from tests.base import BaseTestCase
from nose.tools import eq_

from mailchute import db
from mailchute.api.resource import app


class ApiTestCase(BaseTestCase):
    def setup(self):
        self.app = TestApp(app)


class TestGetIncomingEmail(ApiTestCase):
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

        eq_('200 OK', response.status)
        eq_(1, len(response.json['incoming_emails']))
        eq_(response.json['incoming_emails'][0]['recipient'],
            'foo@bar.com')
        eq_(response.json['incoming_emails'][0]['sender'],
            'foobar@example.com')


class TestGetRawMessage(ApiTestCase):
    def test_message_not_found(self):
        response = self.app.get(
            '/inbox/foo@bar.com/raw_message/0ab55e', status=404)
        eq_({'error': {'message': 'Resource Not Found'}},
            response.json)

    def test_message_found(self):
        email = self.create_incoming_email(
            sender='foobar@example.com',
            recipient='foo@bar.com',
            raw_message='RAW')

        response = self.app.get('/inbox/foo@bar.com/raw_message/{0}'.format(
            email.raw_message_id))

        eq_(1, len(response.json['raw_messages']))
        eq_('RAW', response.json['raw_messages'][0]['message'])
