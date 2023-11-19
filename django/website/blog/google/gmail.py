from __future__ import print_function
import base64
from datetime import datetime
from email.message import EmailMessage
import os
import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def send_mail():
    try:
        credentials = auth.get_auth()
        service = build('gmail', 'v1', credentials=credentials)

        message = EmailMessage()

        message.set_content(f'''
        The sheet has been updated on {datetime.today().strftime('%m/%d/%Y')}
        \n
        Click the linkerino: {str(os.environ.get('SPREADSHEET_LINK'))}
        ''')

        user_one = str(os.environ.get('EMAIL_ONE'))
        user_two = str(os.environ.get('EMAIL_TWO'))

        message['To'] = user_two + ", " + user_one
        message['From'] = str(os.environ.get('EMAIL_TWO'))
        message['Subject'] = "YUH YUH"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        (service.users().messages().send
                        (userId="me", body=create_message).execute())

    except HttpError as error:
        print(F'An error occurred: {error}')