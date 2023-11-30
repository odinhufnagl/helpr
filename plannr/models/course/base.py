from dataclasses import dataclass
from models import BaseSchool

@dataclass
class BaseCourse:
    name: str
    code: str
    school: BaseSchool