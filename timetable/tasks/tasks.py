import smtplib
from email.message import EmailMessage

from celery import Celery
from core.config import settings


app_celery = Celery('tasks', broker='redis://localhost:6379')

def letter_of_registration (username: str, user_email: str):
    email = EmailMessage()
    email['Subject'] = 'Уведомление о регистрации'
    email['From'] = settings.smtp.user
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {username}, Вы успешно прошли регистрацию на сайте ...</h1>'
        '</div>',
        subtype='html'
    )
    return email


@app_celery.task
def send_email_registration(username: str, user_email: str):
    email = letter_of_registration(username, user_email)
    with smtplib.SMTP_SSL(settings.smtp.host, settings.smtp.port) as server:
        server.login(user=settings.smtp.user, password=settings.smtp.password)
        server.send_message(email)