from hmac import new
from typing import Any, Coroutine, List, Optional
from openai import OpenAI
from pydantic import BaseModel
from helpr.index.loader import BaseLoader
from helpr.index.location import BaseIndexLocation
from llama_index import Document, GPTVectorStoreIndex, LLMPredictor, PromptHelper, StorageContext, constr, load_index_from_storage
from llama_index.indices.base import BaseIndex

class Index(BaseIndex):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
      
    @staticmethod  
    async def load_from_location(index_location: BaseIndexLocation, index_id: str):
        return index_location.load_index(index_id)
         
    async def train(self, loaders: List[BaseLoader]):
        docs = []
        for loader in loaders:
            new_docs = await loader.load_docs()
            docs += new_docs
        self.insert(docs)
        return True
    
    async def to_location(self, index_location: BaseIndexLocation):
        index_location.store_index(self)
        
    async def construct() -> 'Index':
        pass

        
class ChatIndex(Index, GPTVectorStoreIndex):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 1
    chunk_size_limit = 600
    open_ai_temperature = 0.7
    model_name = "text-davinci-003"

    @classmethod
    def construct_default(cls, default_documents: List[Document] = []) -> 'ChatIndex':
        prompt_helper = PromptHelper(cls.max_input_size, cls.num_outputs, cls.max_chunk_overlap, chunk_size_limit=cls.chunk_size_limit)
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=cls.open_ai_temperature, model_name=cls.model_name, max_tokens=cls.num_outputs))
        return ChatIndex(documents=default_documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)