import json
from jwt import encode as base_encode
from jwt import decode as base_decode
from pydantic import BaseModel
from helpr.logger import logger



#TODO: pretty repetitive and shit, should be done better, the secret now has to be same on all of these

class JWTAuth(BaseModel):
    algorithm: str | None = "HS256"
    secret: str
    
    def encode(self, payload):
        return base_encode(payload=payload, algorithm=self.algorithm, key=self.secret)
    def decode(self, token):
        try:
            logger.info(f"what is going on??: {token}")
            jwt_object = base_decode(token, algorithms=[self.algorithm], key=self.secret)
            logger.info(f"jwt_object: {jwt_object}")
            return jwt_object
        except:
            return None
        
jwt_auth = JWTAuth(secret="bad secret")

class JWTUserAuth(JWTAuth):
    algorithm: str | None = "HS256"
    secret: str
    def encode(self, user_id) -> str:
        payload = {"user_id": user_id}
        return base_encode(payload=payload, algorithm=self.algorithm, key=self.secret)
    def decode(self, token) -> int | None:
        try:
            jwt_object = base_decode(token, algorithms=[self.algorithm], key=self.secret)
            if isinstance(jwt_object, dict) and 'user_id' in jwt_object.keys():
                return int(jwt_object['user_id'])
        except:
            return None
        
#TODO: use better secret and store it in .env
jwt_user_auth = JWTUserAuth(secret="bad secret")


class JWTClientAuth(JWTAuth):
    algorithm: str | None = "HS256"
    secret: str
    def encode(self, chat_session_id) -> str:
        payload = {"chat_session_id": chat_session_id}
        return base_encode(payload=payload, algorithm=self.algorithm, key=self.secret)
    def decode(self, token) -> int | None:
        try:
            jwt_object = base_decode(token, algorithms=[self.algorithm], key=self.secret)
            if isinstance(jwt_object, dict) and 'chat_session_id' in jwt_object.keys():
                return int(jwt_object['chat_session_id'])
        except:
            return None
        
#TODO: use better secret and store it in .env
jwt_client_auth = JWTClientAuth(secret="bad secret")
