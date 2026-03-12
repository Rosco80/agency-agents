from openai import OpenAI
from config import settings
import json

class OpenAITaskParser:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    def parse_driver_reply(self, message_text: str, context: str):
        """
        Workflow C: The AI-Parsed Reply
        Extracts delivery_id and status from a raw driver message.
        """
        if not self.client:
            return {"error": "OpenAI API Key missing"}

        system_prompt = (
            "You are a logistics parser for the NEXUS Engine. "
            "Extract the status update from the following driver message. "
            "The driver is likely reporting a delivery as finished or failed. "
            "Reply ONLY with a JSON object containing `delivery_id` (if identifiable from context) and `new_status` (one of: DELIVERED, FAILED)."
        )

        user_prompt = f"Context: {context}\nDriver Message: {message_text}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}

openai_parser = OpenAITaskParser()
