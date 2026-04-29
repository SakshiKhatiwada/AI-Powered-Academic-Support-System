from typing import Any
class RetrievalService:
    
    def __init__(self,vector_db, embedding_service, collection_name):
        self.vector_db = vector_db
        self.embedding_service = embedding_service
        self.collection_name = collection_name
        
    async def retrieve_context(
        self, 
        query: str, 
        top_k : int,
        filters : dict[str, Any]
    ) -> list[dict]:
        """Performs Retrieval"""    
        
        if not query:
            raise ValueError("Retrieval Query can't be empty")     
        
        query_embedding = await self.embedding_service(query) # func for now
        
        results = await self.vector_db.search_similar(
            query_embedding = query_embedding,
            top_k = top_k,
            collection_name = self.collection_name,
            filters = filters
        )
        
        if not results:
            return []
        
        return results