import asyncio
from copy import deepcopy
import datetime
from dotenv import load_dotenv
import fastapi
import flask
from socketio import AsyncServer, ASGIApp
import socketio
import sqlalchemy
import uvicorn
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db
from services.database import update as db_update
from socket_components.manager import CustomRedisManager
from urllib.parse import parse_qs
from api.jwt_auth import jwt_auth
import json
load_dotenv()
#TODO: env variables
mgr = CustomRedisManager(url=os.environ['SOCKET_MESSAGE_QUEUE'])



sio = socketio.AsyncServer(client_manager=mgr, logger=True, async_mode='asgi', cors_allowed_origins="*", engineio_logger=True,json=flask.json )

app = ASGIApp(sio)
from logger import logger


@sio.event
async def message():
    logger.info("message arrived")

@sio.event
async def connect(sid, environ, _):
    query_params = parse_qs(environ['QUERY_STRING'])
    logger.info(f"sid: {sid}")
    logger.info(f"environ: {environ}")
    auth_token = query_params.get('auth', [None])[0]
    value = jwt_auth.decode(auth_token)
    logger.info(auth_token)
    logger.info(f"value: {value}")
    if isinstance(value, dict) and value.get('user_id'):
        user_id = int(value.get('user_id'))
        await connect_uid(sid, user_id)
        await sio.enter_room(sid=sid, room=sid)
    elif isinstance(value, dict) and value.get('chat_session_id'):
        client = int(value.get('chat_session_id'))
        await connect_client(sid, client)
        await sio.enter_room(sid=sid, room=sid)
    else:
        await disconnect(sid)

async def connect_uid(sid, uid: int):
    await mgr.save_uid_session(sid, uid)
async def connect_client(sid, client: str):
    await mgr.save_client_session(sid, client)

@sio.event
async def disconnect(sid):
    logger.info(f"Client {sid} disconnected")
    await sio.leave_room(sid=sid, room=sid)
    await mgr.remove_session(sid)

# You can define more events here for handling different messages

async def start_socketio_server():
   pass
  #  await sio.start_background_task(background_task)

async def background_task():
    pass
    # Your background tasks (e.g., managing connections) can go here

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
    logger.info("hello worls")
   # asyncio.run(start_socketio_server())