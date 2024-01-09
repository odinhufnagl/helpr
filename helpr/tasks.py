
import asyncio
import sys
import os

from openai import chat




sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpr import schemas
from time import sleep
from celery import Celery
from helpr.schemas.message import BotMessageSchema
from celery.signals import worker_ready, worker_init
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from dotenv import load_dotenv
from agent.chat_agent import ChatAgent
from db.models.agent import DBAgent
from socket_components.message import SocketServerMessageActionRunStatus, SocketServerMessageBotChat
from socket_components.message_queue import socket_message_queue
from services.action_run import *
from services.database import update
from helpr.schemas.action_run import ActionRunStatus
from helpr.agent.chat_session_agent import ChatSessionAgent
import db

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





#TODO: this code should be thought through so that it can be divided into better parts, because for example
#we might want to do basically all this except not using it as a task, or at the same time, there might be differences to the other
#time we want to use it, so look it through and think about what could go into a own function, and decide if that should be a service/util/or something/or own file

#TODO: this function is part of it and should also be "re-thought" on how it should be structured


#TODO: one things that COULD make sense if have one class that handles everyhting about this like for example when updating status it also sends to socket
#it basically encapsulates all logic in its "run" function so that it updates the database and sends socket etc etc. It could be called like ActionRunxxx
#not sure what xxx should be though, maybe controller not sure. Ask GPT. Anyways this is not optimal because a lot of repition for example with sending 
#chat_session_id to change_status_on_action_run, which may not actually make sense after how we have named the functions

async def change_status_on_action_run(action_run_id: int, status: ActionRunStatus, chat_session_id: int):
    await update(DBActionRun, action_run_id, {'status': status})
    await socket_message_queue.emit_to_client(SocketServerMessageActionRunStatus(action_run_id=action_run_id, status=status), [chat_session_id])
    

async def async_run_action(action_run_id: int, chat_session_id: int):
    action_run_schema = await get_action_run_by_id(action_run_id)
    await change_status_on_action_run(action_run_id, "running", chat_session_id)
    action = BaseAction.from_schema(action_run_schema.action)
    try:
        result = await action.run(action_run_schema.input)
    except:
        await change_status_on_action_run(action_run_id, "error", chat_session_id)
        return
    await change_status_on_action_run(action_run_id, "finished", chat_session_id)
    return result

@celery.task
def run_action(action_run_id: int, chat_session_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_run_action(action_run_id, chat_session_id=chat_session_id))
    



@worker_init.connect
async def startup(**kwargs):
    pass
