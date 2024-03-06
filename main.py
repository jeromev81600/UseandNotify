from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from twilio.rest import Client
from bs4 import BeautifulSoup
import imaplib
import email
from config import *
import os

app = Flask(__name__)

# Configuration de Flask-Mail avec les paramètres SMTP
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL

# Configuration des informations d'identification Twilio
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
twilio_phone_number = TWILIO_PHONE_NUMBER

# Configuration boite e-mail pour utilisation avec imap
IMAP_SERVER = MY_EMAIL_IMAP_SERVER
EMAIL = MY_EMAIL
PASSWORD = MY_PASSWORD

# Liste des destinataires
recipients = RECIPIENTS

# Initialisation de l'extension Flask-Mail avec l'application Flask
mail = Mail(app)

# Initialisation du client Twilio
client = Client(account_sid, auth_token)

# Vérifier et créer le répertoire "uploads" s'il n'existe pas
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Fonction pour envoyer un e-mail avec une pièce jointe
def send_email_with_attachment(to, subject, body, file_path):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = body
    if file_path is not None:  # Vérifier si file_path n'est pas None
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
        # Trie des e-mails par ordre décroissant et limite à 4 e-mails
        emails_nums = list(reversed(data[0].split()))[:4]
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        to = request.form['to']
        subject = request.form['subject']
        body = request.form['bodyMessage']

        recipient_info = recipients.get(to)

        if recipient_info:
            if 'send_email' in request.form:
                file = request.files['file']
                if file:
                    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                    file.save(file_path)
                    send_email_with_attachment(recipient_info['email'], subject, body, file_path)
                else:
                    send_email_with_attachment(recipient_info['email'], subject, body, None)  # Utiliser None comme file_path
            elif 'send_sms' in request.form:
                send_sms(recipient_info['phone'], body)
        else:
            # Gérer le cas où le destinataire sélectionné n'existe pas
            pass
    emails_content, emails_titles = fetch_emails()
    return render_template('index.html', recipients=recipients,emails_titles=emails_titles,emails_content=emails_content)

@app.route('/emails/<int:email_id>')
def email_detail(email_id):
    emails_content, _ = fetch_emails()
    email_content = emails_content[email_id]
    return render_template('email.html', email_content=email_content)


@app.route('/launch_discord')
def launch_discord():
    os.startfile(r'C:\Users\jerom\AppData\Local\Discord\app-1.0.9034\Discord.exe')  # Lancer Discord en local
    return '', 204  # Réponse vide avec code 204 (No Content)

@app.route('/launch_skype')
def launch_skype():
    os.startfile(r'C:\Users\jerom\AppData\Local\Microsoft\WindowsApps\skype.exe')  # Lancer Discord en local
    return '', 204  # Réponse vide avec code 204 (No Content)

@app.route('/launch_whatsapp')
def launch_whatsapp():
    os.startfile(r'C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2407.10.0_x64__cv1g1gvanyjgm\WhatsApp.exe')  # Lancer Discord en local
    return '', 204  # Réponse vide avec code 204 (No Content)

if __name__ == '__main__':
    app.run(debug=True)
