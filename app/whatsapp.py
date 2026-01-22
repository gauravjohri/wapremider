from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()
client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH'))

def normalize_phone(phone: str) -> str:
    phone = phone.strip()              # remove spaces
    phone = phone.replace(" ", "")     # remove internal spaces

    if not phone.startswith("+"):
        phone = "+" + phone

    return phone


def send_whatsapp(phone, message):
    phone = normalize_phone(phone)
    client.messages.create(
        from_=os.getenv('WHATSAPP_FROM'),
        body=message,
        to=f'whatsapp:{phone}'
    )
