import pydantic


class Person(pydantic.BaseModel):
    email: str
    name: str
