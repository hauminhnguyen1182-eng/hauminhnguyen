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

    def generate(self, file_content, task="summarize", template=None, user_input=None):
        if self.gemini_key:
            try:
                return self._gemini_generate(file_content, task, template, user_input)
            except Exception as e:
                print(f"Gemini failed: {e}, falling back to local")
        return self._local_generate(file_content, task, template, user_input)

    def _gemini_generate(self, content, task, template=None, user_input=None):
        if task == "fill_template" and template and user_input:
            prompt = self._build_template_prompt(content, template, user_input)
        elif task == "draft_from_template" and template:
            prompt = self._build_draft_prompt(content, template, user_input)
        else:
            prompts = {
                "summarize": f"Tóm tắt nội dung sau bằng tiếng Việt:\n\n{content[:3000]}",
                "draft": f"Soạn thảo văn bản chuyên nghiệp dựa trên nội dung:\n\n{content[:3000]}",
                "rewrite": f"Viết lại nội dung cho rõ ràng và chuyên nghiệp:\n\n{content[:3000]}",
            }
            prompt = prompts.get(task, prompts["summarize"])

        resp = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_key}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=60
        )
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

    def _build_template_prompt(self, content, template, user_input):
        template_text = "\n".join([f"- {s['text']}" for s in template.get("structure", [])[:10]])
        placeholders = template.get("placeholders", [])

        return f"""Bạn là chuyên gia soạn thảo văn bản chuyên nghiệp.

Cấu trúc mẫu (giữ nguyên định dạng):
{template_text}

Các vị trí cần điền: {', '.join(placeholders) if placeholders else 'Không có'}

Nội dung thô từ người dùng:
{user_input}

Yêu cầu:
1. Giữ nguyên cấu trúc và định dạng của mẫu
2. Điền nội dung thô vào các vị trí phù hợp
3. Viết lại nội dung cho chuyên nghiệp, rõ ràng
4. Không thay đổi thứ tự các mục trong mẫu
5. Trả về văn bản hoàn chỉnh theo đúng cấu trúc mẫu"""

    def _build_draft_prompt(self, content, template, user_input=None):
        template_text = "\n".join([f"- {s['text']}" for s in template.get("structure", [])[:10]])

        extra_info = f"\nNội dung bổ sung: {user_input}" if user_input else ""

        return f"""Bạn là chuyên gia soạn thảo văn bản.

Cấu trúc mẫu:
{template_text}{extra_info}

Yêu cầu:
1. Soạn thảo văn bản theo đúng cấu trúc mẫu trên
2. Viết nội dung chuyên nghiệp, đầy đủ thông tin
3. Giữ nguyên thứ tự và格式 các mục
4. Trả về văn bản hoàn chỉnh"""

    def _local_generate(self, content, task, template=None, user_input=None):
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if self.local_model is None:
            print("Loading Qwen2.5...")
            model_path = "/workspace/models/qwen2.5-0.5b"
            self.local_tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.local_model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cpu")

        if task == "fill_template" and template and user_input:
            template_text = "\n".join([f"- {s['text']}" for s in template.get("structure", [])[:5]])
            prompt = f"Mẫu:\n{template_text}\n\nNội dung:\n{user_input}\n\nViết lại theo mẫu:"
        elif task == "draft_from_template" and template:
            template_text = "\n".join([f"- {s['text']}" for s in template.get("structure", [])[:5]])
            prompt = f"Mẫu:\n{template_text}\n\nSoạn thảo:"
        else:
            prompts = {
                "summarize": f"Tóm tắt:\n{content[:1000]}",
                "draft": f"Soạn thảo:\n{content[:1000]}",
                "rewrite": f"Viết lại:\n{content[:1000]}",
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
