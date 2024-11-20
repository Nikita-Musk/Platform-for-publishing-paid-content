import random

from twilio.rest import Client

from config.settings import ACCOUNT_SID, AUTH_TOKEN
from users.models import User


def generate_unique_token():
    """Генерируется уникальный токен для подтверждения регистрации."""
    while True:
        token = "".join(random.choices("0123456789", k=6))
        if not User.objects.filter(token=token).exists():
            return token


def send_sms_for_your_number(token, phone):
    """Отправление смс с помощью сервиса twilio."""
    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Ваш код подтверждения: {token}",
        from_="<Номер отправителя Twilio>",
        to=f"+{phone}",
    )
    print(message.sid)
