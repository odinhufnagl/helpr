
from dataclasses import dataclass
from optparse import Option
from typing import List, Optional
from src.models.classgroup.base import ClassGroup

from src.schedule.base import BaseSchedule

from src.models.school.base import BaseSchool

from src.models.teacher.base import BaseTeacher
from schedulers.base import BaseFeedback, DumbScheduler


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
        

#TODO: id should not be ints 
@dataclass 
class SchoolScheduleController(BaseScheduleController):
    school_id: int
    school: Optional[BaseSchool] = None
    def __post_init__(self):
       super().__post_init__()
       #fetch the school
    
    def generate_schedule(self, feedback: Optional[List[BaseFeedback]], prev_schedule_id: Optional[int]) -> BaseSchedule: #return ongoing schedule_id aswell
        raise NotImplementedError
        #store the schedule to the db as a ongoing_schedule
    def get_schedule(self, filters: List[BaseFilter]) -> BaseSchedule:
        raise NotImplementedError