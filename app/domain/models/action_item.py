import pydantic


class ActionItem(pydantic.BaseModel):
    id: int
    action_plan: str
    resources: str
