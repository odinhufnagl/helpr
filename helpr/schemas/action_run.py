from dataclasses import dataclass
from datetime import datetime
import string
from typing import Dict, List, Optional
from pydantic import BaseModel

from helpr.schemas.base import BaseSchema

class ActionRunSchema(BaseSchema):
    id: int
    credentials: Dict | None
    input: Dict | None
    output: Dict | None
    is_public: bool
    action_id: int
    input: Dict | None
    output: Dict | None
    
    
    