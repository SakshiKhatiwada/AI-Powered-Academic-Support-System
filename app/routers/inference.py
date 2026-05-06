from fastapi import APIRouter, Depends, HTTPException

from app.schemas.inference import GenerateNotesRequest, QueryResponse
from app.services.generation_service import GenerationService
from app.services.retrieval_service import RetrievalService

from app.dependencies import get_embedding_service, get_llm_service, get_vector_db
from app.config import get_settings

settings = get_settings()

router = APIRouter()

async def prepare_retrieval_context(chapter_context: GenerateNotesRequest):
    topic_names = ", ".join(str(topic) for topic in chapter_context.topics[:4] if topic)

    retrieval_query = (
        f"{chapter_context.chapter} {topic_names} in {chapter_context.subject}"
        if topic_names
        else f"{chapter_context.chapter} in {chapter_context.subject}"
    )

    filters = {}
    if chapter_context.document_id:
        filters["document_id"] = chapter_context.document_id
    elif chapter_context.subject:
        filters["subject"] = chapter_context.subject

    return retrieval_query, filters

@router.post("/generate-notes", response_model=QueryResponse)
async def generate_topic_notes(
    request: GenerateNotesRequest,
    vector_db=Depends(get_vector_db),
    embedding_service=Depends(get_embedding_service),
    llm_service=Depends(get_llm_service),
):
    collection_name = f"subject_{request.subject_id}" if request.subject_id else "default_documents"

    retrieval_service = RetrievalService(vector_db, embedding_service, collection_name)
    generation_service = GenerationService(llm_service)
    
    try:
        retrieval_query, filters = await prepare_retrieval_context(request)
        sources = await retrieval_service.retrieve(
            query=retrieval_query,
            top_k=settings.top_k,
            filters=filters,
        )

        answer = await generation_service.generate_notes(request, sources)
        return QueryResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))