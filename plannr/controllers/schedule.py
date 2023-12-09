
import asyncio
from dataclasses import dataclass
from optparse import Option
from taskqueue.queue import Queue
from time import sleep
from typing import List, Optional
from uu import Error
from models import BaseSchool, BaseTeacher, ClassGroup
from models.coalition.base import BaseCoalition
import db
from db.models.requirement import DBRequirement
from db.models.event import DBEvent
from requirement.base import BaseRequirement
from schedule.base import BaseSchedule
from feedback import BaseFeedback
from schedulers.base import DumbScheduler
from sqlalchemy import select
from pydantic import BaseModel
from logger import logger

queue = Queue()

class BaseFilter:
    pass


class TeacherFilter(BaseFilter):
    teacher: BaseTeacher


class ClassGroupFilter(BaseFilter):
    class_group: ClassGroup


@dataclass
class BaseScheduleController:

    def __post_init__(self):
        pass

    def get_schedule(self, filters: List[BaseFilter]) -> BaseSchedule:
        raise NotImplementedError()

# TODO: id should not be int


#TODO: look through this and decide what should be in-params to the model
class CoalitionScheduleController(BaseModel, BaseScheduleController):
    coalition_id: Optional[int] = None
    coalition: Optional[BaseCoalition] = None
    requirements: List[BaseRequirement] = []
    schedule: Optional[BaseSchedule] = None
    
    class Config:
        arbitrary_types_allowed = True

    # TODO: this should be started as a parallel process on different thread
    # TODO: return ongoing schedule_id aswell
    async def create_new_schedule(self) -> int:
        empty_schedule = BaseSchedule(None, self.coalition_id, BaseSchedule.State.CREATING, [])
        await empty_schedule.store_to_db()
        await queue.push_generate_schedule(empty_schedule.schedule_id)
        return empty_schedule.schedule_id

    def get_schedule(self, filters: List[BaseFilter]) -> BaseSchedule:
        raise NotImplementedError
    
    async def approve_schedule(self, schedule_id: int) -> bool:
        #should approve the schedule for eg set its state to ongoing and update all the events to finished
        raise NotImplementedError
