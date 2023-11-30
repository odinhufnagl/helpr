


from dataclasses import dataclass
from typing import List, Optional
from models.classgroup.base import ClassGroup
from models.classroom.base import ClassRoom
from requirement.base import BaseRequirement, ClassGroupEventRequirement, TeacherEventRequirement, TeacherRequirement
from schedule.base import BaseSchedule, ClassGroupSchedule, ClassRoomSchedule, TeacherSchedule
from src.models.teacher.base import BaseTeacher

@dataclass
class BaseFeedback:
    schedule: BaseSchedule
    

#TODO: a neat way of being able to create new algos for the scheduler

@dataclass
class BaseScheduler():
    @staticmethod
    def generate_schedule(requirements: List[BaseRequirement], feedback: List[BaseFeedback], prev_schedule: Optional[BaseSchedule]) -> BaseSchedule:
        raise NotImplementedError
    

@dataclass
class DumbScheduler(BaseScheduler):
    @staticmethod
    def generate_schedule(requirements: List[BaseRequirement], feedback: List[BaseFeedback], prev_schedule: Optional[BaseSchedule]) -> BaseSchedule:
        schedule = BaseSchedule([])
  
        for requirement in requirements:
            if isinstance(requirement, TeacherEventRequirement):
                schedule.add_event(requirement.event)
            if isinstance(requirement, ClassGroupEventRequirement):
                schedule.add_event(requirement.event)
        return schedule
    
       