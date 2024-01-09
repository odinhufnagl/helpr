from dataclasses import dataclass
from datetime import datetime
import string
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel
from helpr.db.models.action_run import DBActionRun
from helpr.schemas.action import ActionSchema

from helpr.schemas.base import BaseSchema


ActionRunStatus = Literal["created", "running", "finished", "error"]

class ActionRunSchema(BaseSchema):
    id: int
    credentials: Dict | None
    action_id: int
    action: Optional[ActionSchema]
    input: str
    output: str | None
    status: ActionRunStatus
    
    
    def from_model(m: DBActionRun):
        return ActionRunSchema(id=m.id, action_id=m.action_id, action=ActionSchema.from_model(m.action) if m.action else None, input=m.input, output=m.output, status=m.status, credentials=None)

class dto:
    class CreateActionRun(BaseModel):
        action_id: int
        input: str
        output: str | None
        status: str = "created"