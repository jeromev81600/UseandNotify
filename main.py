from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message  # Importer les classes Mail et Message depuis flask_mail

app = Flask(__name__)

# Configuration de Flask-Mail avec les paramètres SMTP
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jerome.vilanova@hotmail.fr'
app.config['MAIL_PASSWORD'] = 'Jerome1234'

# Initialiser l'extension Flask-Mail avec l'application Flask
mail = Mail(app)

# Fonction pour envoyer un e-mail
def send_email(to, subject, body):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = body
    mail.send(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        to = request.form['to']
        subject = request.form['subject']
        body = request.form['body']

        if 'send' in request.form:
            # Appel à la fonction send_email pour envoyer l'e-mail
            send_email(to, subject, body)
            return redirect(url_for('success'))
        elif 'cancel' in request.form:
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
