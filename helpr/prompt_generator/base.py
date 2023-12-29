from typing import Any, Callable, List, Optional
from pydantic import BaseModel
import json

from helpr.action.action_registry import ActionRegistry
from helpr.action.base import BaseAction




class PromptGenerator(BaseModel):
    constraints: List[str] = []
    context: Optional[str] = None
    action_registry: ActionRegistry = None
    resources: List[str] = []
    performance_evaluation: List[str] = []
    name: str = "Bob"
    role: str = "AI"
   
    
   
      

    
    def set_context(self, context: str):
        # Tell the AI about what its main job is and who it is
        self.context = context
        
    def add_performance_evaluation(self, evaluation: str) -> None:
        self.performance_evaluation.append(evaluation)
      
        
    def _generate_numbered_list(self, items: List[Any], item_type="list") -> str:

        if item_type == "action":
            action_strings = []
            action_strings += [self._generate_action_string(item) for item in items]
            return "\n".join(f"{i+1}. {item}" for i, item in enumerate(action_strings))
        else:
            return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))
        
    def _generate_action_string(self, action: BaseAction) -> str:
  
        args = {field_name: field_type.__name__ for field_name, field_type in action.Input.__annotations__.items()}
        return f'{action.name}: "{action.description}", args: {args}'
   
    def generate_prompt_string(self) -> str:

       
        return (
            f"Constraints:\n{self._generate_numbered_list(self.constraints)}\n\n"
            f"Resources:\n{self._generate_numbered_list(self.resources)}\n\n"
            "Performance Evaluation:\n"
            f"{self._generate_numbered_list(self.performance_evaluation)}\n\n"
          
        )
   