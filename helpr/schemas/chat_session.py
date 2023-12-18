from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from helpr.schemas.base import BaseSchema
from helpr.schemas.message import MessageSchema

class ChatSessionSchema(BaseSchema):
    id: int
    chat_id: int
    created_at: datetime
    updated_at: datetime
    messages: Optional[List[MessageSchema]] = None
   