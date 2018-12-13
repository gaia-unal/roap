'''
Abstract tasks.
'''
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import gettext

import jwt

from redis import Redis
from rq import Queue


def queue():
    '''
    Get ourselves a default queue.
    '''
    return Queue('account_validation', connection=Redis(host='redis'))


def send_email(receiver_email, user_lang):
    """Send user account validation."""
    # TODO: add sender to config file.
    server = smtplib.SMTP('smtp.gmail.com:587')
    _ = gettext.translation('account_validation', '/code/locale', languages=[user_lang]).gettext
    server.ehlo()
    server.starttls()
    sender = 'roap.unal.master@gmail.com'
    server.login(sender, "@roap@unal@master")

    token = jwt.encode(
        {'email': receiver_email},
        'dsvalenciah_developer',
        algorithm='HS512'
    ).decode('utf-8')

    message = MIMEMultipart('alternative')

    message['Subject'] = "ROAp account validation"
    message['From'] = sender
    message['To'] = receiver_email

    # TODO: fix host.
    validate_message = _('Hi! Please, click on this <a href="{url}/{token}">link</a> to validate your account.').format(
        url='http://localhost:8081/user-validate', token=token)

    html = """
            <html>
                <head></head>
                <body>
                    <p>
                       {validate_message}
                    </p>
                </body>
            </html>
        """.format(validate_message=validate_message)

    message.attach(MIMEText(html, 'html'))

    server.sendmail(
        sender,
        receiver_email,
        message.as_string()
    )
    server.quit()