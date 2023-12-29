from abc import ABC, abstractmethod
from pydantic import BaseModel
from llama_index import StorageContext, load_index_from_storage


from helpr.index.base import Index

class BaseIndexLocation(ABC, BaseModel):
    @abstractmethod
    def load_index(self, index_id: str) -> Index:
        pass
    @abstractmethod
    def store_index(self, index: Index) -> bool:
        pass
    @abstractmethod
    def from_db_index_location(db_index) -> 'BaseIndexLocation':
        pass
    
class IndexLocationDir(BaseIndexLocation):
    dir: str
    
    def load_index(self, index_id: str) -> Index:
        storage_context = StorageContext.from_defaults(persist_dir=self.dir)
        return load_index_from_storage(storage_context)

    
    def store_index(self, index: Index) -> bool:
        index.storage_context.persist(self.dir)
        return True
    
    def from_db_index_location(db_index) -> 'IndexLocationDir':
        #TODO: just temporary
        return IndexLocationDir(dir=db_index)

    