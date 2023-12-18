
from abc import ABC
from re import S
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel
from redis import Redis
import socketio
from .message import BaseSocketServerMessage
from .manager import CustomRedisManager
import os
from logger import logger
load_dotenv()



class BaseSocketMessageQueue(ABC):
    external_redis: Redis
    
class SocketMessageQueue():

    def __init__(self, url):
        self.url = url
        self.external_manager = CustomRedisManager(url=self.url, write_only=True)

  
    async def emit(self, server_msg: BaseSocketServerMessage, sids: List[str]):
            for sid in sids:  
                await self.external_manager.emit(server_msg.get_event(), data=server_msg.get_data(), room=sid)
                
    #TODO: pretty ugly and repetitive, the problem is probably connected to how we structure CustomRedisManager different session-lookups
    async def emit_to_client(self, server_msg: BaseSocketServerMessage, clients: List[str]):
            for client in clients:
                sids = await self.external_manager.get_client_sids(client)
                await self.emit(server_msg, sids)
                
    async def emit_to_uid(self, server_msg: BaseSocketServerMessage, uids: List[str]):
            for uid in uids:
                sids = await self.external_manager.get_uid_sids(uid)
                await self.emit(server_msg, sids)
                
    
    
socket_message_queue = SocketMessageQueue(url=os.environ['SOCKET_MESSAGE_QUEUE'])

    
    

    