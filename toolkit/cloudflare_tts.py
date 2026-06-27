import os
import requests
import json
from pathlib import Path

env_path = Path("/workspace/.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "")
CF_API_TOKEN = os.environ.get("CF_API_TOKEN", "")

MODELS = {
    "en": "@cf/myshell-ai/melotts",
    "tts": "@cf/myshell-ai/melotts",
}

class CloudflareTTS:
    def __init__(self):
        self.account_id = CF_ACCOUNT_ID
        self.api_token = CF_API_TOKEN
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run"

    def text_to_speech(self, text, lang="en"):
        if not self.api_token:
            print("⚠️ Cloudflare API token not configured")
            return None

        model = MODELS.get(lang, MODELS["en"])
        url = f"{self.base_url}/{model}"

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            },
            json={"prompt": text}
        )

        if response.status_code == 200:
            return response.content
        else:
            print(f"❌ TTS Error: {response.status_code}")
            return None

    def save_audio(self, text, output_path="output.mp3", lang="en"):
        audio = self.text_to_speech(text, lang)
        if audio:
            with open(output_path, "wb") as f:
                f.write(audio)
            print(f"✅ Audio saved: {output_path}")
            return output_path
        return None

if __name__ == "__main__":
    tts = CloudflareTTS()
    tts.save_audio("Hello, this is a test.", "test.mp3")