import smtpd
from email.parser import Parser
from mailchute import db
from mailchute.model import IncomingEmailModel


class MailChuteSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, recipients, data):
        message = Parser().parsestr(data)

        incoming_email = IncomingEmailModel(
            created_at=None, sender=mailfrom, raw_message=data)
        db.session.add(incoming_email)
        db.session.commit()
