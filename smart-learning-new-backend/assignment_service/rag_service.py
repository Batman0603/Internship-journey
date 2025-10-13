from rag_engine.retriever import retrieve_context
from rag_engine.generator import generate_mcq, generate_descriptive
from rag_engine import vector_store # Import the shared instance
from utils.file_utils import extract_text_from_file

def process_teacher_notes(file_path: str):
    text = extract_text_from_file(file_path)
    chunks = text.split(". ")
    vector_store.add_texts(chunks)
    return {"status": "Processed", "chunks_added": len(chunks)}

def create_assignment_with_rag(query: str, mode="mcq", num_q=5):
    context = retrieve_context(query, k=3)
    joined_context = " ".join(context)

    if mode == "mcq":
        return generate_mcq(joined_context, num_q)
    else:
        return generate_descriptive(joined_context, num_q)
