from core.retriever import RetrievalService
from app.constants.prompt import prompt
from core.generator import generate_answer
from core.embeddings import embed_text
from core.vector_store import client, COLLECTION_NAME
from app.constants.prompt import build_prompt

retriever = RetrievalService(vector_db = client, embedding_service = embed_text, collection_name = COLLECTION_NAME)

def build_context(chunks):
    return "\n\n".join(chunks)

def answer_query(query: str):
    chunks = retriever(query)
    context = build_context(chunks)
    
    prompt = build_prompt(context, query)
    
    answer = generate_answer(prompt)
    return answer