import email
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from helpr.api.jwt_auth import jwt_user_auth
from helpr.api.request.base import AuthedRequest
import helpr.db as db
from helpr.db.models.user import DBUser
from helpr.schemas.user import UserSchema

router = APIRouter(prefix='/authenticate')
    

@router.get('')
async def authenticate(request: Request):
    request = AuthedRequest.from_request(request)
    async with db.session() as session:
        user = (await session.execute(select(DBUser).where(DBUser.id == request.user_id))).scalar_one_or_none()
        await session.commit()
    if not user:
        return JSONResponse(status_code=402, content="Not Authenticated")
    
    user = UserSchema.from_model(user)
    
    new_token = jwt_user_auth.encode(user.id)
    
    #TODO: return custom class instead 
    return {'token': new_token, 'user': user}
