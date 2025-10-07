from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.text_chunks = []

    def add_texts(self, texts):
        embeddings = self.model.encode(texts)
        embeddings = np.array(embeddings).astype("float32")
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.text_chunks.extend(texts)

    def search(self, query, k=3):
        q_emb = self.model.encode([query]).astype("float32")
        D, I = self.index.search(q_emb, k)
        return [self.text_chunks[i] for i in I[0]]
