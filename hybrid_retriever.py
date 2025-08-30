
from retrievals.faiss_retriever import FaissRetriever
from retrievals.elasticsearch_retriever import ElasticsearchRetriever

class HybridRetriever:
    def __init__(self, es_endpoint, es_api_key, faiss_model="sentence-transformers/all-MiniLM-L6-v2"):
        # Initialize FAISS retriever and index docs
        self.faiss_retriever = FaissRetriever(file_path="data/docs.txt", model_name=faiss_model)
        
        # Initialize Elasticsearch retriever and index docs
        self.es_retriever = ElasticsearchRetriever(es_endpoint, es_api_key)
        self.es_retriever.index_docs("data/docs.txt")  # ensure docs are indexed
        print("Elastic indexing done")

    def search(self, query, top_k=3):
        es_results = self.es_retriever.search(query, top_k=top_k)
        faiss_results = self.faiss_retriever.search(query, top_k=top_k)

        return {
            "elasticsearch": es_results,
            "faiss": faiss_results
        }
