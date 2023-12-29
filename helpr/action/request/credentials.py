


from abc import ABC, abstractproperty
from typing import Any, Dict
from pydantic import BaseModel
import db
from sqlalchemy import update

class RequestCredentialProvider(BaseModel, ABC):

  class Data(BaseModel):
    pass
  
  @classmethod
  def name(cls) -> str:
    return 'request'
