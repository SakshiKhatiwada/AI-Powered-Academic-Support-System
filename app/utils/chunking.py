from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter

def chunk_text(
    content: str,
    chunk_size: int,
    chunk_overlap: int,
    return_metadata: bool = False,
    chunk_method: str = "recursive",
    document_id: str | None = None,
    ) -> list:
    
    """
    Splits text into chunks using LangChain Splitters.
    
    Args:
    content (str): the full text to be chunked/splitted.
    chunk_size (int): max size of the chunks.
    chunk_overlap (int): overlap between the chunks.
    return_metadata (bool): If True, returns list of dict of metadata
    method (str): "recursive" or "character" splitter
    document_id (str): Optional syllabus/document ID to include in metadata  
    """
    
    splitter: CharacterTextSplitter | RecursiveCharacterTextSplitter
    
    if chunk_method == "recursive":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            length_function = len,
            strip_whitespace = True
        )
        
    elif chunk_method == "character":
        splitter = CharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            separator='\n',
            length_function = len,
            strip_whitespace = True
        )
        
    else:
        raise ValueError("Choose either 'recursive' or 'character'!")
    
    # docs = splitter.create_documents([content]) # chunks as document
    chunks = splitter.split_text(content) # chunks as text
    
    if return_metadata:
        return [
            {
                "chunk_index": i,
                "text": chunk,
                **({"syllabus_uuid": document_id} if document_id else {})
                
            }
            for i, chunk in enumerate(chunks)
        ]
    return chunks
