
from schedulers.base import DumbScheduler
from scheduling.classgroup.base import ClassGroup
from scheduling.classroom.base import ClassRoom
from scheduling.course.base import BaseCourse
from administrators.schedule_admin import ScheduleAdministrator
from scheduling.event.base import Lecture
from scheduling.requirement.base import ClassGroupEventRequirement, ScalePriority, TeacherEventRequirement
from scheduling.schedule.base import BaseSchedule, TeacherSchedule
from scheduling.school.base import BaseSchool
from scheduling.teachers.base import BaseTeacher


school_1 = BaseSchool("Kitas")
course_1 = BaseCourse("Matematik 1", "M1", school_1)
course_2 = BaseCourse("Engelska", "E", school_1)
course_3 = BaseCourse("Teknik", "T", school_1)
class_room_1 = ClassRoom("Rum 1", "R1", school_1)
teacher_1 = BaseTeacher(name="Odin Hufnagl")
classgroup_1 = ClassGroup("NT3C", "NT3C", school_1)

schedule = DumbScheduler.generate_schedule([], [], BaseSchedule())
