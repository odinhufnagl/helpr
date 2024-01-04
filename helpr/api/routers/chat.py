import re
import string
from tabnanny import check
from typing import List
from fastapi import APIRouter, Depends, Request
from helpr.api.error.base import ApiException, ApiNoTokenException, ApiNotValidTokenException
from helpr.db.models.chat_session import DBChatSession
from helpr.logger import logger
from pydantic import BaseModel
from sqlalchemy import select
import db
from helpr.api.middleware.auth import PermissionChecker
from helpr.api.request.base import AuthedRequest, ClientAuthRequest
from helpr.organizations.permissions import Permission, PermissionRole
from helpr.schemas import OrganizationSchema
from helpr.schemas.chat_session import ChatSessionSchema
from helpr.schemas.message import dto
import helpr.services.message as message_service
from helpr.task_queue import task_queue
import jwt
from helpr.api.jwt_auth import jwt_client_auth
from services.chat_session import create as create_chat_session
from services.chat_session import get as get_chat_session
router = APIRouter(prefix='/chats')

class PostChatSession(BaseModel):
    chat_id: int
    
    

async def check_client_session(request: Request, chat_id: int):
        request = ClientAuthRequest.from_request(request)
        if not request.access_token:
            raise ApiNoTokenException()
        chat_session_id_in_token = jwt_client_auth.decode(request.access_token)
        if not chat_session_id_in_token:
            raise ApiNotValidTokenException()
        async with db.session() as session:
            chat_id_from_chat_session = (await session.execute(select(DBChatSession.chat_id).where(DBChatSession.id == chat_session_id_in_token))).scalar_one_or_none()
            await session.commit()
            if chat_id != chat_id_from_chat_session:
                raise ApiNotValidTokenException()
            else: return True
       

@router.post("/{chat_id}/connect")
async def connect(chat_id: int, request: Request):
    request = ClientAuthRequest.from_request(request)
    chat_session_id_from_token = jwt_client_auth.decode(request.access_token)
    if not chat_session_id_from_token:
        new_chat_session = await create_chat_session(chat_id)
        generated_token = jwt_client_auth.encode(new_chat_session.id)
        return {'token': generated_token, 'chat_session': new_chat_session}
    if chat_session_id_from_token:
        chat_session = await get_chat_session(chat_session_id_from_token)
        if chat_session.chat_id != chat_id:
            raise ApiException()
        new_generated_token = jwt_client_auth.encode(chat_session.id)
        return {'token': new_generated_token, 'chat_session': chat_session}
        

@router.get('/{chat_id}/messages')
async def get_messages(chat_id: int, request: Request,  limit: int, offset: int, has_access = Depends(check_client_session)):
    request = ClientAuthRequest.from_request(request)
    #TODO: should be middleware
    chat_session_id_from_token = jwt_client_auth.decode(request.access_token)
    logger.info(f"whyy: {request.access_token}")
    logger.info(f"chat-session: {chat_session_id_from_token}")
    messages, count = await message_service.get_messages(chat_session_id_from_token, limit=limit, offset=offset*limit, order='desc') #TODO: fix pagination, better distincion between page and offset
    logger.info(f"messages: {messages}")
    return {'count': count, 'rows': messages} #TODO: this is wrong, should not be len(messages)

class PostMessage(BaseModel):
    text: str
    
@router.post('/{chat_id}/messages')
async def post_message(chat_id: int, params: PostMessage, request: Request, has_access = Depends(check_client_session)):
    request = ClientAuthRequest.from_request(request)
    #TODO: should be middleware
    chat_session_id_from_token = jwt_client_auth.decode(request.access_token)
    logger.info(f"chat-session: {chat_session_id_from_token}")
    message = await message_service.create_user_message(dto.CreateUserMessage(text=params.text, chat_session_id=chat_session_id_from_token))
    await task_queue.push_generate_bot_message(chat_session_id_from_token)
    return message