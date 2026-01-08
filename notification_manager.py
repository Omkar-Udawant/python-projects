import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:

    def __init__(self):
        self.client = Client(
            os.getenv("TWILIO_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )

    def send_whatsapp(self, message_body):
        message = self.client.messages.create(
            from_=f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}",
            to=f"whatsapp:{os.getenv('TWILIO_VERIFIED_NUMBER')}",
            body=message_body
        )
        print(message.sid)
