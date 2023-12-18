

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

class SocketServerMessageBotChat(BaseSocketServerMessage):
    chat_session_id: int
    text: str
    class Data(BaseModel):
        chat_session_id: int
        text: str
    
    def get_data(self) -> Data.__dict__:
        return {'chat_session_id': self.chat_session_id, 'text': self.text}
    
    @staticmethod
    def get_event():
        return "message_bot"