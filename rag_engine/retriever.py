from rag_engine import vector_store # Import the shared instance

def retrieve_context(query: str, k: int = 3):
    return vector_store.search(query, k)
