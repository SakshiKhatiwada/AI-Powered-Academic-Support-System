from typing import Any

from pydantic import BaseModel

class DocumentIngestRequest(BaseModel):
    document_id: str
    content: str
    metadata: dict[str, Any] | None = None
    
class BatchDocumentIngestRequest(BaseModel):
    documents: list[DocumentIngestRequest]
    
class DocumentIngestResponse(BaseModel):
    status: str
    document_id: str