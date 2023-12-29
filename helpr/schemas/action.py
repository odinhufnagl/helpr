from dataclasses import dataclass
from datetime import datetime
import string
from typing import Any, Dict, List, Literal, Optional, Union
from click import Option
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column

from helpr.db.models.action import DBAction, DBAddAction, DBPostRequestAction
from helpr.logger import logger
from helpr.schemas.base import BaseSchema
    
    
#TODO: we need to add convertion from the stored "types" in db and it maybe could be put here, or perhaps in some better way
#we probably create a dbclass called Type or something and then we also have a schema for it and then it can have a converter there maybe. Or actually just maybe a utils function is better
    
class ActionSchema(BaseSchema):
    class Type:
        ADD = 'add'
        MULTIPLY = 'multiply'
        POST_REQUEST = 'post_request' 
    id: int
    type: Union[str, Type]
    name: str
    description: str
    is_public: bool
    feedback_required: bool
    
    class Config:
        arbitrary_types_allowed = True
        
    def from_model(model: DBAction):
    
        if model.type == DBAction.Type.POST_REQUEST:
            return PostRequestActionSchema.from_model(model)
        if model.type == DBAction.Type.ADD:
            return AddActionSchema.from_model(model)
   
class AddActionSchema(ActionSchema):
    def from_model(m: DBAddAction):
        return AddActionSchema(id=m.id, type=m.type, name=m.name, description=m.description, is_public=m.is_public, feedback_required=m.feedback_required)     
        

class PostRequestActionSchema(ActionSchema):
    url: str
    headers: Dict
    body_input_struct: Dict | None
    result_output_struct: Dict | None
  #  fields: Optional[List[ActionFieldSchema]]
    
   # def from_model(m: DBAction):
   #    return ActionSchema(id=m.id, type=m.type, name=m.name, description=m.description, is_public=m.is_public, input_described=m.input_described, output_described=m.output_described, feedback_required=m.feedback_required, fields=list(map(lambda f: ActionFieldSchema.from_model(f), m.fields)))
    
    def from_model(m: DBPostRequestAction):
       url = m.url_field.get_value()
       headers = m.headers_field.get_value()
       logger.info(f"whyyy: {m.__dict__}, {m.id}, {type(m.url_field.get_value())}, {type(m.headers_field.get_value())}, {type(m.body_input_struct)}, {type(m.result_output_struct)}")
       return PostRequestActionSchema(id=m.id, type=m.type, name=m.name, description=m.description, is_public=m.is_public, feedback_required=m.feedback_required,url=url, body_input_struct=m.body_input_struct, result_output_struct=m.result_output_struct, headers=headers)