import asyncore

from mailchute.smtpd.mailchute import MailchuteSMTPServer
from mailchute import settings
from logbook import Logger


logger = Logger(__name__)


def main():
    address, port = settings.SMTPD['host'], settings.SMTPD['port']

    MailchuteSMTPServer((address, port), None)
    logger.info(
        "Mailchute server started listening at {0}:{1}".format(address, port))
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        logger.info("Exiting...")
