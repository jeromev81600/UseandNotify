from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from twilio.rest import Client
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

# Liste des destinataires
recipients = RECIPIENTS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        to = request.form['to']
        subject = request.form['subject']
        body = request.form['body']

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
            return redirect(url_for('success'))
        else:
            # Gérer le cas où le destinataire sélectionné n'existe pas
            pass

    return render_template('index.html', recipients=recipients)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
