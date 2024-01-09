from dataclasses import dataclass
from datetime import datetime
import string
from typing import Dict, List, Optional
from pydantic import BaseModel
from helpr.db.models.action_request import DBActionRequest, DBActionRequestResponse
from helpr.schemas.action import ActionSchema
from helpr.schemas.action_run import ActionRunSchema

from helpr.schemas.base import BaseSchema

class ActionRequestSchema(BaseSchema):
    id: int
    action_id: int
    action: Optional[ActionSchema]
    input: str
    response_id: int | None
    response: Optional['ActionRequestResponseSchema'] = None
    action_run_id: int | None
    
    def from_model(m: DBActionRequest):
        return ActionRequestSchema(id=m.id, action_id=m.action_id, action=ActionSchema.from_model(m.action) if m.action else None, action_run_id=m.action_run_id, response_id=m.response_id, response=ActionRequestResponseSchema.from_model(m.response) if m.response else None, input=m.input)
 
    
class ActionRequestResponseSchema(BaseSchema):
    id: int
    feedback: str | None
    approved: bool
    next_action_request_id: int | None
    next_action_request: ActionRequestSchema | None
    action_run_id: int | None
    action_run: ActionRunSchema | None 
    
    def from_model(m: DBActionRequestResponse):
        return ActionRequestResponseSchema(id=m.id, feedback=m.feedback, approved=m.approved, next_action_request_id=m.next_action_request_id,action_run_id=m.action_run_id, next_action_request=None, action_run=ActionRunSchema.from_model(m.action_run) if m.action_run else None)
 
    
class dto:
    class CreateActionRequest(BaseModel):
        action_id: int
        input: str
        response_id: int | None
        action_run_id: int | None
        
    class CreateActionResponse(BaseModel):
        feedback: str | None
        approved: bool
        next_action_request_id: int | None
        action_run_id: int | None
        action_request_id: int | None
    