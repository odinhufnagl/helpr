
from re import S
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel
import socketio
from .message import BaseSocketServerMessage
from .manager import CustomRedisManager
import os
from logger import logger
load_dotenv()
class SocketMessageQueue():

    def __init__(self, url):
        self.url = url
        self.external_manager = CustomRedisManager(url=self.url, write_only=True)

        
    async def emit(self, server_msg: BaseSocketServerMessage, user_ids: List[int]):
        for user_id in user_ids:
            sids = await self.external_manager.get_sids(user_id)
            for sid in sids:  
                await self.external_manager.emit(server_msg.get_event(), data=server_msg.get_data(), room=sid)
    
    
socket_message_queue = SocketMessageQueue(url=os.environ['SOCKET_MESSAGE_QUEUE'])

    
    

    