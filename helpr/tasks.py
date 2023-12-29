
import asyncio
import sys
import os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpr import schemas
from time import sleep
from celery import Celery
from helpr.schemas.message import BotMessageSchema
from celery.signals import worker_ready, worker_init
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from dotenv import load_dotenv
from agent.chat_agent import ChatAgent, ChatSessionAgent
from db.models.agent import DBAgent
from socket_components.message import SocketServerMessageBotChat
from socket_components.message_queue import socket_message_queue
import db
from db.models import DBChatSession, DBChat
# TODO: centralise dotenv fetch and so we can define to run with local or production
load_dotenv()

celery = Celery(os.environ['CELERY_MAIN_NAME'], broker=os.environ['CELERY_BROKER'],
                backend=os.environ['CELERY_BACKEND'])

async def async_generate_bot_message(chat_session_id: int):
    print(f"The task was called. chat_session_id: {chat_session_id}")
    chat_agent = await ChatSessionAgent.construct_default(chat_session_id=chat_session_id)
    message_schemas = await chat_agent.chat()
    print(f'message_schemas: {message_schemas}',)
    print("what is going on")
    for message in message_schemas:
        try:
            await socket_message_queue.emit_to_client(message.to_socket_message(), clients=[chat_session_id])
        except:
            print(message.to_socket_message())
            continue


@celery.task
def generate_bot_message(chat_session_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_generate_bot_message(chat_session_id))
    
async def async_generate_index():
    pass

@celery.task
def generate_index():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_generate_index)



async def async_run_action(action_run_id: int):
    #TODO: set action as running
    #start it
    #update status on it
    #send to user
    pass

@celery.task
def run_action(action_run_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete()



@worker_init.connect
async def startup(**kwargs):
    pass
