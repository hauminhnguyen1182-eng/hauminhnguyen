import os
import requests
from pathlib import Path

env_path = Path("/workspace/.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

class AIEngine:
    def __init__(self):
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "")
        self.local_model = None
        self.local_tokenizer = None

    def generate(self, file_content, task="summarize"):
        if self.gemini_key:
            try:
                return self._gemini_generate(file_content, task)
            except Exception as e:
                print(f"Gemini failed: {e}, falling back to local")
        return self._local_generate(file_content, task)

    def _gemini_generate(self, content, task):
        prompts = {
            "summarize": f"Tóm tắt nội dung sau bằng tiếng Việt:\n\n{content[:3000]}",
            "draft": f"Soạn thảo văn bản chuyên nghiệp dựa trên nội dung:\n\n{content[:3000]}",
            "rewrite": f"Viết lại nội dung cho rõ ràng và chuyên nghiệp:\n\n{content[:3000]}",
        }
        prompt = prompts.get(task, prompts["summarize"])

        resp = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_key}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=30
        )
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

    def _local_generate(self, content, task):
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if self.local_model is None:
            print("Loading Qwen2.5...")
            model_path = "/workspace/models/qwen2.5-0.5b"
            self.local_tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.local_model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cpu")

        prompts = {
            "summarize": f"Tóm tắt nội dung sau:\n{content[:1000]}",
            "draft": f"Soạn thảo văn bản:\n{content[:1000]}",
            "rewrite": f"Viết lại nội dung:\n{content[:1000]}",
        }
        prompt = prompts.get(task, prompts["summarize"])

        messages = [{"role": "user", "content": prompt}]
        text = self.local_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.local_tokenizer(text, return_tensors="pt")
        outputs = self.local_model.generate(**inputs, max_new_tokens=512)
        return self.local_tokenizer.decode(outputs[0], skip_special_tokens=True).split("assistant\n")[-1].strip()

if __name__ == "__main__":
    engine = AIEngine()
    print("✅ AIEngine ready")
