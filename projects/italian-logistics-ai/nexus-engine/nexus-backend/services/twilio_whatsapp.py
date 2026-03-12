from twilio.rest import Client
from config import settings

class TwilioService:
    def __init__(self):
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        else:
            self.client = None

    def send_whatsapp_message(self, to_number, message_body):
        """
        Sends a WhatsApp message via Twilio.
        to_number should be in E.164 format, e.g., '+393331234567'
        """
        if not self.client:
            return {"error": "Twilio credentials missing"}
        
        try:
            # Twilio Sandbox requires 'whatsapp:' prefix
            formatted_to = f"whatsapp:{to_number}" if not to_number.startswith("whatsapp:") else to_number
            from_number = f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}"

            message = self.client.messages.create(
                body=message_body,
                from_=from_number,
                to=formatted_to
            )
            return {"sid": message.sid, "status": message.status}
        except Exception as e:
            return {"error": str(e)}

twilio_service = TwilioService()
