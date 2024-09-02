import pydantic


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str
    user_email: str | None = None
