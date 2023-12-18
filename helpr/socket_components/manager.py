import json
from typing import ClassVar, List
from pydantic import BaseModel
import redis
from redis.asyncio.client import Redis
from socketio import RedisManager, AsyncRedisManager
from logger import logger
#TODO: edit name
class CustomRedisManager(AsyncRedisManager):
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)
        #TODO: these should just share same pool instead right?
        self.redis = Redis.from_url(f"{url}/{0}")
        self.redis_websocket_userid = RedisWebSocket.from_url(f"{url}/{1}", decode_responses=True)
        self.redis_websocket_client = RedisWebSocket.from_url(f"{url}/{2}", decode_responses=True)    
        
    async def save_uid_session(self, sid: str, uid: int):
        await self.redis_websocket_userid.save_session(sid, uid)
    async def save_client_session(self, sid: str, client: str):
        await self.redis_websocket_client.save_session(sid, client)
    async def remove_uid_session(self, sid: str):
        await self.redis_websocket_userid.remove_session(sid)
    async def remove_client_session(self, sid: str):
        await self.redis_websocket_client.remove_session(sid)
    async def remove_session(self, sid: str):
        await self.remove_uid_session(sid)
        await self.remove_client_session(sid)
    async def get_client_session(self, sid: str):
        return await self.redis_websocket_client.get_session(sid)
    async def get_uid_session(self, sid: str):
        return await self.redis_websocket_userid.get_session(sid)
    async def get_client_sids(self, client: str):
        return await self.redis_websocket_client.get_sids(client)
    async def get_uid_sids(self, uid: int):
        return await self.redis_websocket_userid.get_sids(uid)
    

  
  
class RedisWebSocket(Redis):
    sid_key_sessions = "sid_key_sessions"
    key_sids_sessions = "key_sids_sessions"
    
    async def get_session(self, sid: str):
        val = await self.hget(self.sid_key_sessions, sid)
        return json.loads(val) if val else {}
    
    async def save_session(self, sid: str, key: str):
        prev_sids = (await self.hget(self.key_sids_sessions, key))
        if prev_sids:
            prev_sids = json.loads(prev_sids)
        else:
            prev_sids = []
            
        await self.hset(self.key_sids_sessions, key, json.dumps(prev_sids + [sid]))
        await self.hset(self.sid_key_sessions, sid, json.dumps(key))
        
    async def remove_session(self, sid: str):
        val = await self.hget(self.sid_key_sessions, sid)
        if not val:
            return
        val = json.loads(val)
        await self.hdel(self.sid_key_sessions, sid)
        prev_sids = json.loads(await self.hget(self.key_sids_sessions, val))
        await self.hset(self.key_sids_sessions, sid, json.dumps([x for x in prev_sids if x != sid]))
        
    async def get_sids(self, key: str) -> List[str]:
        sessions = await self.hget(self.key_sids_sessions, key)
        if not sessions:
            return []
        sessions = json.loads(sessions)
        return sessions
    
    

    
    