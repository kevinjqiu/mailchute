# -*- coding: utf-8 -*-
import smtpd
from email.parser import Parser


class MailChuteSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, recipients, data):
        message = Parser().parsestr(data)
