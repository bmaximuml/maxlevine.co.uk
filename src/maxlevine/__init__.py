import logging

from datetime import datetime
from email.message import EmailMessage
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_xcaptcha import XCaptcha
from os import environ
from requests import post
from secrets import token_hex
from smtplib import SMTP_SSL, SMTPRecipientsRefused
from wtforms import Field, Form, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, length

from maxlevine.models import db, Skill, Project, About

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ENV_VAR_PREFIX='ML_'

REQUIRED_VARS = [
    'DB_USERNAME',
    'DB_PASSWORD',
    'DB_HOST',
    'DB_PORT',
    'DB_DRIVER',
    'DB_NAME',
    'SMTP_HOST',
    'SMTP_USERNAME',
    'SMTP_PASSWORD',
    'SMTP_PORT',
    'XCAPTCHA_SITE_KEY',
    'XCAPTCHA_SECRET_KEY',
    'XCAPTCHA_VERIFY_URL',
    'XCAPTCHA_API_URL',
    'XCAPTCHA_DIV_CLASS',
]
OPTIONAL_VARS = [
    ('SECRET_KEY', token_hex(64)),
    ('TITLE', 'Max Levine'),
    ('AUTHOR', 'Max Levine')
]

def read_file(file):
    with open(file, 'r') as f:
        result = f.read().strip()
        return result


def create_application():
    app = Flask(__name__)
    for var in REQUIRED_VARS:
        env_var = f'{ENV_VAR_PREFIX}{var}'
        try:
            app.config[var.lower()] = read_file(environ[f'{env_var}_FILE'])
        except (KeyError, FileNotFoundError):
            try:
                app.config[var.lower()] = environ[env_var]
            except KeyError:
                raise KeyError(f'{env_var} environment variable must be set')

    # for var, default in OPTIONAL_VARS:
    for var, default in OPTIONAL_VARS:
        env_var = f'{ENV_VAR_PREFIX}{var}'
        try:
            app.config[var.lower()] = read_file(environ[f'{env_var}_FILE'])
        except (KeyError, FileNotFoundError):
            try:
                app.config[var.lower()] = environ[env_var]
            except KeyError:
                app.config[var.lower()] = default

    db_driver = app.config.get('db_driver').lower().strip()
    if db_driver == 'mysql':
        sqlalchemy_database_uri = (
            'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
                app.config.get('db_username'),
                app.config.get('db_password'),
                app.config.get('db_host'),
                app.config.get('db_port'),
                app.config.get('db_name'),
            )
        )
        app.config.update({
            'SQLALCHEMY_DATABASE_URI': sqlalchemy_database_uri,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        })
    app.secret_key = app.config.get('secret_key')
    app.config.update({
        'XCAPTCHA_SITE_KEY': app.config.get('xcaptcha_site_key'),
        'XCAPTCHA_SECRET_KEY': app.config.get('xcaptcha_secret_key'),
        'XCAPTCHA_VERIFY_URL': app.config.get('xcaptcha_verify_url'),
        'XCAPTCHA_API_URL': app.config.get('xcaptcha_api_url'),
        'XCAPTCHA_DIV_CLASS': app.config.get('xcaptcha_div_class'),
    })

    db.init_app(app)
    return app


app = create_application()
xcaptcha = XCaptcha(app=app)

info = {
    'title' : 'Max Levine',
    'fname' : 'Max',
    'email' : 'max@maxlevine.co.uk',
    'linkedin' : 'https://www.linkedin.com/in/bmaxlevine/',
    'github' : 'https://github.com/bmaximuml',
    'gitlab' : 'https://gitlab.com/bmaximuml',
    'cv_file' : 'https://static.maxlevine.co.uk/files/Max_Levine_CV.pdf',
    'main_photo' :  'https://static.maxlevine.co.uk/images/portrait.jpg',
    'second_photo' : 'https://static.maxlevine.co.uk/images/Madrid.jpg',
    'logo' : 'https://static.maxlevine.co.uk/images/logo.svg',
    'logo_png' : 'https://static.maxlevine.co.uk/images/logo.png',
}

class ContactForm(Form):
    name = StringField('Name',
        validators=[DataRequired(), length(max=200)],
        render_kw={
            "placeholder": "Name",
            "class": "input",
            "maxlength": 200
        }
    )
    email = EmailField('Email Address',
        validators=[
            DataRequired(),
            Email(message="Invalid email address"),
            length(max=200)
        ],
        render_kw={
            "placeholder": "Email",
            "class": "input",
            "maxlength": 200
        }
    )
    message = TextAreaField('Message',
        validators=[DataRequired(), length(max=5000)],
        render_kw={
            "placeholder": "Enter your message here...",
            "class": "textarea",
            "rows": 5,
            "maxlength": 5000
        }
    )
    submit = SubmitField('Send', render_kw={"class": "button is-link"})


@app.route('/', methods=['POST', 'GET'])
def about():
    skills = Skill.query.all()
    about_data = About.query.order_by(About.priority).all()
    projects = Project.query.order_by(Project.priority).all()

    form = ContactForm(request.form)
    if request.method == 'POST':
        if form.validate() and xcaptcha.verify():      
            try:
                send_message(form.name.data, form.email.data, form.message.data)
                flash('Message successfully sent!')
            except SMTPRecipientsRefused as e:
                flash('Invalid email address entered. Message not sent.')
                email_bug_report(
                    form.name.data,
                    form.email.data,
                    form.message.data,
                    e
                )
            except Exception as e:
                flash('Unknown error occurred. Message not sent.')
                email_bug_report(
                    form.name.data,
                    form.email.data,
                    form.message.data,
                    e
                )
        elif not form.validate():
            flash('Invalid data supplied, message not sent.')            
        elif not xcaptcha.verify():
            flash('Bot suspected, message not sent.')
        else:
            flash('Error occurred, message not sent.')
        return redirect(url_for('about', _anchor='contact'))

    return render_template('index.html',
        year=datetime.now().year,
        about=about_data,
        projects=projects,
        skills=skills,
        form=form,
        **info
    )


def send_message(name, email, message, subject=None):
    send_to = 'contactform@maxlevine.co.uk'

    s = SMTP_SSL(
        environ['MAX_LEVINE_SMTP_HOST'],
        environ['MAX_LEVINE_SMTP_PORT']
    )

    s.login(
        environ['MAX_LEVINE_SMTP_USERNAME'],
        environ['MAX_LEVINE_SMTP_PASSWORD']
    )

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = f'{name} - maxlevine.co.uk Contact Form' if subject is None else subject
    msg['From'] = email
    msg['To'] = send_to

    s.send_message(msg)
    s.quit()


def email_bug_report(name, email, message, error):
    e_from = 'website@maxlevine.co.uk'
    subject = 'Bug Report - maxlevine.co.uk'
    message = (
        f'Name: {name}\n' +
        f'From: {email}\n' +
        f'Message: {message}\n' +
        f'Error: {error}'
    )

    send_message('Bug Report', e_from, message, subject=subject)


if __name__ == '__main__':
    app.debug = True
    app.run()
