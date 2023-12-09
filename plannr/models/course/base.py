from dataclasses import dataclass
from models.school import BaseSchool

@dataclass
class BaseCourse:
    name: str
    code: str
    school: BaseSchool