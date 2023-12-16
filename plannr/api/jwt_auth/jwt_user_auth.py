import json
from jwt import encode as base_encode
from jwt import decode as base_decode
from pydantic import BaseModel
from plannr.logger import logger

class JWTUserAuth(BaseModel):
    algorithm: str | None = "HS256"
    secret: str
    def encode(self, user_id) -> str:
        payload = {"user_id": user_id}
        return base_encode(payload=payload, algorithm=self.algorithm, key=self.secret)
    def decode(self, token) -> int | None:
        jwt_object = base_decode(token, algorithms=[self.algorithm], key=self.secret)
        if isinstance(jwt_object, dict) and 'user_id' in jwt_object.keys():
            return int(jwt_object['user_id'])
        
#TODO: use better secret and store it in .env
jwt_user_auth = JWTUserAuth(secret="bad secret")