from fastapi import UploadFile
from typing import Any
import uuid

from app.utils.loaders import load_pdf
from app.utils.chunking import chunk_text

from qdrant_client.http.models import PointStruct

class IngestionService:
    
    def __init__(
        self, 
        vector_db, 
        embedding_service, 
        chunk_size, 
        chunk_overlap, 
        chunk_method
    ):
        self.vector_db = vector_db
        self.embedding_service = embedding_service
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunk_method = chunk_method
        
    async def ingest_document(
        self, document_id: str, file: UploadFile, metadata: dict[str, Any] | None = None
    ):
        
        # delete old vectors
        await self.delete_existing_syllabus(document_id)
        
        # load pdf
        try:
            pages = load_pdf(file) # returns list of string
            full_text = "\n".join(pages)
        except Exception as e:
            raise RuntimeError("Error loading PDF") from e # error chaining, preserves the original error
        
        # split text into chunks
        chunks = chunk_text(
            full_text,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            chunk_method=self.chunk_method,    
            return_metadata=True,
            document_id=document_id
        )
        
        # generate embeddings in parallel and store in batches
        EMBED_BATCH_SIZE = 32 # for CPU, 32 chunks at a time for embeddings
        UPSERT_BATCH_SIZE = 64 # for network,64 vectors at once to db
        points_buffer: list[PointStruct] = [] # buffer to hold before bulk inserting to database
        
        await self.vector_db.ensure_collection()
        
        for i in range(0, len(chunks), EMBED_BATCH_SIZE): # takes a batch
            batch_chunks = chunks[i : i + EMBED_BATCH_SIZE]
            texts = [c["text"] for c in batch_chunks]
            
            embeddings = await self.embedding_service.embed_texts(texts)
            
            for chunk, embedding in zip(batch_chunks, embeddings, strict=True): # processes all members of the current batch one by one
                # strictness True will raise ValueError if one data exhaust before another
                chunk_id = f"{uuid.uuid4()}"
                payload={
                    "document_id": document_id,
                    "chunk_index": chunk["chunk_index"],
                    "content": chunk["text"],
                    **(metadata or {})
                }
                
                points_buffer.append(
                    PointStruct(
                        id = chunk_id,
                        payload = payload,
                        vector = embedding
                    )
                )
                
            if len(points_buffer) > UPSERT_BATCH_SIZE: # upserts in bulk
                await self.vector_db.upsert_points(points_buffer)
                points_buffer.clear()
        
        if points_buffer: # upserts everything that remains at the last
            await self.vector_db.upsert_points(points_buffer)
                
        
    async def delete_existing_syllabus(self, document_id: str):
        """
        Delete all the vectors associated with the given document_id from the vector database """
        await self.vector_db.delete_by_document_id(document_id)