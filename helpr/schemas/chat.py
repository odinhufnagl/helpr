from dataclasses import dataclass
from datetime import datetime
from re import S
from typing import List, Optional
from pydantic import BaseModel

from helpr.schemas.base import BaseSchema

class ChatSchema(BaseSchema):
    id: int
    agent_id: int
    organization_id: int
    name: str
    created_at: datetime
    updated_at: datetime
   
   
class dto:
    class CreateChat(BaseModel):
        agent_id: int
        organization_id: int
        name: str
        system_prompt: str