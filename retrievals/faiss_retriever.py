
import faiss
from sentence_transformers import SentenceTransformer

class FaissRetriever:
    def __init__(self, file_path="data/docs.txt", model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.docs = []

        # Load docs
        with open(file_path, "r", encoding="utf-8") as f:
            self.docs = [line.strip() for line in f.readlines() if line.strip()]

        if not self.docs:
            raise ValueError("No documents found in docs.txt!")

        # Embed docs
        embeddings = self.model.encode(self.docs, convert_to_numpy=True)

        # Build FAISS index
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        print(f"FAISS index built with {len(self.docs)} documents")

    def search(self, query, top_k=3):
        if self.index is None:
            raise ValueError("FAISS index not initialized")

        query_vec = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, top_k)
        return [self.docs[i] for i in indices[0]]
