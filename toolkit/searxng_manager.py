import httpx
import json
from urllib.parse import quote

# Public SearXNG instances (fallback list)
SEARXNG_INSTANCES = [
    "https://search.bus-hit.me",
    "https://searx.tiekoetter.com",
    "https://search.ononoki.org",
    "https://searxng.ch",
    "https://search.sapti.me",
]

class SearxNGManager:
    def __init__(self, instance_url=None):
        self.instance_url = instance_url or SEARXNG_INSTANCES[0]
        self.client = httpx.Client(timeout=10)

    def search(self, query, num_results=10, categories="general"):
        for instance in SEARXNG_INSTANCES:
            try:
                resp = self.client.get(
                    f"{instance}/search",
                    params={
                        "q": query,
                        "format": "json",
                        "categories": categories,
                        "language": "auto"
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])[:num_results]
                    return [{
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("content", "")[:200]
                    } for r in results]
            except Exception:
                continue
        return []

    def search_images(self, query, num_results=5):
        return self.search(query, num_results, "images")

    def search_news(self, query, num_results=5):
        return self.search(query, num_results, "news")

    def search_videos(self, query, num_results=5):
        return self.search(query, num_results, "videos")

if __name__ == "__main__":
    searx = SearxNGManager()
    results = searx.search("OpenSearch tutorial", num_results=3)
    print(f"🔍 Found {len(results)} results")
    for r in results:
        print(f"  - {r['title']}")
        print(f"    {r['url']}")