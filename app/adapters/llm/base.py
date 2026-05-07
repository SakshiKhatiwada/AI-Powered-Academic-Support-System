from abc import ABC, abstractmethod

class LLMAdapter(ABC):
    @abstractmethod
    def generate_text(
        self, 
        prompt : str,
        temperature : float,
        max_tokens :int 
    ) -> str:
        pass