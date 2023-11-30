from dataclasses import dataclass
from models.classroom.base import ClassRoom
from models.event.base import BaseEvent, ClassGroupsEvent, ClassRoomsEvent, Lecture, TeachersEvent
from models.classgroup.base import ClassGroup
from typing import List
from prettytable import PrettyTable
from src.models.teacher.base import BaseTeacher

@dataclass
class BaseSchedule:
    events: List[BaseEvent]
    
    def add_event(self, event: BaseEvent):
        self.events.append(event)
        
    def filter_by_teacher(self, teacher: BaseTeacher) -> 'TeacherSchedule':
        filtered_events = []
        for event in self.events:
            if isinstance(event, TeachersEvent):
                filtered_events.append(event)
        return TeacherSchedule(filtered_events, teacher)
                
    
    def filter_by_class_group(self, class_group: ClassGroup) -> 'ClassGroupSchedule':
        filtered_events = []
        for event in self.events:
            if isinstance(event, ClassGroupsEvent):
                filtered_events.append(event)
        return ClassGroupSchedule(filtered_events, class_group)
            
    
    def filter_by_class_room(self, class_room: ClassRoom) -> 'ClassRoomSchedule':
        filtered_events = []
        for event in self.events:
            if isinstance(event, ClassRoomsEvent):
                filtered_events.append(event)
        return ClassRoomSchedule(filtered_events, class_room)
    
    def print(self):
        pass
    @staticmethod
    def default():
        return BaseSchedule([])
    
@dataclass
class ClassGroupSchedule(BaseSchedule):
    events: List[ClassGroupsEvent]
    class_group: ClassGroup
    
    def print(self):
        table = PrettyTable()
        table.field_names = ["Day", "Time Interval", "Event Type", "Teacher"]

        for event in self.events:
            time_interval = f"{event.interval.start_time}-{event.interval.end_time}"
            event_type = type(event).__name__
            details = ""

            if isinstance(event, Lecture):
                details = f"{event.course.name}/{event.teachers[0].name}"
            table.add_row([time_interval, event_type, details])

        print(table)
    
@dataclass
class TeacherSchedule(BaseSchedule):
    events: List[TeachersEvent]
    teacher: BaseTeacher
    
    def print(self):
        table = PrettyTable()
        table.field_names = ["Day", "Time Interval", "Event Type", "ClassGroup"]

        for event in self.events:

            time_interval = f"{event.interval.start_time}-{event.interval.end_time}"
            event_type = type(event).__name__
            details = ""

            if isinstance(event, Lecture):
                details = f"{event.class_groups[0].name}"
            table.add_row([time_interval, event_type, details])

        print(table)

@dataclass
class ClassRoomSchedule(BaseSchedule):
    events: List[ClassRoomsEvent]
    class_room: ClassRoom
    
