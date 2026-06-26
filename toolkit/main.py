from opensearch_manager import OpenSearchManager
from browser_manager import BrowserManager
from ai_manager import AIManager
import asyncio

class Toolkit:
    def __init__(self, ai_provider="groq", ai_key=None):
        self.search = OpenSearchManager()
        self.browser = BrowserManager()
        self.ai = AIManager(provider=ai_provider, api_key=ai_key)

    def init_indices(self):
        self.search.create_index("documents")
        self.search.create_index("web_cache")
        print("✅ Indices ready")

    def search_documents(self, query, index="documents"):
        results = self.search.search(index, query)
        print(f"🔍 Found {len(results)} results for '{query}'")
        for r in results:
            print(f"  - {r['title']} (score: {r['score']:.2f})")
        return results

    def add_document(self, doc_id, title, content, index="documents"):
        self.search.index_document(index, doc_id, {"title": title, "content": content})

    async def search_web(self, query):
        await self.browser.start()
        results = await self.browser.search_google(query)
        for r in results:
            self.search.index_document("web_cache", r["url"],
                {"title": r["title"], "content": r["url"]})
        await self.browser.stop()
        print(f"🌐 Cached {len(results)} web results")
        return results

    async def browse_and_store(self, url):
        await self.browser.start()
        await self.browser.goto(url)
        text = await self.browser.get_text()
        title = await self.browser.goto(url)
        self.search.index_document("documents", url,
            {"title": title, "content": text[:5000]})
        await self.browser.stop()
        print(f"📄 Stored: {title}")
        return {"title": title, "content_length": len(text)}

    def smart_search(self, query):
        print(f"🤖 AI analyzing: {query}")
        analysis = self.ai.analyze_query(query)
        print(f"📊 Analysis: {analysis}")

        results = self.search_documents(query)
        if not results:
            print("⚠️ No local results, try: toolkit.search_web()")
        return results

    def stats(self):
        indices = self.search.list_indices()
        print(f"📊 Indices: {indices}")
        for idx in indices:
            count = self.search.client.count(index=idx)["count"]
            print(f"  - {idx}: {count} docs")

if __name__ == "__main__":
    toolkit = Toolkit()
    toolkit.init_indices()
    toolkit.add_document("1", "Hello World", "This is a test document")
    toolkit.search_documents("test")
    toolkit.stats()