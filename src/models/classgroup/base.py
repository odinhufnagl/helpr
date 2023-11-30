from dataclasses import dataclass
from typing import List, Optional

from scheduling.school.base import BaseSchool



@dataclass
class ClassGroup:
    name: str
    code: str
    school: BaseSchool
