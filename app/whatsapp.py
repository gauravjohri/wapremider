from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()
client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH'))

def send_whatsapp(phone, message):
    client.messages.create(
        from_=os.getenv('WHATSAPP_FROM'),
        body=message,
        to=f'whatsapp:{phone}'
    )
