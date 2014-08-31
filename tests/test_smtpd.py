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
        assert 1 == len(emails)
        assert emails[0].recipient == 'janesmith@test.com'
        assert emails[0].sender == 'johndoe@example.com'
        assert emails[0].raw_message.message == 'DATA'

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
