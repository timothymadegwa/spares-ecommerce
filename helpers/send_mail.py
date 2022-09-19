from django.conf import settings
import ssl
from email.message import EmailMessage
from smtplib import SMTP_SSL

def send_mail(receiver_mail, subject, message):
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = settings.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD

    port = EMAIL_PORT
    smtp_server = EMAIL_HOST
    sender_email = EMAIL_HOST_USER
    password = EMAIL_HOST_PASSWORD
    
    
    mail_message = message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_mail
    msg.set_content(mail_message)
    context = ssl.create_default_context()
    with SMTP_SSL(smtp_server , port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)