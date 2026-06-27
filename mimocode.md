# MiMoCode - Complete Reference

## Quick Commands
- `/1` → Open this file (full reference)
- `/toolkit` → Run AI Toolkit
- `/search` → Exa AI Search
- `/tts` → Text-to-Speech
- `/meili` → Meilisearch local

---

## System Status

| Component | Status | Location |
|-----------|--------|----------|
| GitHub Pages | ✅ | https://hauminhnguyen1182-eng.github.io/hauminhnguyen/ |
| Cloudflare Pages | ✅ | https://hauminhnguyen.pages.dev |
| PostgreSQL | ✅ | Aiven (pg-2137e692) |
| OpenSearch | ✅ | Aiven (os-8509b23) |
| Kafka | ✅ | Aiven REST API (port 23278) |
| Qwen2.5 Local | ✅ | /workspace/models/qwen2.5-0.5b/ |
| Exa AI | ✅ | Cloud API |
| Meilisearch | ✅ | localhost:7700 |
| Cloudflare TTS | ✅ | Workers AI |
| Browser-use | ✅ | Playwright + Chromium |

---

## AI Toolkit

### Initialize
```python
import sys
sys.path.insert(0, "/workspace/toolkit")
from main import Toolkit

tk = Toolkit(ai_provider="local")
```

### AI Chat (Qwen2.5 Local)
```python
tk.ai_chat("What is OpenSearch?")
```

### Web Search (Exa)
```python
tk.web_search("query", num_results=10)
tk.web_search_news("AI news")
tk.web_search_docs("Kafka tutorial")
```

### Document Search (OpenSearch)
```python
tk.add_document("id", "title", "content")
tk.search_documents("query")
```

### Local Fast Search (Meilisearch)
```python
tk.meili_add("docs", [{"id": 1, "title": "Guide"}])
tk.meili_search("docs", "query", limit=10)
```

### Translation
```python
tk.ai_translate("Hello", lang="Vietnamese")
```

### Summarization
```python
tk.ai_summarize("long text...")
```

### Kafka Events
```python
tk.kafka_send("page_view", {"page": "blog"})
events = tk.kafka_consume(max_messages=10)
```

### Text-to-Speech
```python
from toolkit.cloudflare_tts import CloudflareTTS
tts = CloudflareTTS()
tts.save_audio("Hello world", "output.mp3")
```

### Scheduler
```python
# Run task every 5 minutes
tk.scheduler.add_interval("reindex", func=my_func, seconds=300)

# Run task daily at 9am
tk.scheduler.add_cron("daily_report", func=my_func, hour=9, minute=0)

# List tasks
tk.scheduler.list_tasks()
```

### Logger
```python
tk.logger.info("Task started")
tk.logger.task_start("reindex")
tk.logger.task_done("reindex")
tk.logger.error("Something failed")
```

### Monitor
```python
tk.monitor.print_stats()
# CPU: 15% | RAM: 2.1GB/9.7GB (21%) | Disk: 25GB/1007GB

stats = tk.monitor.stats()
```

---

## Search Stack

| Engine | Use Case | Speed |
|--------|----------|-------|
| Exa AI | Web search, neural | ~1s |
| Meilisearch | Local fast search | ~10ms |
| OpenSearch | Document storage | ~100ms |

---

## Browser Automation

```python
import asyncio
from toolkit.browser_manager import BrowserManager

browser = BrowserManager()

async def run():
    await browser.start()
    await browser.goto("https://example.com")
    text = await browser.get_text()
    await browser.stop()
    return text

asyncio.run(run())
```

---

## Web Pages

```
/workspace/
├── index.html              ← Homepage
├── contact.html            ← Contact form (Formspree)
├── style.css               ← Global styles
├── blog/
│   ├── index.html          ← Blog listing
│   ├── setup-github-pages.html
│   ├── cloudflare-pages.html
│   └── web-analytics.html
├── blog/assets/
│   └── audio-player.js     ← TTS player
└── workers/
    ├── tts-worker.js       ← Cloudflare Worker
    └── wrangler.toml       ← Config
```

---

## Services

### GitHub
- Repo: https://github.com/hauminhnguyen1182-eng/hauminhnguyen
- SSH Key: ~/.ssh/id_ed25519
- Branch: main

### Aiven
| Service | Host | Port |
|---------|------|------|
| PostgreSQL | pg-2137e692-hauminhnguyen1182-7219.l.aivencloud.com | 23274 |
| OpenSearch | os-8509b23-hauminhnguyen1182-7219.l.aivencloud.com | 23274 |
| Kafka REST | kafka-17dd3441-hauminhnguyen1182-7219.b.aivencloud.com | 23278 |

### Cloudflare
- Account ID: 071779bca1938f1e1db98b8c237afcc2
- TTS Model: @cf/myshell-ai/melotts
- Pages: https://hauminhnguyen.pages.dev

---

## Environment Variables

```env
# PostgreSQL
PG_HOST=pg-2137e692-hauminhnguyen1182-7219.l.aivencloud.com
PG_PORT=23274
PG_DB=defaultdb
PG_USER=avnadmin
PG_PASS=<see .env>

# OpenSearch
OS_HOST=os-8509b23-hauminhnguyen1182-7219.l.aivencloud.com
OS_PORT=23274
OS_USER=avnadmin
OS_PASS=<see .env>

# Kafka
KAFKA_PASS=<see .env>

# Exa AI
EXA_API_KEY=<see .env>

# Cloudflare
CF_ACCOUNT_ID=071779bca1938f1e1db98b8c237afcc2
CF_API_TOKEN=<see .env>
```

> Secrets in `/workspace/.env` (never committed)

---

## Toolkit Files

| File | Purpose |
|------|---------|
| main.py | Main entry |
| ai_manager.py | AI (Qwen2.5 + Groq) |
| exa_manager.py | Exa web search |
| opensearch_manager.py | Document storage |
| browser_manager.py | Browser automation |
| kafka_manager.py | Event streaming |
| search_manager.py | Search orchestrator |
| meilisearch_manager.py | Local fast search |
| cloudflare_tts.py | Text-to-Speech |
| config.py | Load .env |

---

## Start Services

### Meilisearch
```bash
/workspace/meilisearch --db-path /workspace/meilisearch-data --no-analytics --master-key "mimocode-key" &
```

### Toolkit Test
```python
cd /workspace/toolkit && python3 -c "from main import Toolkit; tk = Toolkit(); print('OK')"
```

---

## Installed Packages

torch, transformers, playwright, browser-use, exa-py, opensearch-py, psycopg2-binary, confluent-kafka, meilisearch, whoosh, httpx, beautifulsoup4

---

## Contact
- Email: hauminhnguyen1182@gmail.com
- GitHub: https://github.com/hauminhnguyen1182-eng