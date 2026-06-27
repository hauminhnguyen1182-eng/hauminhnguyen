import os
import requests
from pathlib import Path

env_path = Path("/workspace/.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

MEILI_URL = "http://localhost:7700"
MEILI_KEY = "mimocode-key"

class MeilisearchManager:
    def __init__(self):
        self.url = MEILI_URL
        self.headers = {
            "Authorization": f"Bearer {MEILI_KEY}",
            "Content-Type": "application/json"
        }

    def create_index(self, uid, primary_key="id"):
        resp = requests.post(
            f"{self.url}/indexes",
            headers=self.headers,
            json={"uid": uid, "primaryKey": primary_key}
        )
        return resp.json()

    def add_documents(self, index_uid, documents):
        resp = requests.post(
            f"{self.url}/indexes/{index_uid}/documents",
            headers=self.headers,
            json=documents
        )
        return resp.json()

    def search(self, index_uid, query, limit=10):
        resp = requests.get(
            f"{self.url}/indexes/{index_uid}/search",
            headers=self.headers,
            params={"q": query, "limit": limit}
        )
        data = resp.json()
        return [{
            "id": r.get("id"),
            "title": r.get("title", ""),
            "content": r.get("content", "")[:200]
        } for r in data.get("hits", [])]

    def delete_document(self, index_uid, doc_id):
        resp = requests.delete(
            f"{self.url}/indexes/{index_uid}/documents/{doc_id}",
            headers=self.headers
        )
        return resp.json()

    def list_indexes(self):
        resp = requests.get(f"{self.url}/indexes", headers=self.headers)
        return [idx["uid"] for idx in resp.json().get("results", [])]

    def get_stats(self, index_uid):
        resp = requests.get(
            f"{self.url}/indexes/{index_uid}/stats",
            headers=self.headers
        )
        return resp.json()

if __name__ == "__main__":
    meili = MeilisearchManager()
    print(f"✅ Meilisearch connected!")
    print(f"📋 Indexes: {meili.list_indexes()}")