from abc import ABC, abstractmethod
from typing import Any, List, Optional
from pydantic import BaseModel
from requests import request
import requests
from sqlalchemy import desc, select
from sqlalchemy.orm import selectinload
from helpr import db
from logger import logger
from llama_index.tools import FunctionTool

from helpr.schemas.action import ActionSchema


class BaseAction(BaseModel, ABC):
    id: int
    name: str 
    description: str
    feedback_required: bool = False

    class Config:
        arbitrary_types_allowed = True

    class Input(BaseModel):
        pass

    class Output(BaseModel):
        pass

    class Creds(BaseModel):
        pass
    
    class Fields(BaseModel):
        pass
    
    fields: Fields = Fields()
    
    
    creds: Creds = Creds()
    
    #TODO: get_credentials

    def run(self, input: Input) -> Output:
        pass

    @staticmethod
    def empty_run() -> Output:
        return BaseAction.Output()

    @staticmethod
    def from_schema(schema: ActionSchema):
        if schema.type == ActionSchema.Type.ADD:
            logger.info(f"{schema.name}, {schema.description}, {schema.feedback_required}")
            return AddAction(id=schema.id, name=schema.name, description=schema.description, feedback_required=schema.feedback_required)
    def to_tool(self):
        return (self.run, self.empty_run, self.name, self.description)


# These are actions that the companies should be able to add so they have to be very prototyped

class PrintAction(BaseAction):
    name: str = "log"
    description: str = "This will print the input to the terminal"
    feedback_required: bool = True

    class Input(BaseAction.Input):
        text: str

    class Output(BaseAction.Output):
        success: bool

    def run(self, text: str) -> Output:
        print(text)
        return self.Output(success=True)

    @staticmethod
    def empty_run(text: str) -> Output:
        return BaseAction.Output()


class AddAction(BaseAction):
    name: str = "add"
    description: str = "This will add two numbers"
    feedback_required: bool = False

    class Input(BaseAction.Input):
        a: int
        b: int

    class Output(BaseAction.Output):
        c: int

    def run(self, a: int, b: int) -> Output:
        return self.Output(c=a + b)

