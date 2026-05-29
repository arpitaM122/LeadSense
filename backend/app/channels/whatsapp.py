from twilio.rest import Client
from app.config import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_whatsapp_buttons(to_number: str, buttons: list):
    to_whatsapp = f"whatsapp:{to_number}"
    from_whatsapp = f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}"
    message_body = "Choose an option:\n" + "\n".join(f"• {b}" for b in buttons)
    client.messages.create(
        body=message_body,
        from_=from_whatsapp,
        to=to_whatsapp
    )