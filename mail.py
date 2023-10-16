from params import Params
import smtplib
import ssl


class Email:

    def __init__(self, message_body):

        self.host = Params.get('mail_host')
        self.port = Params.get('mail_port')
        self.subject = Params.get('mail_subject')
        self.username = Params.get('mail_username')
        self.password = Params.get('mail_password')
        self.recipients = Params.get('mail_recipients')
        self.message_body = message_body
        self.access_token = ''

    def send_email(self):
        context = ssl.create_default_context()
        with smtplib.SMTP(self.host, self.port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.username, self.password)
            server.sendmail(self.username, self.recipients, self.message_body)
