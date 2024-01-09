

from pydantic import BaseModel
from helpr.schemas.action import ActionSchema
from helpr.schemas.action_run import ActionRunSchema

from helpr.schemas.message import ActionRequestMessageSchema, ActionResultMessageSchema, BotMessageSchema, MessageSchema


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


class SocketServerChatMessage(BaseSocketServerMessage):
    message: MessageSchema
    
    
    def get_data(self):
        return {'message': self.message.model_dump()}
    
    @staticmethod
    def get_event():
        raise NotImplementedError()


#TODO: holy shit these look horrid
class SocketServerMessageBotChat(BaseSocketServerMessage):
    message: BotMessageSchema
    
          
    def get_data(self):
        return {'message': self.message.model_dump()}
    
    
    @staticmethod
    def get_event():
        return "message_bot"

class SocketServerMessageActionRequestChat(BaseSocketServerMessage):
    message: ActionRequestMessageSchema
    
    
    def get_data(self):
        return {'message': self.message.model_dump()}
    
    
    @staticmethod
    def get_event():
        return "message_action_request"
    

"""class SocketServerMessageActionRequestResponseChat(BaseSocketServerMessage):
    message: ActionRequestResponseMessageSchema
    
    def get_data(self):
        return {'message': self.message.model_dump()}
    
    
    @staticmethod
    def get_event():
        return "message_action_request_response"
"""
class SocketServerMessageActionResultChat(BaseSocketServerMessage):
    message: ActionResultMessageSchema
    
    
    def get_data(self):
        return {'message': self.message.model_dump()}
    
    
    @staticmethod
    def get_event():
        return "message_action_result"
    

 
class SocketServerMessageActionRun(BaseSocketServerMessage):
    action_run: ActionRunSchema
    
    def get_data(self):
        return {'action_run': self.action_run.model_dump()}
    
    
    @staticmethod
    def get_event():
        return "action_run"
    
class SocketServerMessageActionRunStatus(BaseSocketServerMessage):
    action_run_id: int
    status: str
    
    def get_data(self):
        return {'status': self.status, 'action_run_id': self.action_run_id}
    
    @staticmethod
    def get_event():
        return "action_run_status"