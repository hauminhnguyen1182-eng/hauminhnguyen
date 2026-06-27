import os
from exa_py import Exa
from pathlib import Path

env_path = Path("/workspace/.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

class ExaManager:
    def __init__(self):
        self.exa = Exa(api_key=os.environ.get("EXA_API_KEY"))

    def search(self, query, num_results=5):
        results = self.exa.search(
            query,
            type="auto",
            num_results=num_results,
            contents={"highlights": True}
        )
        return [{"title": r.title, "url": r.url, "highlights": r.highlights} for r in results.results]

    def search_deep(self, query, num_results=5):
        results = self.exa.search(
            query,
            type="deep",
            num_results=num_results,
            contents={"highlights": True}
        )
        return [{"title": r.title, "url": r.url, "highlights": r.highlights} for r in results.results]

    def get_contents(self, urls):
        results = self.exa.get_contents(urls, highlights=True)
        return [{"title": r.title, "url": r.url, "highlights": r.highlights} for r in results.results]

if __name__ == "__main__":
    exa = ExaManager()
    results = exa.search("OpenSearch tutorial", num_results=3)
    for r in results:
        print(f"  {r['title']}")
        print(f"  {r['url']}\n")