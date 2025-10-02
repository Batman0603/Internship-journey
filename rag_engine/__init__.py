from .vector_store import VectorStore

# Create a single, shared instance of the VectorStore
# to be used across the application.
vector_store = VectorStore()