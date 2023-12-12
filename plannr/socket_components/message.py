

from pydantic import BaseModel


class BaseSocketMessage(BaseModel):
    
    def get_data(self):
        raise NotImplementedError()
    
    @staticmethod
    def get_event():
        raise NotImplementedError()
    
    
class BaseSocketClientMessage(BaseSocketMessage):
    pass

#actually probably the reciever should not be part of the message
#I should be able to create a message and send it to multiple and not have to define who it is going to
class BaseSocketServerMessage(BaseSocketMessage):
   # reciever_user_id: int
   pass

class SocketServerMessageScheduleGenerated(BaseSocketServerMessage):
    schedule_id: int
    
    class Data:
        schedule_id: int
    
    def get_data(self) -> dict:
        return {'schedule_id': self.schedule_id}
    @staticmethod
    def get_event():
        return 'schedule_generated'
    
