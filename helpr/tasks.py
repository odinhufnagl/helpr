
import asyncio
import sys
from time import sleep
from celery import Celery
import os
from celery.signals import worker_ready, worker_init
from sqlalchemy import select
from dotenv import load_dotenv
from socket_components.message import SocketServerMessageBotChat
from socket_components.message_queue import socket_message_queue

#TODO: centralise dotenv fetch and so we can device to run with local or production
load_dotenv()
#TODO: use .env for all values in celery
celery = Celery(os.environ['CELERY_MAIN_NAME'], broker=os.environ['CELERY_BROKER'],
    backend=os.environ['CELERY_BACKEND'])

#TODO: this should be a class or something reusable atleast, or atleast the entire socket structure with its messages and so on will have to be a whole structure


async def async_generate_bot_message(chat_session_id: int):
   print(f"The task was called. chat_session_id: {chat_session_id}")
   await socket_message_queue.emit_to_client(SocketServerMessageBotChat(chat_session_id=chat_session_id, text="Hey nice to meet you"), clients=[chat_session_id])

@celery.task
def generate_bot_message(chat_session_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_generate_bot_message(chat_session_id))
  
  
  
@worker_init.connect
async def startup(**kwargs):
  pass
  