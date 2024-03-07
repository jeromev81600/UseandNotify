from flask import Flask
from flask_mail import Mail, Message
from twilio.rest import Client
from bs4 import BeautifulSoup
import imaplib
import email
import os
from config.config import *

# Initialisation de l'extension Flask-Mail avec l'application Flask
mail = Mail()


def init_app(app):
    mail.init_app(app)


# Configuration des informations d'identification Twilio
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
twilio_phone_number = TWILIO_PHONE_NUMBER

# Configuration boite e-mail pour utilisation avec imap
IMAP_SERVER = MY_EMAIL_IMAP_SERVER
EMAIL = MY_EMAIL
PASSWORD = MY_PASSWORD

# Initialisation du client Twilio
client = Client(account_sid, auth_token)

# Vérifier et créer le répertoire "uploads" s'il n'existe pas
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Fonction pour envoyer un e-mail avec une pièce jointe
def send_email_with_attachment(app, to, subject, body, file_path):
    with app.app_context():
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
        msg.body = body
        if file_path is not None:
            with app.open_resource(file_path) as attachment:
                msg.attach(filename=file_path, content_type='application/octet-stream', data=attachment.read())
        mail.send(msg)


# Fonction pour envoyer un SMS
def send_sms(recipient, message):
    sms = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=recipient
    )


# Fonction pour récupérer les emails via le serveur IMAP
def fetch_emails():
    try:
        # Connexion au serveur IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)

        # Sélection de la boîte de réception
        mail.select('inbox')

        # Recherche des e-mails
        result, data = mail.search(None, 'ALL')

        email_contents = []
        email_titles = []

        # Récupération des e-mails
        # Trie des e-mails par ordre décroissant et limite à 5 e-mails
        emails_nums = list(reversed(data[0].split()))[:5]
        for num in emails_nums:
            result, message_data = mail.fetch(num, '(RFC822)')
            raw_email = message_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Vérification si l'e-mail est au format multipart
            if msg.is_multipart():
                for part in msg.walk():
                    # Si le contenu est en texte/html
                    if part.get_content_type() == 'text/html':
                        email_content = part.get_payload(decode=True).decode('utf-8')
                        email_contents.append(email_content)

                        # Utiliser BeautifulSoup pour extraire le titre de l'e-mail
                        soup = BeautifulSoup(email_content, 'html.parser')
                        title_tag = soup.find('title')
                        if title_tag:
                            email_titles.append(title_tag.text)

        # Fermeture de la connexion
        mail.logout()

        return email_contents, email_titles
    except Exception as e:
        print(f"Erreur lors de la récupération des e-mails : {e}")
        return [], []
