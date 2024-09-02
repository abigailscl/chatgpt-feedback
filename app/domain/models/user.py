import pydantic

from app.domain.models.person import Person


class User(pydantic.BaseModel):
    user: Person
    hashed_password: str
