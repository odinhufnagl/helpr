from abc import ABC, abstractmethod
from typing import List, Optional
from llama_index import BaseDocument, SimpleDirectoryReader, download_loader
from pydantic import BaseModel
from llama_index.readers.base import BaseReader
from llama_index.schema import Document

#TODO: might not be the best name as it collides with llama-index idea of a loader
class BaseLoader(ABC):

    class Credentials(BaseModel):
        pass
    
    credentials: Credentials
    
    @abstractmethod
    async def get_reader(self) -> Optional[BaseReader]:
        pass
    
    @abstractmethod
    async def load_docs(self) -> List[Document]:
        reader = await self.get_reader()
        return reader.load_data()
    
    
class DirectoryLoader(BaseLoader):
    directory: str
    
    async def get_reader(self):
        return SimpleDirectoryReader(self.directory)
    
    
class ApifyLoader(BaseLoader):
    url: str
    
    class Credentials(BaseLoader.Credentials):
        apify_token = "apify_api_fqPckyPjG8xGt5JgGlsqpD148DYkqe3INE0f"
    
    credentials: Credentials
    
    async def get_reader(self): 
         #TODO: this is baaaad, should store the loader in the server and take it from there
         ApifyActor = download_loader('ApifyActor') 
         return ApifyActor(self.credentials.apify_token)

