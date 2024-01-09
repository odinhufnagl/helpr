from typing import List, Literal, Optional
from pydantic import BaseModel
from helpr.action.base import AddAction, BaseAction, PrintAction
from helpr.schemas.action_request import ActionRequestResponseSchema, ActionRequestSchema
from helpr.schemas.action_run import ActionRunSchema
from schemas.message import ActionRequestMessageSchema, ActionResultMessageSchema, BotMessageSchema, MessageSchema, UserMessageSchema



class ChatAgentMessage(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    # TODO: add the rest

    @staticmethod
    def from_schema(schema: MessageSchema) -> 'ChatAgentMessage':
        if isinstance(schema, BotMessageSchema):
            return BotChatAgentMessage(text=schema.text)
        if isinstance(schema, UserMessageSchema):
            return UserChatAgentMessage(text=schema.text)
        if isinstance(schema, ActionRequestMessageSchema):
            return ActionRequestAgentMessage.from_action_request_schema(schema.action_request)
        if isinstance(schema, ActionResultMessageSchema):
            return ActionResultMessage(output=schema.output, action=BaseAction.from_schema(schema.action))

    @staticmethod
    def from_schemas(schemas: List[MessageSchema]):
        return list(map(lambda s: ChatAgentMessage.from_schema(s), schemas))


class UserChatAgentMessage(ChatAgentMessage):

    text: str


class SystemChatAgentMessage(ChatAgentMessage):

    text: str


class BotChatAgentMessage(ChatAgentMessage):

    text: str


class ActionRequestAgentMessage(ChatAgentMessage):
    class Config:
        arbitrary_types_allowed = True
    text: Optional[str]
    action: Optional[BaseAction]
    input: BaseAction.Input | str  # TODO: should not be allowed to be str
    response: Optional['ActionRequestResponseAgentMessage'] = None

    def from_action_request_schema(schema: ActionRequestSchema):
        return ActionRequestAgentMessage(text=None, action=BaseAction.from_schema(schema.action), input=schema.input, response=ActionRequestResponseAgentMessage.from_action_request_response_schema(schema.response) if schema.response else None)


class ActionRequestResponseAgentMessage(ChatAgentMessage):
    feedback: Optional[str] = None
    approved: bool
    action_result: Optional['ActionResultMessage'] = None
    next_action_request: Optional['ActionRequestAgentMessage'] = None

    def from_action_request_response_schema(schema: ActionRequestResponseSchema):
        return ActionRequestResponseAgentMessage(action_result=ActionResultMessage.from_action_run_schema(schema.action_run) if schema.action_run else None, approved=schema.approved, feedback=schema.feedback, next_action_request=ChatAgentMessage.from_schema(schema.next_action_request) if schema.next_action_request else None)


class ActionResultMessage(ChatAgentMessage):
    output: BaseAction.Output | str  # TODO: should not be allowed to be str
    action: Optional[BaseAction]

    def from_action_run_schema(schema: ActionRunSchema):
        return ActionResultMessage(output=schema.output, action=BaseAction.from_schema(schema.action))


class ActionResultSummaryMessage(ChatAgentMessage):

    action_result: ActionResultMessage
    text: str