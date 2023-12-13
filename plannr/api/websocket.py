import asyncio
from dotenv import load_dotenv
from socketio import AsyncServer, ASGIApp
import socketio
import uvicorn
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db
from services.database import update as db_update
from socket_components.manager import CustomRedisManager
from urllib.parse import parse_qs
load_dotenv()
#TODO: env variables
mgr = CustomRedisManager(url=os.environ['SOCKET_MESSAGE_QUEUE'])
sio = socketio.AsyncServer(client_manager=mgr, logger=True, async_mode='asgi')

app = ASGIApp(sio)
from logger import logger


@sio.event
async def message():
    logger.info("message arrived")

@sio.event
async def connect(sid, environ):
    query_params = parse_qs(environ['QUERY_STRING'])
    auth_token = query_params.get('auth', [None])[0]
    #TODO: this should instead be like user_id = decode_token(auth_token)
    user_id = auth_token  
    await sio.enter_room(sid=sid, room=sid)
    await mgr.save_session(sid, user_id)

@sio.event
async def disconnect(sid):
    logger.info(f"Client {sid} disconnected")
    await sio.leave_room(sid=sid, room=sid)
    await mgr.remove_session(sid)

# You can define more events here for handling different messages

async def start_socketio_server():
   
    await sio.start_background_task(background_task)
    await sio.sleep(0.1)

async def background_task():
    pass
    # Your background tasks (e.g., managing connections) can go here

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
    logger.info("hello worls")
   # asyncio.run(start_socketio_server())