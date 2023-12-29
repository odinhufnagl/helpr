from hmac import new
from typing import Any, Coroutine, List, Optional
from dotenv import load_dotenv
from langchain import OpenAI
from pydantic import BaseModel
from helpr.index.loader import BaseLoader

from llama_index import Document, LLMPredictor, PromptHelper, ServiceContext
import os


import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Sequence, Type, TypeVar, cast

from llama_index.chat_engine.types import BaseChatEngine, ChatMode
from llama_index.core import BaseQueryEngine, BaseRetriever
from llama_index.data_structs.data_structs import IndexStruct
from llama_index.ingestion import run_transformations
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_utils import is_function_calling_model
from llama_index.schema import BaseNode, Document
from llama_index.service_context import ServiceContext
from llama_index.storage.docstore.types import BaseDocumentStore, RefDocInfo
from llama_index.storage.storage_context import StorageContext
from llama_index import VectorStoreIndex
from llama_index.indices.base import BaseIndex


class Index(BaseIndex):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
         
    async def train(self, loaders: List[BaseLoader]):
        docs = []
        for loader in loaders:
            new_docs = await loader.load_docs()
            docs += new_docs
        self.insert(docs)
        return True
    



 
class ChatIndex(Index, VectorStoreIndex):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 1
    chunk_size_limit = 600
    open_ai_temperature = 0.7
    model_name = "text-davinci-003"

    @classmethod
    def construct_default(cls, default_documents: List[Document] = []) -> 'ChatIndex':
        load_dotenv()

        prompt_helper = PromptHelper(cls.max_input_size, cls.num_outputs, cls.max_chunk_overlap, chunk_size_limit=cls.chunk_size_limit)
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=cls.open_ai_temperature, model_name=cls.model_name, max_tokens=cls.num_outputs))
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        return ChatIndex.from_documents(service_context=service_context, documents=default_documents)