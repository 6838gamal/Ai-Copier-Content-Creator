import requests
from app.config import GEMINI_API_KEY, GEMINI_URL

def generate_text(prompt: str, temperature: float = 0.7, max_output_tokens: int = 512):
    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"

    payload = {
        "prompt": {"text": prompt},
        "temperature": temperature,
        "maxOutputTokens": max_output_tokens
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["output"]["text"]
