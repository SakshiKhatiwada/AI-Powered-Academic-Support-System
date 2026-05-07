from functools import lru_cache

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    
    # vector db
    qdrant_url: str | None = None
    
    # embeddings
    embedding_provider: str = "sentence_transformers"
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # llm
    llm_provider: str = "gemini"
    gemini_api_key: SecretStr | None = None
    openai_api_key: SecretStr | None = None
    local_llm_model: str | None = None
    
    # chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # retrieval
    top_k : int = 5
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # validators
    @field_validator("chunk_overlap")
    @classmethod
    def validate_chunk_overlap(cls, v, info):
        if v >= info.data['chunk_size']:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        return v
    
@lru_cache
def get_settings() -> Settings:
    return Settings() #type: ignore[call-arg]