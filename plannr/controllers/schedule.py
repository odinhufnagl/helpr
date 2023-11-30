
from dataclasses import dataclass
from optparse import Option
from typing import List, Optional
from models import BaseSchool, BaseTeacher, ClassGroup
from plannr.schedule import BaseSchedule
from feedback import BaseFeedback



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