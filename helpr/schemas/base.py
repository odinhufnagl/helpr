from pydantic import BaseModel


class BaseSchema(BaseModel):
    @classmethod
    def from_model(cls, model):
        return cls.from_orm(model.__dict__)
    
        
    class Config:
        orm_mode = True
        from_attributes=True
    