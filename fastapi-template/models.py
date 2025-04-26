from typing import Optional
from pydantic import BaseModel


class MsgPayload(BaseModel):
    msg_id: Optional[int]
    msg_name: str


class CropRequest(BaseModel):
    x: int
    y: int
    width: int
    height: int
