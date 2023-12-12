
import asyncio
import sys
from time import sleep
from celery import Celery
import os
from celery.signals import worker_ready, worker_init
from sqlalchemy import select
from dotenv import load_dotenv
from sqlalchemy.orm import joinedload, selectinload
import socketio
import db
from generators.schedule import CoalitionScheduleGenerator
from socket_components import socket_message_queue
from socket_components.message import SocketServerMessageScheduleGenerated
#TODO: centralise dotenv fetch and so we can device to run with local or production
load_dotenv()
#TODO: use .env for all values in celery
celery = Celery(os.environ['CELERY_MAIN_NAME'], broker=os.environ['CELERY_BROKER'],
    backend=os.environ['CELERY_BACKEND'])

#TODO: this should be a class or something reusable atleast, or atleast the entire socket structure with its messages and so on will have to be a whole structure



#TODO: add feedback
#TODO: what if there is already a generate on that schedule? Check the state in db, or finish the previous

async def generate_schedule_async(schedule_id: int):
    await db.init()
    generated_schedule = await CoalitionScheduleGenerator.generate_schedule(schedule_id=schedule_id, feedback=[])
    #TODO: read above about making this a better structure, for example now we have to match 'schedule_generated' in server and here, not good
    #send to correct client, this will require some type of storage where all clients are kept, so for example you can find them with their user_id,
    #they should be inserted from the websocket-server, and then found here. This should all happen in well-structured classes.
    #so there is lots of work to do around the socket-system
    #TODO: either we should send to all users in the coalition, or just to one who is creating the schedule, then we need to restructure 
    #the api and how the schedulecontroller works and so on, also add to db. But i believe multiple users in a coalition should be able to 
    #edit the same schedule
    async with db.session() as session:
        schedule = (await session.execute(select(db.models.DBSchedule).where(db.models.DBSchedule.id == schedule_id).options(selectinload(db.models.DBSchedule.coalition).options(selectinload(db.models.DBCoalition.admins))))).scalar_one_or_none()
        print("admins", schedule.coalition.admins)
    user_ids = list(map(lambda a: a.user_id, schedule.coalition.admins))
    await socket_message_queue.emit(SocketServerMessageScheduleGenerated(schedule_id=schedule_id), user_ids)
    print(generated_schedule)
    
@celery.task
def generate_schedule(schedule_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_schedule_async(schedule_id))
  
  
@worker_init.connect
async def startup(**kwargs):
  await db.init()

  