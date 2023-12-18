from abc import ABC, abstractmethod
from pydantic import BaseModel
from llama_index import StorageContext, constr, load_index_from_storage
from llama_index.indices.base import BaseIndex

class BaseIndexLocation(ABC):
    @abstractmethod
    def load_index(self, index_id: str) -> BaseIndex:
        pass
    @abstractmethod
    def store_index(self, index: BaseIndex) -> bool:
        pass

class IndexLocationDir(BaseIndexLocation):
    dir: str
    
    def load_index(self, index_id: str) -> BaseIndex:
        storage_context = StorageContext.from_defaults(persist_dir=self.dir)
        return load_index_from_storage(storage_context, index_id=index_id)
    
    def store_index(self, index: BaseIndex) -> bool:
        index.storage_context.persist(self.dir)
        return True
    