import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings


def email_login():
    return smtplib.SMTP(settings.EMAIL_SMTP_SERVER)


def envia_email(msg, from_, dest, subject):
    msg_mime = MIMEMultipart("alternative")
    msg_mime.set_charset("utf-8")
    msg_mime["FROM"] = from_
    msg_mime["Subject"] = subject
    msg_mime["To"] = dest[0]
    msg_mime["Bcc"] = from_
    attachment = MIMEText(msg.encode("utf-8"), "html", "UTF-8")
    msg_mime.attach(attachment)

    server = email_login()
    server.sendmail(from_, dest, msg_mime.as_string())


def notifica_por_email(operacao):
    from operations.messages import Mensagem
    message = Mensagem(operacao=operacao)
    envia_email(
        message.render(),
        from_=settings.EMAIL_HOST_USER,
        dest=settings.EMAIL_DEST_NOTIFY,
        subject=settings.EMAIL_SUBJECT
    )
