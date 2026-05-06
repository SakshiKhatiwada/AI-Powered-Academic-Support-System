import json
from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.schemas.ingestion import DocumentIngestResponse
from app.services.ingestion_service import IngestionService
from app.utils.validators import validate_pdf

from app.dependencies import get_embedding_service, get_vector_db
from app.config import get_settings

settings = get_settings()
router = APIRouter()

@router.post("ingest-documents", response_model=DocumentIngestResponse)
async def ingest_document(
    subject_id: str | None = Form(default=None, description="Unique ID for the Subject"),
    document_id: str = Form(..., description="Unique ID for the document"),
    file: UploadFile = File(..., description="File to ingest"),
    metadata: str | None = Form(None),
    vector_db=Depends(get_vector_db),
    embedding_service=Depends(get_embedding_service),
):
    
    # Validate if file is PDF
    await validate_pdf(file)

    metadata_dict: dict[str, Any] = {}
    if metadata:
        try:
            metadata_dict = json.loads(metadata)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="metadata must be valid JSON")

    service = IngestionService(
        vector_db, embedding_service, settings.chunk_size, settings.chunk_overlap
    )
    try:
        collection_name = f"subject_{subject_id}" if subject_id else "default_documents"
        await service.ingest_document(document_id, file, metadata_dict, collection_name)
        return {"status": "success", "document_id": document_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
