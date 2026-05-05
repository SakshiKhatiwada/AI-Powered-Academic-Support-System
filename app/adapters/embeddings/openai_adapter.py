import openai  # type: ignore[import]

from app.adapters.embeddings.base import EmbeddingAdapter


class OpenAIAdapter(EmbeddingAdapter):
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.model = "text-embedding-ada-002"

    async def embed_text(self, text: str) -> list[float]:
        embeddings = await self.embed_texts([text])
        return embeddings[0]

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = await openai.Embedding.acreate(  # type: ignore[attr-defined]
            input=texts, model=self.model
        )
        return [item["embedding"] for item in response["data"]]
