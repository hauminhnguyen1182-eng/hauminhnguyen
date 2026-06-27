from opensearch_manager import OpenSearchManager
from browser_manager import BrowserManager
from ai_manager import AIManager
from exa_manager import ExaManager
from kafka_manager import KafkaManager
from search_manager import SearchManager
from meilisearch_manager import MeilisearchManager
from scheduler import TaskScheduler
from logger import AppLogger
from monitor import SystemMonitor
import asyncio

class Toolkit:
    def __init__(self, ai_provider="local", ai_key=None, model_path=None):
        self.search = OpenSearchManager()
        self.browser = BrowserManager()
        self.ai = AIManager(provider=ai_provider, api_key=ai_key, model_path=model_path)
        self.exa = ExaManager()
        self.kafka = KafkaManager()
        self.web_search = SearchManager()
        self.meili = MeilisearchManager()
        self.scheduler = TaskScheduler()
        self.logger = AppLogger()
        self.monitor = SystemMonitor()

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

    def search_exa(self, query, num_results=5):
        results = self.exa.search(query, num_results=num_results)
        print(f"🌐 Exa found {len(results)} results")
        for r in results:
            print(f"  - {r['title']}")
            print(f"    {r['url']}")
        return results

    def search_exa_deep(self, query, num_results=5):
        results = self.exa.search_deep(query, num_results=num_results)
        print(f"🔬 Exa Deep found {len(results)} results")
        for r in results:
            print(f"  - {r['title']}")
        return results

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
        local = self.search_documents(query)
        exa = self.search_exa(query, num_results=3)
        return {"local": local, "exa": exa}

    def ai_chat(self, question):
        messages = [{"role": "user", "content": question}]
        response = self.ai.chat(messages)
        print(f"🤖 AI: {response}")
        return response

    def ai_summarize(self, text):
        return self.ai.summarize(text)

    def ai_translate(self, text, lang="English"):
        return self.ai.translate(text, lang)

    def kafka_send(self, event_type, data):
        self.kafka.send_event(event_type, data)
        print(f"📨 Event sent: {event_type}")

    def kafka_consume(self, topic="website-events", max_messages=10):
        return self.kafka.consume(topic, max_messages=max_messages)

    def web_search(self, query, num_results=10):
        return self.web_search.search(query, num_results)

    def web_search_news(self, query, num_results=5):
        return self.web_search.search_news(query, num_results)

    def web_search_docs(self, query, num_results=5):
        return self.web_search.search_docs(query, num_results)

    def meili_add(self, index_uid, documents):
        return self.meili.add_documents(index_uid, documents)

    def meili_search(self, index_uid, query, limit=10):
        return self.meili.search(index_uid, query, limit)

    def meili_stats(self):
        return self.meili.list_indexes()

    def stats(self):
        indices = self.search.list_indices()
        print(f"📊 Indices: {indices}")
        for idx in indices:
            count = self.search.client.count(index=idx)["count"]
            print(f"  - {idx}: {count} docs")

if __name__ == "__main__":
    print("🚀 AI Toolkit: Qwen2.5 + Exa + OpenSearch")
    print("=" * 50)

    toolkit = Toolkit(ai_provider="local")
    toolkit.init_indices()

    print("\n🌐 Test Exa Search:")
    toolkit.search_exa("OpenSearch tutorial", num_results=3)

    print("\n💬 Test AI Chat:")
    toolkit.ai_chat("What is OpenSearch?")

    toolkit.stats()