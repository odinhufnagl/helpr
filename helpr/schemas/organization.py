from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from helpr.schemas.base import BaseSchema

class OrganizationSchema(BaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    users: Optional[List['UserSchema']] = None #type: ignore

    