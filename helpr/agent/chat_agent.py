from typing import List, Literal, Optional
from numpy import isin
from helpr.action.action_registry import ActionRegistry
from .chat_agent_message import *
from helpr.services.action import get_actions_in_chat
from index.base import Index
from llama_index.llms.types import ChatMessage, MessageRole
from index.location import BaseIndexLocation, IndexLocationDir
from llama_index.tools import ToolOutput
from llama_index.chat_engine.types import AGENT_CHAT_RESPONSE_TYPE
from llama_index.tools import FunctionTool


class ChatEngineMessage(ChatMessage):
    @staticmethod
    def from_chat_message(msg: ChatAgentMessage):
        if isinstance(msg, UserChatAgentMessage):
            return ChatEngineMessage(role=MessageRole.USER, content=msg.text)
        if isinstance(msg, BotChatAgentMessage):
            return ChatEngineMessage(role=MessageRole.ASSISTANT, content=msg.text)
        if isinstance(msg, SystemChatAgentMessage):
            return ChatEngineMessage(role=MessageRole.SYSTEM, content=msg.text)
        if isinstance(msg, ActionRequestAgentMessage):
            # TODO: this should also be done with some generator
            return ChatEngineMessage(role=MessageRole.ASSISTANT, content=f"text: {msg.text}, function: {msg.action.name} with input: {msg.input}")
        if isinstance(msg, ActionRequestResponseAgentMessage):
            # TODO: for example this should match how the text looks when we put it as input_text so it should come from same generator
            if msg.feedback:
                # TODO: this must probably be changed so it is connected to the action_request
                return ChatEngineMessage(role=MessageRole.USER, content=f'feedback: {msg.feedback} to the action')
            if msg.approved:
                return ChatEngineMessage(role=MessageRole.USER, content=f'I approve of the action')
            if not msg.approved:
                return ChatEngineMessage(role=MessageRole.USER, content=f'I do not approve the action')
        if isinstance(msg, ActionResultMessage):
            # TODO: should function response come from system?
            return ChatEngineMessage(role=MessageRole.ASSISTANT, content=f'result: {msg.output} to action: {msg.action.name}')
        if isinstance(msg, ActionResultSummaryMessage):
            return ChatEngineMessage(role=MessageRole.SYSTEM, content=msg.text)

    def from_chat_messages(messages: List[ChatAgentMessage]) -> List['ChatEngineMessage']:
        engine_messages: List[ChatEngineMessage] = []
        for message in messages:
            if isinstance(message, ActionRequestAgentMessage):
                engine_messages.append(ChatEngineMessage.from_chat_message(message))
                if message.response:
                    engine_messages.append(ChatEngineMessage.from_chat_message(message.response))
            else:
                engine_messages.append(ChatEngineMessage.from_chat_message(message))
        return engine_messages

class ChatAgent:

    def __init__(self, index: Index, prompt: str, message_history: List[ChatAgentMessage], action_registry: ActionRegistry) -> None:
        self.index = index
        # TODO: if this ChatAgent should be able to have its own implementations so its quite modular, it shuoldnt take in the prompt right? Because the prompt
        # might be different for another chat_agent, and right now we have tried to make the messages as abstract as possible (not linked to the logic of the chat-function)
        # Or maybe just switch lane and build everything with the idea that we are using llama. Maybe not the best best, but will improve the flow in some ways
        self.prompt = prompt
        self.message_history = message_history
        self.action_registry = action_registry

    # TODO: put in utils?
    @staticmethod
    def actions_to_tools(action_registry: ActionRegistry) -> List[FunctionTool]:
        tools = []
        for action in action_registry.get_actions():
            if action.feedback_required:

                tool = FunctionTool.from_defaults(
                    fn=action.empty_run, description=action.description, name=action.name)
            else:
                tool = FunctionTool.from_defaults(
                    fn=action.run, description=action.description, name=action.name)
            tools.append(tool)
        return tools

    def parse_chat_response(self, response: AGENT_CHAT_RESPONSE_TYPE) -> List[ChatAgentMessage]:
        responses = []
        sources = response.sources
        for source in sources:
            if isinstance(source, ToolOutput):
                action = self.action_registry.get(source.tool_name)
                k = source.raw_input['kwargs']
                i = action.Input(**k)
                if not action:
                    return responses
                if action.feedback_required: 
                    message = ActionRequestAgentMessage(
                        text=response.response, action=action,  input=i)
                    responses.append(message)
                    return responses
                else:
                    responses.append(ActionResultMessage(
                        action=action, output=source.raw_output))
        responses.append(BotChatAgentMessage(text=response.response))

        return responses
    
    
    async def chat(self) -> List[ChatAgentMessage]:
        created_messages: List[ChatAgentMessage] = []
        if len(self.message_history) == 0:
            return []
        chat_history: List[ChatEngineMessage] = ChatEngineMessage.from_chat_messages(
            self.message_history)
        latest_message = chat_history[-1]
        rest_of_messages = chat_history[:-1]
        tools = self.actions_to_tools(
            self.action_registry)
        chat_engine = self.index.as_chat_engine(
            system_prompt=self.prompt, tools=tools)
        if latest_message.role != MessageRole.ASSISTANT:
            input_text = latest_message.content
            response = chat_engine.chat(input_text, chat_history=rest_of_messages)
            new_messages = self.parse_chat_response(response)
            created_messages += new_messages
            self.message_history += created_messages
            return created_messages
        else:
            return []

    def update_message_history(self, new_message_history):
        self.message_history = new_message_history

