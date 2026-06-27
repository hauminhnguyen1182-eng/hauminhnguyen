import os
from pathlib import Path

env_path = Path("/workspace/.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

POSTGRES = {
    "host": os.environ.get("PG_HOST", "pg-2137e692-hauminhnguyen1182-7219.l.aivencloud.com"),
    "port": os.environ.get("PG_PORT", "23274"),
    "dbname": os.environ.get("PG_DB", "defaultdb"),
    "user": os.environ.get("PG_USER", "avnadmin"),
    "password": os.environ.get("PG_PASS", ""),
    "sslmode": "require"
}

OPENSEARCH = {
    "host": os.environ.get("OS_HOST", "os-8509b23-hauminhnguyen1182-7219.l.aivencloud.com"),
    "port": int(os.environ.get("OS_PORT", "23274")),
    "user": os.environ.get("OS_USER", "avnadmin"),
    "password": os.environ.get("OS_PASS", "")
}

AI_API_KEY = os.environ.get("GROQ_API_KEY", "")
AI_MODEL = "llama-3.3-70b-versatile"