from opensearchpy import OpenSearch
from config import OPENSEARCH

class OpenSearchManager:
    def __init__(self):
        self.client = OpenSearch(
            hosts=[{"host": OPENSEARCH["host"], "port": OPENSEARCH["port"]}],
            http_auth=(OPENSEARCH["user"], OPENSEARCH["password"]),
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )

    def create_index(self, index_name, settings=None):
        if not self.client.indices.exists(index=index_name):
            body = settings or {
                "settings": {"number_of_shards": 1, "number_of_replicas": 0},
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "content": {"type": "text"},
                        "url": {"type": "keyword"},
                        "timestamp": {"type": "date"}
                    }
                }
            }
            self.client.indices.create(index=index_name, body=body)
            print(f"✅ Created index: {index_name}")
        return True

    def index_document(self, index_name, doc_id, document):
        self.client.index(index=index_name, id=doc_id, body=document)
        print(f"✅ Indexed doc: {doc_id}")

    def search(self, index_name, query, size=10):
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "content"]
                }
            },
            "size": size
        }
        results = self.client.search(index=index_name, body=body)
        return [{"title": h["_source"].get("title", ""),
                 "content": h["_source"].get("content", "")[:200],
                 "score": h["_score"]} for h in results["hits"]["hits"]]

    def bulk_index(self, index_name, documents):
        actions = []
        for doc in documents:
            actions.append({"index": {"_index": index_name, "_id": doc["id"]}})
            actions.append({"title": doc["title"], "content": doc["content"]})
        self.client.bulk(body=actions)
        print(f"✅ Bulk indexed {len(documents)} docs")

    def delete_index(self, index_name):
        if self.client.indices.exists(index=index_name):
            self.client.indices.delete(index=index_name)
            print(f"✅ Deleted index: {index_name}")

    def list_indices(self):
        return list(self.client.indices.get(index="*").keys())