from abc import ABC, abstractmethod

from app.domain.models.feedback import Feedback


_PROMPT = "Este es un prompt"


class FeedbackRepository(ABC):
    @abstractmethod
    def save(self, feedback: Feedback) -> Feedback:
        pass

    @abstractmethod
    def get(self):
        pass
