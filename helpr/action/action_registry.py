from typing import Dict, List, Optional

from pydantic import BaseModel

from helpr.action.base import AddAction, BaseAction
from helpr.action.request.base import PostRequestAction
from helpr.schemas.action import ActionSchema
from helpr.logger import logger
#TODO: redo with name as key
class ActionRegistry(BaseModel):
    actions: List[BaseAction] = []
    
    #TODO: from_schema functions should be defined in the actions I guess, or in some general place
    def register_schema(self, action_schema: ActionSchema) -> Optional[BaseAction]:
        new_action = None
        logger.info(f"haha, {action_schema.type} {ActionSchema.Type.ADD}")
        if action_schema.type == ActionSchema.Type.ADD:
            logger.info("hahaha")
            new_action = AddAction.from_schema(action_schema)
        if action_schema.type == ActionSchema.Type.POST_REQUEST:
            new_action = PostRequestAction.from_schema(action_schema)
        self.actions.append(new_action)
        return new_action
        
    def get(self, action_name: str) -> Optional[BaseAction]:
        for action in self.actions:
            if action.name == action_name:
                return action
            
