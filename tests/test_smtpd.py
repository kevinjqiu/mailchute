from tests.base import BaseTestCase, Fixture
from mailchute import db
from mailchute.smtpd.mailchute import MessageProcessor
from mailchute.model import IncomingEmail
from unittest.mock import patch


class TestMessageProcessor(BaseTestCase):
    def setup(self):
        self.message_processor = MessageProcessor()

    def test_process_message_single_recipient(self):
        self.message_processor(
            'PEER', 'johndoe@example.com', ['janesmith@test.com'],
            data='DATA')
        emails = db.session.query(IncomingEmail).all()
        assert 1 == len(emails)
        assert emails[0].recipient == 'janesmith@test.com'
        assert emails[0].sender == 'johndoe@example.com'
        assert emails[0].raw_message.message == 'DATA'
        assert emails[0].subject is None

    def test_process_message_multi_recipient(self):
        self.message_processor(
            'PEER', 'johndoe@example.com',
            ['janesmith@test.com', 'bluemarsh@test.com'],
            data='DATA')
        emails = db.session.query(IncomingEmail).all()
        assert 2, len(emails)
        assert emails[0].recipient == 'janesmith@test.com'
        assert emails[0].sender == 'johndoe@example.com'
        assert emails[0].raw_message.message == 'DATA'
        assert emails[1].recipient == 'bluemarsh@test.com'
        assert emails[1].sender == 'johndoe@example.com'
        assert emails[1].raw_message.message == 'DATA'

    def test_process_message_with_subject(self):
        self.message_processor(
            'PEER',
            'johndoe@example.com',
            ['janesmith@test.com'],
            Fixture.INCOMING_EMAIL,
        )
        emails = db.session.query(IncomingEmail).all()
        assert 1 == len(emails)
        assert 'another test' == emails[0].subject

    @patch('mailchute.smtpd.mailchute.settings')
    def test_process_message_recipient_wrong_domain(self, settings):
        settings.RECEIVER_DOMAIN = 'receiver.com'
        self.message_processor(
            'PEER',
            'johndoe@example.com',
            ['janesmith@test.com'],
            'DATA',
        )
        emails = db.session.query(IncomingEmail).all()
        assert 0 == len(emails)

    @patch('mailchute.smtpd.mailchute.settings')
    def test_process_message_no_check_recipient_domain(self, settings):
        settings.RECEIVER_DOMAIN = None
        self.message_processor(
            'PEER',
            'johndoe@example.com',
            ['janesmith@test.com'],
            'DATA',
        )
        emails = db.session.query(IncomingEmail).all()
        assert 1 == len(emails)
