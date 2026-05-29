from twilio.rest import Client
from app.config import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_sms(to_number: str, message: str):
    client.messages.create(
        body=message,
        from_=settings.TWILIO_SMS_NUMBER,
        to=to_number
    )