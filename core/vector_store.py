from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# persistent storage
client = QdrantClient(path="qdrant_db")

COLLECTION_NAME = "academic_data"

def create_collection(vector_size : int):
    client.create_collection(
        collection_name= COLLECTION_NAME,
        vectors_config= VectorParams(size=vector_size, distance = Distance.COSINE)
    )
    
def insert_chunks(docs, embeddings):
    points = []
    
    for i, (doc,vector) in enumerate(zip(docs,embeddings)):
        points.append({
            "id": i,
            "vector": vector,
            "payload": {
                "text": doc.page_content, 
                "metadata": doc.metadata},
        })
        
    client.upsert(collection_name=COLLECTION_NAME, points=points)