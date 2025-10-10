import os
from utils.file_utils import extract_text_from_file

def ingest_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    return extract_text_from_file(file_path)
