import requests
from config import AI_API_KEY, AI_MODEL
import os

class AIManager:
    def __init__(self, provider="local", api_key=None, model_path=None):
        self.provider = provider
        self.api_key = api_key or AI_API_KEY
        self.model = AI_MODEL
        self.model_path = model_path or "/workspace/models/qwen2.5-0.5b"
        self._local_model = None
        self._local_tokenizer = None

    def _load_local_model(self):
        if self._local_model is None:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            print("🔄 Loading Qwen2.5 locally...")
            self._local_tokenizer = AutoTokenizer.from_pretrained(
                self.model_path, trust_remote_code=True
            )
            self._local_model = AutoModelForCausalLM.from_pretrained(
                self.model_path, device_map="cpu", trust_remote_code=True
            )
            print("✅ Qwen2.5 loaded")
        return self._local_model, self._local_tokenizer

    def chat(self, messages, temperature=0.7, max_tokens=512):
        if self.provider == "local":
            return self._local_chat(messages, max_tokens)
        elif self.provider == "groq":
            return self._groq_chat(messages, temperature)
        elif self.provider == "openai":
            return self._openai_chat(messages, temperature)
        else:
            return self._local_chat(messages, max_tokens)

    def _local_chat(self, messages, max_tokens=512):
        model, tokenizer = self._load_local_model()
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = tokenizer(text, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=max_tokens)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("assistant\n")[-1].strip()

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
            {"role": "system", "content": "You are a search assistant. Analyze the query and suggest keywords. Reply in JSON: {\"keywords\": [...], \"search_type\": \"...\"}"},
            {"role": "user", "content": query}
        ]
        return self.chat(messages, temperature=0.3)

    def summarize(self, text, max_tokens=200):
        messages = [
            {"role": "system", "content": "Summarize the following text concisely."},
            {"role": "user", "content": text}
        ]
        return self.chat(messages, max_tokens=max_tokens)

    def translate(self, text, target_lang="English"):
        messages = [
            {"role": "system", "content": f"Translate to {target_lang}. Reply only with translation."},
            {"role": "user", "content": text}
        ]
        return self.chat(messages)