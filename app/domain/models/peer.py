import pydantic

from app.domain.models.person import Person


class Peer(pydantic.BaseModel):
    peer: Person
    question: str
    response: str
