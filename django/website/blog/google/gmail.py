from __future__ import print_function
import base64
from datetime import datetime
from email.message import EmailMessage
import os
from .auth import get_auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def send_mail(contact_form):
    try:
        credentials = get_auth()
        service = build('gmail', 'v1', credentials=credentials)

        message = EmailMessage()

        message.set_content(f'''
        Nombre: {contact_form['first_name']} {contact_form['last_name']}
        \n
        Mensage:
        \n
        {contact_form['message']}
        \n
        ''')

        eto = str(os.environ.get('ETO_EMAIL'))

        message['To'] = eto
        message['From'] = contact_form['email']
        message['Subject'] = "Mensaje De Contacto"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        (service.users().messages().send
                        (userId="me", body=create_message).execute())

    except Exception as e:
        raise Exception(F'An error occurred: {e}')