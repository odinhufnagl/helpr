from dataclasses import dataclass
from enum import Enum
import re
from tkinter import Scale
from typing import Any, List, Optional
from uu import Error

from setuptools import Require
from scheduling.classgroup.base import ClassGroup
from scheduling.classroom.base import ClassRoom
from scheduling.event.base import BaseEvent
from common.date import TimeInterval
from scheduling.schedule.base import BaseSchedule
from scheduling.school.base import BaseSchool
from scheduling.teachers.base import BaseTeacher


#TODO: better structure so it is easy to create new requirements



@dataclass
class RequirementDeviation:
    value: int

@dataclass
class PriorityScale:
    min: int
    max: int
    
    def is_in_range(self, value):
        return min <= value or value <= max
    
class BaseRequirement:
    PRIORITY_MAX = 100
    PRIORITY_MIN = 0
    priority_scale = PriorityScale(PRIORITY_MIN,PRIORITY_MAX)
    priority: int
     
    def __init__(self, prio) -> None:
        self.set_priority(prio)
    
    def set_priority(self, prio: int):
        if self.priority_scale.is_in_range(prio):
            self.priority = prio
            return
        raise Error
    
    def deviation(self, schedule: BaseSchedule) -> RequirementDeviation:
        raise NotImplementedError
            
        
    
@dataclass
class TeacherRequirement(BaseRequirement):
    teacher: BaseTeacher
@dataclass
class ClassGroupRequirement(BaseRequirement):
    class_group: ClassGroup
@dataclass
class ClassRoomRequirement(BaseRequirement):
    class_room: ClassRoom
@dataclass
class TeacherEventRequirement(TeacherRequirement):
    event: BaseEvent
@dataclass
class ClassGroupEventRequirement(ClassGroupRequirement):
    event: BaseEvent
  
class SchoolRequirement(BaseRequirement):
    school: BaseSchool

