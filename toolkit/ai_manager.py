import requests
from config import AI_API_KEY, AI_MODEL

class AIManager:
    def __init__(self, provider="groq", api_key=None):
        self.provider = provider
        self.api_key = api_key or AI_API_KEY
        self.model = AI_MODEL

    def chat(self, messages, temperature=0.7):
        if self.provider == "groq":
            return self._groq_chat(messages, temperature)
        elif self.provider == "openai":
            return self._openai_chat(messages, temperature)
        else:
            return self._groq_chat(messages, temperature)

    def _groq_chat(self, messages, temperature):
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "messages": messages, "temperature": temperature}
        )
        return resp.json()["choices"][0]["message"]["content"]

    def _openai_chat(self, messages, temperature):
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": "gpt-4o-mini", "messages": messages, "temperature": temperature}
        )
        return resp.json()["choices"][0]["message"]["content"]

    def analyze_query(self, query):
        messages = [
            {"role": "system", "content": "You are a search assistant. Analyze the user query and suggest the best search strategy. Reply in JSON with fields: keywords, search_type, index_suggestion."},
            {"role": "user", "content": query}
        ]
        return self.chat(messages, temperature=0.3)