from dotenv import load_dotenv
from pydantic import BaseModel
from tasks import generate_bot_message as task_generate_bot_message
from tasks import run_action as task_run_action
import os

load_dotenv()

class TaskQueue(BaseModel):
  api_url: str
   
  async def push_generate_bot_message(self, chat_session_id: int) -> bool:
    #TODO: update state on the chat_session that message is being created
    task_generate_bot_message.delay(chat_session_id)
    return True
  
  async def push_run_action(self, action_run_id: int, chat_session_id: int) -> bool:
    task_run_action.delay(action_run_id=action_run_id, chat_session_id=chat_session_id)
    return True
  
  
task_queue = TaskQueue(api_url=os.environ['API_URL'])

    
    
    

