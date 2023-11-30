from dataclasses import dataclass
from models import BaseSchool

@dataclass
class ClassRoom:
    name: str
    code: str
    school: BaseSchool
