import asyncore

from mailchute.mailchute import MailChuteSMTPServer


def main():
    MailChuteSMTPServer(('0.0.0.0', 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
