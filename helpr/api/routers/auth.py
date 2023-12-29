import email
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from flask import jsonify
import orjson
from pydantic import BaseModel
from sqlalchemy import JSON, Select, select
from helpr.logger import logger
from helpr.api.error.base import ApiWrongEmailPasswordException
from helpr.api.jwt_auth import jwt_user_auth
import helpr.db as db
from helpr.db.models.user import DBUser
import json
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy.orm import make_transient, selectinload
from sqlalchemy import select
from helpr.schemas.user import UserSchema

router = APIRouter(prefix='/auth')

class SignUp(BaseModel):
    email: str
    password: str
    
@router.post('/signup')
async def sign_up(params: SignUp):
    async with db.session() as session:
        user = DBUser(email=params.email)
        user.password_hash = params.password
        session.add(user)
        await session.commit()

    user = UserSchema.from_model(user)

    new_token = jwt_user_auth.encode(user.id) 
    #TODO: return custom class instead
    return {'token': new_token, 'user': user}
 
    
    
class SignIn(BaseModel):
    email: str
    password: str
    
@router.post('/signin')
async def sign_in(params: SignIn):
    async with db.session() as session:
        user = (await session.execute(select(DBUser).where(DBUser.email == params.email))).scalar_one_or_none()
        await session.commit()

    if not user or not user.verify_password(params.password):
        raise ApiWrongEmailPasswordException()
    
    user = UserSchema.from_model(user)
        
    new_token = jwt_user_auth.encode(user.id)
    #TODO: return custom class instead
    return {'token': new_token, 'user': user}

