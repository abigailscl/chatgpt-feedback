from abc import ABC, abstractmethod

from app.domain.models.ai_response import AIResponse


class AIRepository(ABC):
    @abstractmethod
    def response_json(self, prompt: str) -> AIResponse:
        pass
