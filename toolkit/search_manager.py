import os
from pathlib import Path
from exa_manager import ExaManager

env_path = Path("/workspace/.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

class SearchManager:
    def __init__(self):
        self.exa = ExaManager()

    def search(self, query, num_results=10):
        try:
            results = self.exa.search(query, num_results=num_results)
            print(f"🔍 Exa: Found {len(results)} results")
            return results
        except Exception as e:
            print(f"⚠️ Exa error: {e}")
            return []

    def search_deep(self, query, num_results=5):
        try:
            results = self.exa.search_deep(query, num_results=num_results)
            print(f"🔬 Exa Deep: Found {len(results)} results")
            return results
        except Exception as e:
            print(f"⚠️ Exa error: {e}")
            return []

    def search_news(self, query, num_results=5):
        return self.search(f"news: {query}", num_results)

    def search_docs(self, query, num_results=5):
        return self.search(f"documentation: {query}", num_results)

    def get_content(self, urls):
        return self.exa.get_contents(urls)

if __name__ == "__main__":
    search = SearchManager()
    results = search.search("OpenSearch tutorial", num_results=3)
    for r in results:
        print(f"  - {r['title']}")
        print(f"    {r['url']}")