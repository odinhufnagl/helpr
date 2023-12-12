import json
from typing import List
import redis
from redis.asyncio.client import Redis
from socketio import RedisManager, AsyncRedisManager
from logger import logger
#TODO: edit name
class CustomRedisManager(AsyncRedisManager):
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)
        self.redis = Redis.from_url(f"{url}/{0}")
        self.redis2 = Redis.from_url(f"{url}/{1}", decode_responses=True)
   
    #TODO: all these functions should probably be looked at, should be better alternatives for the mapping
    async def get_session(self, sid):
        user_id = await self.redis2.hget('sid_uid_sessions', sid)
        return json.loads(user_id) if user_id else {}

    async def save_session(self, sid, user_id):
        prev_sids = (await self.redis2.hget('uid_sids_sessions', user_id))
        if prev_sids:
            prev_sids = json.loads(prev_sids)
        else:
            prev_sids = []
            
        await self.redis2.hset('uid_sids_sessions', user_id, json.dumps(prev_sids + [sid]))
        await self.redis2.hset('sid_uid_sessions', sid, json.dumps(user_id))
        
    async def remove_session(self, sid):
        user_id = await self.redis2.hget('sid_uid_sessions', sid)
        if not user_id:
            return
        user_id = json.loads(user_id)
        await self.redis2.hdel('sid_uid_sessions', sid)
        prev_sids = json.loads(await self.redis2.hget('uid_sids_sessions', user_id))
        await self.redis2.hset('uid_sids_sessions', sid, json.dumps([x for x in prev_sids if x != sid]))

    async def get_sids(self, user_id: int) -> List[str]:
        sessions = await self.redis2.hget('uid_sids_sessions', user_id)
        if not sessions:
            return []
        sessions = json.loads(sessions)
        return sessions
    
  