import asyncore

from mailchute.mailchute import MailChuteSMTPServer
from logbook import Logger


logger = Logger(__name__)


def main():
    address, port = '0.0.0.0', 25

    MailChuteSMTPServer((address, port), None)
    logger.info(
        "Mailchute server started listening at {0}:{1}".format(address, port))
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        logger.info("Exiting...")
