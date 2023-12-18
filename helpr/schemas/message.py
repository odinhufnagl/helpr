from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from helpr.schemas.base import BaseSchema

class MessageSchema(BaseSchema):
    id: int
    text: str
    chat_session_id: int
    created_at: datetime
    updated_at: datetime

class dto:
    class CreateMessage(BaseModel):
        text: str
        chat_session_id: int