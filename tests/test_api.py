from webtest import TestApp
from tests.base import BaseTestCase

from mailchute.api.resource import app


class ApiTestCase(BaseTestCase):
    def setup(self):
        self.app = TestApp(app)


class TestGetInbox(ApiTestCase):
    def test_no_incoming_email_for_inbox(self):
        response = self.app.get('/inbox/foo@bar.com/')
        assert '200 OK' == response.status
        expected = {
            'inboxes': [{
                'emails': [],
                'id': 'foo@bar.com',
                'name': 'foo@bar.com',
                'num_of_emails': 0
            }]}
        assert expected == response.json

    def test_with_incoming_email(self):
        self.create_incoming_email(
            sender='foobar@example.com',
            recipient='foo@bar.com',
            raw_message='RAW')
        response = self.app.get('/inbox/foo@bar.com/')

        assert '200 OK' == response.status
        assert 1 == len(response.json['inboxes'])
        assert 'foo@bar.com' == response.json['inboxes'][0]['id']
        assert 'foo@bar.com' == response.json['inboxes'][0]['name']
        assert 1 == len(response.json['inboxes'][0]['emails'])
        assert response.json['inboxes'][0]['emails'][0]['recipient'] == \
            'foo@bar.com'
        assert response.json['inboxes'][0]['emails'][0]['sender'] == \
            'foobar@example.com'


class TestGetRawMessage(ApiTestCase):
    def test_message_not_found(self):
        response = self.app.get(
            '/inbox/foo@bar.com/raw_message/0ab55e', status=404)
        assert {'error': {'message': 'Resource Not Found'}} == \
            response.json

    def test_message_found(self):
        email = self.create_incoming_email(
            sender='foobar@example.com',
            recipient='foo@bar.com',
            raw_message='RAW')

        response = self.app.get('/inbox/foo@bar.com/raw_message/{0}'.format(
            email.raw_message_id))

        assert 1 == len(response.json['raw_messages'])
        assert 'RAW' == response.json['raw_messages'][0]['message']
