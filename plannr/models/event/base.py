

from dataclasses import dataclass
from typing import List
from plannr.models.classgroup.base import ClassGroup
from plannr.models.classroom.base import ClassRoom
from plannr.models.course.base import BaseCourse
from plannr.models.event.type import EventType
from plannr.models.school.base import BaseSchool
from plannr.models.teacher.base import BaseTeacher
from common.date import  TimeInterval

@dataclass
class BaseEvent:
    interval: TimeInterval
    type: EventType
@dataclass
class TeachersEvent(BaseEvent):
    teachers: List[BaseTeacher]
@dataclass
class ClassGroupsEvent(BaseEvent):
    class_groups: List[ClassGroup]
@dataclass
class ClassRoomsEvent(BaseEvent):
    class_rooms: List[ClassRoom]
@dataclass
class Lecture(TeachersEvent, ClassGroupsEvent, ClassRoomsEvent):
    course: BaseCourse
    school: BaseSchool
    type = EventType.LECTURE
       
@dataclass
class TeachersLunch(TeachersEvent):
    type = EventType.TEACHER_LUNCH
@dataclass
class ClassGroupsLunch(ClassGroupsEvent):
    class_group: ClassGroup
    type = EventType.CLASSGROUP_LUNCH
