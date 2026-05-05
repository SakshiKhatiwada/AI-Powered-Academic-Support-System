from functools import lru_cache

from app.adapters.embeddings.base import EmbeddingAdapter
from app.adapters.embeddings.openai_adapter import OpenAIAdapter
from app.adapters.embeddings.sentence_transformer import (
    SentenceTransformersAdapter,
)
from app.adapters.llm.base import LLMAdapter
from app.adapters.llm.gemini_adapter import GeminiAdapter
from app.adapters.llm.local_adapter import LocalAdapter
from app.adapters.vector_db.base import VectorDBAdapter
from app.adapters.vector_db.qdrant_adapter import QdrantAdapter
from app.config import get_settings

settings = get_settings()

@lru_cache
def get_vector_db() -> VectorDBAdapter:
    return QdrantAdapter(
        url=settings.qdrant_url or "http://localhost:6333",
        vector_size=settings.embedding_dimension,
    )

@lru_cache
def get_embedding_service() -> EmbeddingAdapter:
    if settings.embedding_provider == "sentence_transformers":
        return SentenceTransformersAdapter(model_name=settings.embedding_model)
    elif settings.embedding_provider == "openai":
        api_key = settings.openai_api_key
        if not api_key:
            raise ValueError("OpenAI API key is required for the selected provider.")
        return OpenAIAdapter(api_key=api_key.get_secret_value())
    else:
        raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")


@lru_cache
def get_llm_service() -> LLMAdapter:
    if settings.llm_provider == "gemini":
        api_key = settings.gemini_api_key
        if not api_key:
            raise ValueError("Gemini API key is required for remote LLMs.")
        return GeminiAdapter(api_key=api_key.get_secret_value())
    elif settings.llm_provider == "local":
        model_name = settings.local_llm_model
        if not model_name:
            raise ValueError("Local LLM model name must be configured.")
        return LocalAdapter(model_name=model_name)
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
