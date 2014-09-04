from webtest import TestApp
from tests.base import BaseTestCase

from mailchute.api.resource import app


class ApiTestCase(BaseTestCase):
    def setup(self):
        self.app = TestApp(app)


class TestGetEmail(ApiTestCase):
    def test_mandatory_inbox_filter(self):
        self.app.get('/emails', status=400)

    def test_no_incoming_email_for_inbox(self):
        response = self.app.get('/emails?inbox=foo@bar.com')
        assert '200 OK' == response.status
        expected = {
            'emails': []
        }
        assert expected == response.json

    def test_with_incoming_email(self):
        self.create_incoming_email(
            sender='foobar@example.com',
            recipient='foo@bar.com',
            raw_message='RAW',
            subject='subject',
        )
        self.create_incoming_email(
            sender='foobar@example.com',
            recipient='foo-test@bar.com',
            raw_message='RAW',
            subject='subject',
        )
        response = self.app.get('/emails?inbox=foo@bar.com')

        assert '200 OK' == response.status
        response_json = dict(response.json)
        response_json['emails'][0]['created_at'] = '$TIME'
        response_json['emails'][0]['raw_message_id'] = '$ID'

        expected = {
            'emails': [{
                'created_at': '$TIME',
                'raw_message_id': '$ID',
                'subject': 'subject',
                'recipient':
                'foo@bar.com',
                'id': 1,
                'sender': 'foobar@example.com'
            }],
        }
        assert expected == response_json


class TestGetRawMessage(ApiTestCase):
    def test_message_not_found(self):
        response = self.app.get(
            '/raw_messages/0ab55e', status=404)
        assert {'error': {'message': 'Resource Not Found'}} == \
            response.json

    def test_message_found(self):
        email = self.create_incoming_email(
            sender='foobar@example.com',
            recipient='foo@bar.com',
            raw_message='RAW')

        response = self.app.get('/raw_messages/{0}'.format(
            email.raw_message_id))
        response_json = dict(response.json)
        response_json['raw_messages'][0]['id'] = '$ID'

        expected = {
            'raw_messages': [{
                'message': 'RAW',
                'id': '$ID',
            }]
        }

        assert '200 OK' == response.status
        assert expected == response_json
