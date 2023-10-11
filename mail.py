from email.mime.text import MIMEText

import base64
import os.path
import smtplib

from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from params import Params

# If modifying these scopes, delete the file token.json.
SCOPES = Params.get('mail_scopes')

# user token storage
USER_TOKENS = Params.get('token_filename')

# application credentials
CREDENTIALS = Params.get('creds_filename')


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

    def send(self):
        msg = MIMEText(self.message_body)
        msg['Subject'] = self.subject
        msg['From'] = self.username
        msg['To'] = ', '.join(self.recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.username, self.password)
            smtp_server.sendmail(self.username, self.recipients, msg.as_string())
        print("Message sent!")

    def get_token(self) -> str:
        creds = None

        if os.path.exists(USER_TOKENS):
            creds = Credentials.from_authorized_user_file(USER_TOKENS, SCOPES)
        creds.refresh(Request())
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(USER_TOKENS, 'w') as token:
                token.write(creds.to_json())
        return creds.token

    def generate_oauth2_string(self) -> str:
        auth_string = 'user=' + self.username + '\1auth=Bearer ' + self.access_token + '\1\1'
        return base64.b64encode(auth_string.encode('ascii')).decode('ascii')

    def send_email(self):
        self.access_token = self.get_token()
        auth_string = self.generate_oauth2_string()

        msg = MIMEText(self.message_body)
        msg['Subject'] = self.subject
        msg['From'] = self.username
        msg['To'] = ', '.join(self.recipients)

        server = smtplib.SMTP(self.host, self.port)
        server.starttls()
        server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
        server.sendmail(self.username, self.recipients,  msg.as_string())
        server.quit()
