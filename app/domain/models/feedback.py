from typing import Optional
import typing
import pydantic

from app.domain.models.user import User
from app.domain.models.action_item import ActionItem
from app.domain.models.peer import Peer


class Feedback(pydantic.BaseModel):
    id: Optional[int]
    user: User
    peers: typing.List[Peer]
    action_item: Optional[ActionItem]
