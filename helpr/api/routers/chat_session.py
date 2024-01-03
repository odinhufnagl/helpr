import string
from tabnanny import check
from typing import List
from fastapi import APIRouter, Depends, Request
from helpr.api.error.base import ApiNoTokenException, ApiNotValidTokenException
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

router = APIRouter(prefix='/chat_sessions')

class PostChatSession(BaseModel):
    chat_id: int
    

async def check_client_session(request: Request, chat_session_id: int):
        chat_session_id_in_path = chat_session_id
        request = ClientAuthRequest.from_request(request)
        logger.info(request.headers)
        if not request.access_token:
            raise ApiNoTokenException()
        chat_session_id_in_token = jwt_client_auth.decode(request.access_token)
        if not chat_session_id_in_token:
            raise ApiNotValidTokenException()
        if chat_session_id_in_path != chat_session_id_in_token:
            raise ApiNotValidTokenException()

        return True



@router.post('')
async def post_chat_session(params: PostChatSession, request: Request):
    #TODO: generate a session to add to the db_chat_session, could be generated upon creation
    async with db.session() as session:
        model = db.models.DBChatSession(chat_id=params.chat_id)
        session.add(model)
        await session.commit()
        logger.info(f"model: {model.__dict__}")
    generated_token = jwt_client_auth.encode(model.id)
    return {'token': generated_token, 'chat_session': ChatSessionSchema.from_model(model)}
    
@router.get('/{chat_session_id}')
async def get_chat_session(chat_session_id: int, has_access = Depends(check_client_session)):
    async with db.session() as session:
        model = (await session.execute(select(db.models.DBChatSession).where(db.models.DBChatSession.id == chat_session_id))).scalar_one_or_none()
        await session.commit()
    return ChatSessionSchema.from_model(model)
          
class PostMessage(BaseModel):
    text: str
    
@router.post('/{chat_session_id}/messages')
async def post_message(chat_session_id: int, params: PostMessage, has_access = Depends(check_client_session)):
    message = await message_service.create_user_message(dto.CreateUserMessage(text=params.text, chat_session_id=chat_session_id))
    await task_queue.push_generate_bot_message(chat_session_id)
    return message

@router.get('/{chat_session_id}/messages')
async def get_messages(chat_session_id: int, has_access = Depends(check_client_session)):
    messages = await message_service.get_messages(chat_session_id) #TODO: fix pagination
    return messages

    
                                                                            
"""@router.post('/{chat_session_id}/action_request_response_message')
async def post_action_request_response_message(chat_session_id: int, params: PostMessage, has_access: Depends(check_client_session)):
    message = await message_service.create_action_request_response_message(dto.Create)
"""