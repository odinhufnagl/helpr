
from typing import Any, Dict, Type, TypeVar
import requests
from helpr.action.base import BaseAction
from helpr.action.request.credentials import RequestCredentialProvider
from helpr.logger import logger
from helpr.schemas.action import PostRequestActionSchema
import json

T = TypeVar('T')
T2 = TypeVar('T2')


class BaseRequestAction(BaseAction):
    feedback_required: bool = True

    class Creds(BaseAction.Creds):
        request: RequestCredentialProvider.Data
        
    class Fields(BaseAction.Fields):
        url: str
        headers: Dict | None 
        
    fields: Fields
    
    
class PostRequestAction(BaseRequestAction):
    
    class Input(BaseAction.Input):
        data: Any

    class Output(BaseAction.Output):
        json_result: Any
    
    
    async def run(self, data: Any) -> Output: #TODO: fix the input-parameters, should be the input class and then the conversion to tools should fix it
        response = requests.post(self.fields.url, data=data, headers=self.fields.headers) 
        return BaseRequestAction.Output(json_result=response.json())
    
    def empty_run(self, data: Any) -> Output:
        return PostRequestAction.Output()
    
    @classmethod
    def from_schema(cls, schema: PostRequestActionSchema):
        description = f"{schema.description}. The input.data must be in the form: {json.dumps(schema.body_input_struct)}" #TODO: should be centralised somewhere else, ot atleast in another function or class
        logger.info(description)
        return PostRequestAction(id=schema.id, name=schema.name, feedback_required=schema.feedback_required, description=description, fields=BaseRequestAction.Fields(headers=schema.headers, url=schema.url,))