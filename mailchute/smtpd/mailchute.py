import smtpd
from email.parser import Parser
from mailchute import db
from mailchute.model import RawMessage, IncomingEmail
from logbook import Logger


logger = Logger(__name__)


class MailChuteSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, recipients, data):
        mailfrom = mailfrom.lower()
        recipients = map(str.lower, recipients)

        logger.info(
            "Incoming message from {0} to {1}".format(mailfrom, recipients))

        message = Parser().parsestr(data)

        raw_message = RawMessage(message=data)

        for recipient in recipients:
            incoming_email = IncomingEmail(
                sender=mailfrom, recipient=recipient,
                raw_message=raw_message)
            db.session.add(incoming_email)

        db.session.commit()
        logger.info("Message saved")
