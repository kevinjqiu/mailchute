from nose.tools import eq_
from tests.base import BaseTestCase
from mailchute import db
from mailchute.smtpd.mailchute import MessageProcessor
from mailchute.model import IncomingEmail


class TestMessageProcessor(BaseTestCase):
    def setup(self):
        self.message_processor = MessageProcessor()

    def test_process_message_single_recipient(self):
        self.message_processor(
            'PEER', 'johndoe@example.com', ['janesmith@test.com'],
            data='DATA')
        emails = db.session.query(IncomingEmail).all()
        eq_(1, len(emails))
        eq_(emails[0].recipient, 'janesmith@test.com')
        eq_(emails[0].sender, 'johndoe@example.com')
        eq_(emails[0].raw_message.message, 'DATA')

    def test_process_message_multi_recipient(self):
        self.message_processor(
            'PEER', 'johndoe@example.com',
            ['janesmith@test.com', 'bluemarsh@test.com'],
            data='DATA')
        emails = db.session.query(IncomingEmail).all()
        eq_(2, len(emails))
        eq_(emails[0].recipient, 'janesmith@test.com')
        eq_(emails[0].sender, 'johndoe@example.com')
        eq_(emails[0].raw_message.message, 'DATA')
        eq_(emails[1].recipient, 'bluemarsh@test.com')
        eq_(emails[1].sender, 'johndoe@example.com')
        eq_(emails[1].raw_message.message, 'DATA')
