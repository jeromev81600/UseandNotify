from flask import Flask, render_template, request, redirect, url_for
import subprocess
import time
import os
import webbrowser
from waitress import serve
from messaging.messaging import *
from config.config import *

app = Flask(__name__)

# Liste des destinataires (dictionnaire)
recipients = RECIPIENTS

# Configuration de Flask-Mail avec les paramètres SMTP
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL

# Initialisation de Flask-Mail
init_app(app)


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
                    send_email_with_attachment(app, recipient_info['email'], subject, body, file_path)
                else:
                    send_email_with_attachment(app, recipient_info['email'], subject, body, None)
            elif 'send_sms' in request.form:
                send_sms(recipient_info['phone'], body)
        else:
            # Gérer le cas où le destinataire sélectionné n'existe pas
            pass
    emails_content, emails_titles = fetch_emails()
    return render_template('index.html', recipients=recipients, emails_titles=emails_titles,
                           emails_content=emails_content)


@app.route('/emails/<int:email_id>')
def email_detail(email_id):
    emails_content, _ = fetch_emails()
    email_content = emails_content[email_id]
    return render_template('email.html', email_content=email_content)


# Lancement de la plateforme Discord en local
@app.route('/launch_discord')
def launch_discord():
    os.startfile(r'C:\Users\jerom\AppData\Local\Discord\app-1.0.9034\Discord.exe')
    return '', 204  # Réponse vide avec code 204 (No Content)


# Lancement de la plateforme WhatsApp en local
@app.route('/launch_whatsapp')
def launch_whatsapp():
    os.startfile(
        r'C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2407.10.0_x64__cv1g1gvanyjgm\WhatsApp.exe')
    return '', 204  # Réponse vide avec code 204 (No Content)


# Lancement de la plateforme Skype en local
@app.route('/launch_skype')
def launch_skype():
    os.startfile(r'C:\Users\jerom\AppData\Local\Microsoft\WindowsApps\skype.exe')
    return '', 204  # Réponse vide avec code 204 (No Content)


if __name__ == '__main__':
    app.run(debug=True)
    # Ouvre le navigateur par défaut et Démarre le serveur Waitress
    # serve(app, host=LOCALHOST, port=PORT)
    # webbrowser.open('http://{LOCALHOST}:{PORT}')
