from dataclasses import dataclass
from scheduling.school.base import BaseSchool

@dataclass
class BaseCourse:
    name: str
    code: str
    school: BaseSchool