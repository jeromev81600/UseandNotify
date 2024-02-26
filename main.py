from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from twilio.rest import Client
from config import *

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

# Fonction pour envoyer un e-mail
def send_email(to, subject, body):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = body
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
                send_email(recipient_info['email'], subject, body)
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
