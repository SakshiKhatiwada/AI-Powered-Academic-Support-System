import uuid
from collections.abc import Sequence
from typing import Any

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams
from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.adapters.vector_db.base import VectorDBAdapter

class QdrantAdapter(VectorDBAdapter):
    
    def __init__(self, url: str = "http://localhost:6333", vector_size: int=384):
        self.client = AsyncQdrantClient(url=url)
        self.collection_name = "documents"
        self.vector_size = vector_size
        self._collection_ready = False
        
    async def ensure_collection(self) -> None:
        if self._collection_ready:
            return
        
        collections = await self.client.get_collections()
        existing = {collection.name for collection in collections.collections} # set comprehension
        
        if self.collection_name not in existing:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size = self.vector_size,
                    distance=Distance.COSINE
                )
            )
        self._collection_ready = True
        
    async def store_embedding(self, id: str, embedding: list[float], metadata: dict[str, Any]):
         await self.ensure_collection()
         point=PointStruct(
             id = str(uuid.uuid4()),
             vector=embedding,
             payload={**metadata, "document_id":id}
         )
         await self.client.upsert(
             collection_name=self.collection_name,
             points=list(point)
         )
        
    async def upsert_points(self, points: Sequence[Any]) -> None:
        await self.ensure_collection()
        await self.client.upsert(
            collection_name=self.collection_name,
            points=list(points)
        )
        
    async def search_similar(
        self,
        query_embedding: list[float],
        top_k: int,
        filters: dict[str,Any] | None = None
        ) -> list[dict[str,Any]]:
        await self.ensure_collection()
        
        qdrant_filter = None
        
        # build conditional filter
        if filters:
            conditions: list[FieldCondition] = []
            for key,value in filters.items():
                if value is None:
                    continue
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            
            if conditions:
                qdrant_filter = Filter(must=list(conditions))
                
            results = await self.client.search(
                collection_name = self.collection_name,
                query_vector = query_embedding,
                limit=top_k,
                query_filter = qdrant_filter
            ) # type: ignore[attr-defined]
            
            return[
                {
                    "id": hit.id,
                    "score": hit.score,
                    "content": hit.payload.get("content") if hit.payload else None,
                    "metadata": hit.payload
                }
                for hit in results
            ]
            
    
    async def delete_by_document_id(self, document_id:str):
        await self.ensure_collection()
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id)
                )]
            )
        )