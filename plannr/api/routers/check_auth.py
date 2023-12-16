import email
from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from plannr.api.jwt_auth import jwt_user_auth
from plannr.api.request.base import AuthedRequest
import plannr.db as db
from plannr.db.models.user import DBUser
jsonable_encoder
router = APIRouter(prefix='/authenticate')
    

@router.get('')
async def authenticate(request: Request):
    request = AuthedRequest.from_request(request)
    async with db.session() as session:
        user = (await session.execute(select(DBUser).where(DBUser.id == request.user_id))).scalar_one_or_none()
    if not user:
        return JSONResponse(status_code=402, content="Not Authenticated")
        
    #TODO: validate-password
    
    new_token = jwt_user_auth.encode(user.id)
    #TODO: return custom class instead
    
    return JSONResponse(content={'token': new_token, 'user': jsonable_encoder(user)})
