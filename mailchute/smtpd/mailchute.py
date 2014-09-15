import datetime
import smtpd
from email.parser import Parser
from mailchute import db
from mailchute import settings
from mailchute.model import RawMessage, IncomingEmail
from logbook import Logger


logger = Logger(__name__)


class MessageProcessor(object):
    def _should_persist(self, recipient):
        recipient_domain = recipient.split('@')[1].lower()
        allowed_receiver_domains = settings.RECEIVER_DOMAIN
        if allowed_receiver_domains:
            allowed_receiver_domains = allowed_receiver_domains.split(',')
        return (allowed_receiver_domains is None
                or recipient_domain in allowed_receiver_domains)

    def __call__(self, peer, mailfrom, recipients, data):
        try:
            mailfrom = mailfrom.lower()
            recipients = list(map(str.lower, recipients))

            logger.info(
                "Incoming message from {0} to {1}".format(mailfrom, recipients))

            email = Parser().parsestr(data)

            raw_message = RawMessage(message=data)

            for recipient in recipients:
                if self._should_persist(recipient):
                    incoming_email = IncomingEmail(
                        sender=mailfrom, recipient=recipient,
                        raw_message=raw_message,
                        subject=email['subject'],
                        created_at=datetime.datetime.now(),
                    )
                    db.session.add(incoming_email)
                else:
                    logger.info('{} is not an allowed recipient. Skip.'.format(
                        recipient))

            db.session.commit()
            logger.info("Message saved")
        except Exception as e:  # pragma: no cover
            logger.exception(e)
            db.session.rollback()


class MailchuteSMTPServer(smtpd.SMTPServer):
    process_message = MessageProcessor()
