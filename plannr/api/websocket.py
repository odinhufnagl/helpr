import asyncio
from dotenv import load_dotenv
from socketio import AsyncServer, ASGIApp
import socketio
import uvicorn
import os
import db
from services.database import update as db_update
load_dotenv()
#TODO: env variables
mgr = socketio.AsyncRedisManager(os.environ['SOCKET_MESSAGE_QUEUE'])
sio = socketio.AsyncServer(client_manager=mgr, logger=True, async_mode='asgi')
app = ASGIApp(sio)
from logger import logger


@sio.event
async def message():
    logger.info("message arrived")

@sio.event
async def connect(sid, environ):
    logger.info(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    logger.info(f"Client {sid} disconnected")

# You can define more events here for handling different messages

async def start_socketio_server():
   
    await sio.start_background_task(background_task)
    await sio.sleep(0.1)

async def background_task():
    pass
    # Your background tasks (e.g., managing connections) can go here

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081, debug=True)
    logger.info("hello worls")
   # asyncio.run(start_socketio_server())