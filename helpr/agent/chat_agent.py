from re import S
from typing import List, Optional
from pydantic import BaseModel
from helpr.index.base import ChatIndex
from llama_index.llms.types import ChatMessage
from helpr.index.location import BaseIndexLocation


class ChatAgent(BaseModel):
    organization_id: int
    index_location: BaseIndexLocation
    index_id: str
    system_prompt: str
    index: Optional[ChatIndex] = None
    chat_history: List[ChatMessage] = []
    
    
    async def get_index(self):
        if not self.index:
            self.index = await ChatIndex.load_from_location(self.index_location, self.index_id)
        return self.index
    
    async def chat(self, input_text: str):
        index = await self.get_index()
        chat_engine = index.as_chat_engine(system_prompt=self.system_prompt)
        response = chat_engine.chat(input_text, chat_history=self.chat_history)
        #TODO: construct chatmessage and return it and add it to history
        
        