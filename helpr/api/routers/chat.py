import re
import string
from tabnanny import check
from turtle import update
from typing import List, Optional
from fastapi import APIRouter, Depends, Request
from numpy import number
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
from helpr.schemas.action_run import dto
from helpr.schemas.chat_session import ChatSessionSchema
from helpr.schemas.message import ActionRequestMessageSchema, dto as message_dto
from helpr.schemas.action_request import dto as action_request_dto
import helpr.services.message as message_service
import helpr.services.action_request as action_request_service
from helpr.socket_components.message import SocketServerMessageActionRun
from helpr.task_queue import task_queue
import jwt
from helpr.api.jwt_auth import jwt_client_auth
from services.chat_session import create as create_chat_session
from services.chat_session import get as get_chat_session
from socket_components.message_queue import socket_message_queue
import services.action_run as action_run_services

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
    message = await message_service.create_user_message(message_dto.CreateUserMessage(text=params.text, chat_session_id=chat_session_id_from_token))
    await task_queue.push_generate_bot_message(chat_session_id_from_token)
    return message

class PostActionRequestResponseMessage(BaseModel):
    approved: bool
    action_request_id: int
    action_request_message_id: int
    feedback: Optional[str] = None
    
@router.post('/{chat_id}/action_request_responses')
async def post_action_request_response_message(chat_id: int, params: PostActionRequestResponseMessage, request: Request, has_access = Depends(check_client_session)):
    request = ClientAuthRequest.from_request(request)
    #TODO: should be middleware
    chat_session_id_from_token = jwt_client_auth.decode(request.access_token)
    logger.info(f"chat-session: {chat_session_id_from_token}")
    if await action_request_service.request_has_response(params.action_request_id): #There is already a response to the action
        logger.info("response already exists")
        return
    response = await action_request_service.create_new_response(action_request_dto.CreateActionResponse(feedback=params.feedback, approved=params.approved, next_action_request_id=None, action_run_id=None, action_request_id=params.action_request_id))
    if not response:
        return
    logger.info("sucess!!")
    if response.feedback:
        logger.info("handle feedback")
    elif not response.approved:
        updated_message = await message_service.get_message_by_id(params.action_request_message_id)
        await socket_message_queue.emit_to_client(updated_message.to_socket_message(),[chat_session_id_from_token])
        await task_queue.push_generate_bot_message(chat_session_id_from_token)
    elif response.approved:
        updated_message = await message_service.get_message_by_id(params.action_request_message_id)
        updated_message: ActionRequestMessageSchema
        prev_action_request = updated_message.action_request #TODO: this should be the previous request, so not the one directly on the updated_message
        action_run = await action_run_services.create(dto.CreateActionRun(action_id=prev_action_request.action_id, input=prev_action_request.input, output=None))
        await socket_message_queue.emit_to_client(SocketServerMessageActionRun(action_run=action_run), [chat_session_id_from_token])
        await task_queue.push_run_action(action_run_id=action_run.id, chat_session_id=chat_session_id_from_token)
    return response
    #TODO: some different scenarios
    


