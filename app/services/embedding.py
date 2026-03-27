import requests
from app.config import GEMINI_API_KEY

def get_embedding(text: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent?key={GEMINI_API_KEY}"

    payload = {
        "content": {
            "parts": [{"text": text}]
        }
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    return response.json()["embedding"]["values"]

