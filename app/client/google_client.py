# app/client/google_client.py

import requests
from app.client.base import ChatAPIClient

class GoogleAIClient(ChatAPIClient):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def send_message(self, messages: list[dict]) -> dict:
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        contents = []
        for m in messages:
            contents.append({
                "role": m["role"],
                "parts": [{"text": m["content"]}]
            })

        body = {
            "contents": contents
        }

        response = requests.post(self.endpoint, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()

        # Geminiはレスポンスがちょっと違うので取り出し
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        return {"content": text}
