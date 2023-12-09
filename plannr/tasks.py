
import asyncio
import sys
from celery import Celery
import os
from celery.signals import worker_ready, worker_init
from dotenv import load_dotenv
import socketio
import db
from generators.schedule import CoalitionScheduleGenerator
#TODO: centralise dotenv fetch and so we can device to run with local or production
load_dotenv()
#TODO: use .env for all values in celery
celery = Celery(os.environ['CELERY_MAIN_NAME'], broker=os.environ['CELERY_BROKER'],
    backend=os.environ['CELERY_BACKEND'])

#TODO: this should be a class or something reusable atleast, or atleast the entire socket structure with its messages and so on will have to be a whole structure
external_sio = socketio.RedisManager(os.environ['SOCKET_MESSAGE_QUEUE'], write_only=True)


#TODO: add feedback
#TODO: what if there is already a generate on that schedule? Check the state in db, or finish the previous

async def generate_schedule_async(schedule_id: int):
    await db.init()
    generated_schedule = await CoalitionScheduleGenerator.generate_schedule(schedule_id=schedule_id, feedback=[])
    #TODO: read above about making this a better structure, for example now we have to match 'schedule_generated' in server and here, not good
    #send to correct client, this will require some type of storage where all clients are kept, so for example you can find them with their user_id,
    #they should be inserted from the websocket-server, and then found here. This should all happen in well-structured classes.
    #so there is lots of work to do around the socket-system
    external_sio.emit('schedule_generated', data={'schedule_id': 1})
    print(generated_schedule)
    
@celery.task
def generate_schedule(schedule_id: int):
  asyncio.run(generate_schedule_async(schedule_id))
  
  
@worker_init.connect
async def startup(**kwargs):
  await db.init()

  