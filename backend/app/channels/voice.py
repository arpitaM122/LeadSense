from twilio.rest import Client
from app.config import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def initiate_call(to_number: str, callback_url: str):
    call = client.calls.create(
        url=callback_url,  # TwiML URL for call instructions
        to=to_number,
        from_=settings.TWILIO_SMS_NUMBER  # or voice number
    )
    return call.sid