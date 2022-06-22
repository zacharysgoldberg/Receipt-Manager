import asyncio
from threading import Thread
from api import create_app, mail
from flask_mail import Message

app = create_app()


async def send_async_email(app, msg):
    with app.app_context():
        try:
            await mail.send(msg)
        except BaseException:
            raise "[MAIL_SERVER] not working"


def send_email(subject, sender, recipients, text):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text
    # mail.send(msg)
    Thread(target=send_async_email, args=(app, msg)).start()
