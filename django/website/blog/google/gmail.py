import base64
from email.message import EmailMessage
import os
from typing import List

from blog.models import Lead, LeadImage
from .auth import get_auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class EmailService():
    def __init__(self):
        self.service = build('gmail', 'v1', credentials=get_auth())
        self.eto = str(os.environ.get('ETO_EMAIL'))

    def lead_notification(self, lead: Lead, lead_images: List[LeadImage]):
        try:
            message = EmailMessage()
            message_content = f'''
            <html>
                <body>
                    <p>Nombre: {lead.first_name} {lead.last_name}</p>
                    <p>Numero de Telefono: <a href="tel:{lead.phone_number}">{lead.phone_number}</a></p>
                    <p>Fecha: {lead.date_created.strftime("%B,%d %Y - %I:%M %p")}</p>
                    <p>Servicio: {lead.service.name}</p>
                    <p>Ciudad: {lead.location.name}</p>
                    <p>Mensaje del Cliente:</p>
                    <p>{lead.message}</p>
                '''

            # Check if latitude and longitude are greater than 0
            if lead.latitude is not None and lead.longitude is not None:
                message_content += f'''
            Localizacion exacta: <a href="https://www.google.com/maps?q={lead.latitude},{lead.longitude}">Localizacion</a><br>
            '''
            if len(lead_images) > 0:
                message_content += f'''<h2>Imagenes:</h2>'''

            for img in lead_images:
                message_content += f'''<img src="https://{os.environ.get('AWS_S3_CUSTOM_DOMAIN')}/images/{img.src}" />'''
                
            message_content += '''
                </body>
            </html>
            '''

            message.set_content(message_content, subtype='html')

            message['To'] = self.eto
            message['From'] = self.eto
            message['Subject'] = f"Pedido de {lead.service.name} - {lead.location.name}"

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {
                'raw': encoded_message
            }

            (self.service.users().messages().send(userId="me", body=create_message).execute())

        except Exception as e:
            raise Exception(F'An error occurred: {e}')

    def send_mail(self, contact_form):
        try:
            message = EmailMessage()

            message.set_content(f'''
            Nombre: {contact_form['first_name']} {contact_form['last_name']}
            \n
            Mensaje:
            \n
            {contact_form['message']}
            \n
            ''')

            message['To'] = self.eto
            message['From'] = contact_form['email']
            message['Subject'] = "Mensaje De Contacto"

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {
                'raw': encoded_message
            }

            (self.service.users().messages().send
                            (userId="me", body=create_message).execute())

        except Exception as e:
            raise Exception(F'An error occurred: {e}')