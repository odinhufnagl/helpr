from typing import Optional

from dotenv import load_dotenv
import db
from tasks import generate_schedule as task_generate_schedule
import services.database as db_services
from pydantic import BaseModel
import logging
import os
#TODO: fix logging class
from logger import logger
from celery import Celery

load_dotenv()

class Queue():
   
  def __init__(self):
    self.api_url = os.environ['API_URL']
   
  async def push_generate_schedule(self, schedule_id: int) -> bool:
    logger.info(f"hello worldddd {schedule_id}")
    #TODO: should not be forced to use CREATING.name, check other places aswell. Should just be constants
    await db_services.update(db.models.DBSchedule, schedule_id, {'state': db.models.DBSchedule.State.CREATING.name})
    
    task_generate_schedule.delay(schedule_id)
    
    return True
  


    
    
    

