

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



#TODO: holy shit these look horrid
class SocketServerMessageBotChat(BaseSocketServerMessage):
    id: int
    chat_session_id: int
    text: str
    class Data(BaseModel):
        chat_session_id: int
        text: str
    
    def get_data(self) -> Data.__dict__:
        return {'id': self.id, 'chat_session_id': self.chat_session_id, 'text': self.text}
    
    @staticmethod
    def get_event():
        return "message_bot"

class SocketServerMessageActionRequestChat(BaseSocketServerMessage):
    id: int
    text: str
    chat_session_id: int
    action_id: int
    input: str

    class Data(BaseModel):
        text: str
        chat_session_id: int
        action_id: int
        input: str
    
    def get_data(self) -> Data.__dict__:
        return {'id': self.id, 'chat_session_id': self.chat_session_id, 'text': self.text, 'action_id': self.action_id, 'input': self.input}
    
    @staticmethod
    def get_event():
        return "message_action_request"
    
class SocketServerMessageActionResultChat(BaseSocketServerMessage):
    id: int
    text: str
    chat_session_id: int
    action_id: int
    output: str

    class Data(BaseModel):
        text: str
        chat_session_id: int
        action_id: int
        output: str
    
    def get_data(self) -> Data.__dict__:
        return {'id': self.id, 'chat_session_id': self.chat_session_id, 'text': self.text, 'action_id': self.action_id, 'output': self.output}
    
    @staticmethod
    def get_event():
        return "message_action_result"
    

 
 