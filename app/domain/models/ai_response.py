import typing
import pydantic


class AIResponse(pydantic.BaseModel):
    response: typing.Dict
