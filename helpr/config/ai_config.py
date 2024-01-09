from pydantic import BaseModel
from helpr.prompt_generator.base import PromptGenerator


class AIConfig(BaseModel):
    api_budget: float = 0.0
    
    def construct_full_prompt(self, prompt_generator: PromptGenerator) -> str:
        prompt_start = (
            "Your decisions must always be made independently without"
            " seeking user assistance. Play to your strengths as an LLM and pursue"
            " simple strategies with no legal complications."
            " When using any tools, you must have all the required parameters, otherwise you must ask the user to retrieve them. Ask yourself if you really have all the parameters to execute the action"
            ""
        )

        # Construct full prompt
        full_prompt = f"You are {prompt_generator.name}, {prompt_generator.role}\n{prompt_start}\n\n"
      
        if self.api_budget > 0.0:
            full_prompt += f"\nIt takes money to let you run. Your API budget is ${self.api_budget:.3f}"
        full_prompt += f"\n\n{prompt_generator.generate_prompt_string()}"
        return full_prompt
