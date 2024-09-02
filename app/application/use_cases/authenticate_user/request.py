import pydantic


class AuthenticaeUserRequest(pydantic.BaseModel):
    email: str
    password: str
    hashed_password: str
