"""
Elasticsearch Retriever
-----------------------
Connects to Elasticsearch using endpoint + API key and indexes docs if needed.
"""

from elasticsearch import Elasticsearch

class ElasticsearchRetriever:
    def __init__(self, endpoint: str, api_key: str, index_name: str = "documents"):
        self.client = Elasticsearch(endpoint, api_key=api_key, verify_certs=True)
        self.index_name = index_name

    def index_docs(self, file_path="data/docs.txt"):
        # Only create index if it does not exist
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(
                index=self.index_name,
                body={
                    "mappings": {
                        "properties": {
                            "content": {"type": "text"}
                        }
                    }
                }
            )
            print(f"Index '{self.index_name}' created")
        else:
            print(f"Index '{self.index_name}' already exists")

        # Read docs and index
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        for i, doc in enumerate(lines):
            self.client.index(index=self.index_name, id=i, document={"content": doc})

        print(f"Indexed {len(lines)} docs into '{self.index_name}'")


    def search(self, query, top_k=3):
        """Full-text search using Elasticsearch"""
        response = self.client.search(
            index=self.index_name,
            body={
                "size": top_k,
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["content"]
                    }
                }
            }
        )
        hits = response["hits"]["hits"]
        return [hit["_source"]["content"] for hit in hits]
