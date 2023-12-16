import email
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from flask import jsonify
from pydantic import BaseModel
from sqlalchemy import JSON, select
from plannr.api.jwt_auth import jwt_user_auth
import plannr.db as db
from plannr.db.models.user import DBUser
import json
from fastapi.encoders import jsonable_encoder

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
    new_token = jwt_user_auth.encode(user.id)
    #TODO: return custom class instead
    return JSONResponse(content={'token': new_token, 'user': jsonable_encoder(user)})
 
    
    
class SignIn(BaseModel):
    email: str
    password: str
    
@router.post('/signin')
async def sign_in(params: SignIn):
    async with db.session() as session:
        user = (await session.execute(select(DBUser).where(DBUser.email == params.email))).scalar_one_or_none()
        await session.commit()

    if not user or not user.verify_password(params.password):
        return JSONResponse(status_code=402, content="Wrong email or password")
        
    
    new_token = jwt_user_auth.encode(user.id)
    #TODO: return custom class instead
    return JSONResponse(content={'token': new_token, 'user': jsonable_encoder(user)})

