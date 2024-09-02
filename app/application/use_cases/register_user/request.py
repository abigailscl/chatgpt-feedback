import pydantic


class RegisterUserRequest(pydantic.BaseModel):
    name: str
    email: str
    password: str
