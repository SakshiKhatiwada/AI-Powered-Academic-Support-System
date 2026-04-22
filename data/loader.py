from pypdf import PdfReader

def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    
    print("reader: ", reader)
    for page in reader.pages:
        text = page.extract_text() + "\n"
        
    return text