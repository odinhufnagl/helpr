
from abc import ABC, abstractproperty
from pydantic import BaseModel
import db
from sqlalchemy import update

class BaseCredentialProvider(BaseModel, ABC):

  class Data(BaseModel):
    pass

  @classmethod
  async def create_credential(cls, data: Data, organization_id: int) -> int:
    async with db.session() as session:
      credential = db.models.Credential(
        provider=cls.name,
        data=data.dict(),
        organization_id=organization_id,
      )
      session.add(credential)
      await session.commit()
      return credential.id
  
  @classmethod
  async def update_credential(cls, id: int, data: Data):
    async with db.session() as session:
      await session.execute(
        update(db.models.Credential)
          .where(db.models.Credential.id == id)
          .values(data=data.dict())
      )
      await session.commit()

  def __init_subclass__(cls, **kwargs):
    super().__init_subclass__(**kwargs)

  @abstractproperty
  @classmethod
  def name(cls) -> str:
    raise NotImplementedError
