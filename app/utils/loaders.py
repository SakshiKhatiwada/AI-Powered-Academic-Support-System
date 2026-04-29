from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file: UploadFile) -> list[str]:
    """
    Load PDF from FastAPI UploadFile using LangChain's PyPDFLoader
    
    Returns:
        List of Page texts (One string per Page)
    """
    
    if file.content_type != "application/pdf":
        raise ValueError("Only PDF files are supported")
    
    import tempfile
    
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp_file:
        tmp_file.write(file.file.read())
        tmp_file.flush()
        
        try:
            loader = PyPDFLoader(tmp_file.name)
            docs = loader.load()
        except Exception as e:
            raise ValueError(f"PDF parsing failed (possible bbox error): {e}") # Somehow your font is corrupt, and there is incorrect data in one or more of these bounding boxes (or /BBox) data structures.
        
    page_texts = [doc.page_content for doc in docs]
    return page_texts