from tests.base import BaseTestCase, Fixture
from mailchute import db
from mailchute.smtpd.mailchute import MessageProcessor
from mailchute.smtpd.cli import main as smtpd_main
from mailchute.model import IncomingEmail
from unittest.mock import patch, call


class TestSMTPDCli(object):
    @patch('mailchute.smtpd.cli.settings')
    @patch('mailchute.smtpd.cli.MailchuteSMTPServer')
    @patch('mailchute.smtpd.cli.asyncore')
    def test_smtpd_is_served_at_the_expected_addresses(
            self, asyncore, smtp_server_class, settings):
        settings.SMTPD = {
            'host': 'host',
            'port': 'port',
        }
        asyncore.loop.side_effect = KeyboardInterrupt
        smtpd_main()
        assert [call(('host', 'port'), None)] == \
            smtp_server_class.call_args_list


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
