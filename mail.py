from params import Params
import smtplib
import ssl


class Email:
    """
    Class for sending email from gmail account
    Uses username and app password
    """
    def __init__(self, message_body):
        """
        Class constructor. Information except message_body is obtained from params.json file.
        Parameters:
            message_body (str) - Email message body
        """
        self.host = Params.get('mail_host')
        self.port = Params.get('mail_port')
        self.subject = Params.get('mail_subject')
        self.username = Params.get('mail_username')
        self.password = Params.get('mail_password')
        self.recipients = Params.get('mail_recipients')
        self.message_body = message_body
        self.access_token = ''

    def send_email(self):
        """
        Sends email
        """
        context = ssl.create_default_context()
        with smtplib.SMTP(self.host, self.port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.username, self.password)
            server.sendmail(self.username, self.recipients, self.message_body)
