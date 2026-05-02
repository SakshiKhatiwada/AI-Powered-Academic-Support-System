from abc import ABC, abstractmethod

class EmbeddingAdapter(ABC):
    
    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        pass

    @abstractmethod
    def embed_texts(self, text: list[str]) -> list[list[float]]:
        pass