import os

def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from a given file based on its extension.
    Currently supports .txt files.
    """
    _, extension = os.path.splitext(file_path)

    if extension.lower() == ".txt":
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
            
    # Example for PDF (requires `pip install PyPDF2`):
    # elif extension.lower() == ".pdf":
    #     import PyPDF2
    #     text = ""
    #     with open(file_path, 'rb') as f:
    #         reader = PyPDF2.PdfReader(f)
    #         for page in reader.pages:
    #             text += page.extract_text() or ""
    #     return text

    else:
        # For simplicity, we'll raise an error for unsupported types.
        # You could also try reading it as a plain text file as a fallback.
        raise ValueError(f"Unsupported file type: {extension}. Please upload a .txt file.")