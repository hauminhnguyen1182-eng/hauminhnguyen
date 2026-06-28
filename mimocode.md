# MiMoCode - Complete Reference

## Lệnh nhanh
- `/1` → Đọc file này - Quy tắc làm việc + Tools đã cài
- `/2` → Đọc tóm tắt phiên + Việc còn dang dở

---

# /1: QUY TẮC LÀM VIỆC + TOOLS

## Quy tắc với hauminhnguyen

1. **Ưu tiên free tier** - Không tốn token tiền
2. **Không root** - Không cài system package
3. **GitHub Push Protection** - Không commit secrets
4. **Tiếng Việt** - Trả lời ngắn gọn, súc tích
5. **Tối ưu RAM** - Chọn tools nhẹ, nhanh

## Tools đã cài & có thể vận hành

### AI & Search

| Tool | Chức năng | Câu lệnh |
|------|-----------|----------|
| Qwen2.5-0.5B | AI local miễn phí | `tk.ai_chat("câu hỏi")` |
| Exa AI | Web search neural | `tk.web_search("query")` |
| Meilisearch | Local fast search | `tk.meili_search("idx", "q")` |
| OpenSearch | Document storage | `tk.search_documents("q")` |

### Web & Browser

| Tool | Chức năng | Câu lệnh |
|------|-----------|----------|
| Playwright | Browser automation | `browser.goto("url")` |
| Cloudflare Pages | Static hosting | https://hauminhnguyen.pages.dev |
| GitHub Pages | Backup hosting | https://hauminhnguyen1182-eng.github.io/hauminhnguyen/ |

### Database & Storage

| Tool | Chức năng | Host |
|------|-----------|------|
| PostgreSQL | Relational DB | Aiven pg-2137e692:23274 |
| OpenSearch | Search engine | Aiven os-8509b23:23274 |
| Kafka | Event streaming | Aiven kafka:23278 |

### Automation

| Tool | Chức năng | Câu lệnh |
|------|-----------|----------|
| APScheduler | Task scheduling | `scheduler.add_interval("name", func, seconds=60)` |
| Python logging | Structured logs | `logger.info("msg")` |
| psutil | System monitor | `monitor.print_stats()` |

### Document Processing

| Tool | Chức năng | Library |
|------|-----------|---------|
| Word (.docx) | Tạo/sửa Word | python-docx |
| Excel (.xlsx) | Tạo/sửa Excel | openpyxl |
| PowerPoint (.pptx) | Tạo/sửa PPT | python-pptx |
| Text-to-Speech | Giọng nói AI | Cloudflare Workers AI |

### Chatbot

| Component | Status | URL |
|-----------|--------|-----|
| Flask API | ✅ | http://127.0.0.1:5000 |
| Cloudflare Tunnel | ✅ | https://acrylic-investors-christopher-downloadable.trycloudflare.com |
| Frontend | ✅ | https://hauminhnguyen.pages.dev/blog/chatbot |

## Cấu trúc thư mục

```
/workspace/
├── mimocode.md              ← File này
├── .env                     ← Secrets (không commit)
├── chatbot/                 ← Document chatbot
│   ├── app.py               ← Flask API
│   ├── doc_reader.py        ← Đọc file
│   ├── doc_writer.py        ← Tạo file
│   ├── ai_engine.py         ← AI (Qwen + Gemini)
│   └── run.sh               ← Startup script
├── toolkit/                 ← AI toolkit
│   ├── main.py              ← Main entry
│   ├── ai_manager.py        ← AI
│   ├── exa_manager.py       ← Search
│   ├── opensearch_manager.py
│   ├── meilisearch_manager.py
│   ├── browser_manager.py
│   ├── kafka_manager.py
│   ├── search_manager.py
│   ├── scheduler.py
│   ├── logger.py
│   ├── monitor.py
│   └── cloudflare_tts.py
├── models/qwen2.5-0.5b/    ← Local AI
├── blog/                    ← Website
├── workers/                 ← Cloudflare Workers
└── aiven_keepalive.py       ← Giữ活性 Aiven
```

## Khởi động services

```bash
# Chatbot
/workspace/chatbot/run.sh

# Meilisearch
/workspace/meilisearch --db-path /workspace/meilisearch-data --no-analytics --master-key "mimocode-key" &

# Keepalive Aiven
python3 /workspace/aiven_keepalive.py
```

---

# /2: TÓM TẮT PHIÊN + VIỆC CÒN DANG DỞ

## Phiên làm việc 27/06/2026

### Đã hoàn thành

| Hạng mục | Trạng thái |
|----------|-----------|
| GitHub Pages + Cloudflare Pages | ✅ |
| Blog với 3 bài viết | ✅ |
| Contact form (Formspree) | ✅ |
| PostgreSQL (Aiven) | ✅ |
| OpenSearch (Aiven) | ✅ |
| Kafka REST API (Aiven) | ✅ |
| Qwen2.5 Local AI | ✅ |
| Exa AI Search | ✅ |
| Meilisearch Local | ✅ |
| Cloudflare TTS | ✅ |
| Browser-use (Playwright) | ✅ |
| APScheduler + Logger + Monitor | ✅ |
| Document Chatbot | ✅ |
| Aiven Keepalive | ✅ |

### Việc còn dang dở

| Việc | Lý do | Ưu tiên |
|------|-------|---------|
| Gemini API key | Chưa có key | Cao |
| Kafka SSL connection | Cần CA cert đúng | Trung bình |
| PowerPoint template đẹp | Cần mẫu tham khảo | Trung bình |
| Cloudflare Tunnel ổn định | Hay restart khi timeout | Cao |
| Image generation cho PPT | Pollinations.ai OK nhưng chưa tích hợp | Thấp |

### Liên hệ

- Email: hauminhnguyen1182@gmail.com
- GitHub: https://github.com/hauminhnguyen1182-eng

### Cloudflare Tunnel Note

- Free tier tạo URL mới mỗi lần restart
- Để giữ URL cố định: dùng Cloudflare Named Tunnel (cần account)
- Hiện tại dùng Quick Tunnel (tự động URL)