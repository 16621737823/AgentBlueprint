import threading
from typing import Optional, Any, Dict, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from pydantic._internal._model_construction import ModelMetaclass
from pydantic.dataclasses import dataclass
from .data_interface import DataInterface
from enum import Enum



class ContextState(Enum):
    INITIALIZED = 0,
    IN_PROGRESS = 1,
    ACTIVE = 2,
    COMPLETED = 3,
    INTERRUPTED = 4,
    BACKLOGGED = 5,
    ERROR = -1

class AllOptional(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)

class QueryResult(BaseModel):
    class Config:
        arbitrary_types_allowed = True
    #TODO for now every query creates a new datainstancecontext, but we can override to the previous one
    data_instance: "DataInstanceContext" = None
    source_query_context: "QueryContext" = None
    #data_type_index: int = 0 #seems that we dont have to specify which of the certain type of data is being referred to
    cached_data: DataInterface = None



class SessionContext(BaseModel):
    query_result: Optional[Dict[int, QueryResult]] = {}
    def get_cached_data(self, target_index:int)-> DataInterface:
        if self.query_result is not None and target_index in self.query_result:
            return self.query_result[target_index].cached_data
        else:
            raise ValueError(f"No reference context found for {target_index}")

class DataInstanceContext(BaseModel):
    class Config:
        arbitrary_types_allowed = True
    parent_context: Optional["DataInstanceContext"] = None
    children_context: Optional[list["DataInstanceContext"]] = []
    reference_context: Optional["DataInstanceContext"] = None
    # callback: EventChannel = None
    _lock: threading.Lock = PrivateAttr(default_factory=threading.Lock)
    def try_lock(self):
        return self.lock.acquire(blocking=False)
    def release_lock(self):
        self.lock.release()

class QueryContext(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    usr_prompt: Optional[str] = ""
    usr_input_data: Optional[Dict[int, DataInterface]] = None
    # context_root: DataInstanceContext = None # converged with session_ctx
    root_cache: Optional[Dict[int, DataInterface]] = {}
    session: SessionContext = None
    # response: Optional[Any] = None # equivalent to cached_data in QueryResult
    def get_reference_context(self, target_index:int)->DataInterface :
        if self.session != None:
            return self.session.get_cached_data(target_index)
        else:
            raise ValueError("No session context found")


class DataNodeContext(QueryContext):
    param_data: Optional[Dict[int,Tuple[Any,str]]] = {}
    source_index: Optional[int] = 0
    parent_context: QueryContext = None

    def __getattribute__(self, item):
        if item == "usr_prompt" or item == "usr_input_data" or item == "root_cache" or item == "response" or item == "context_root" or item == "session":
            parent = super().__getattribute__("parent_context")
            if parent is None:
                raise AttributeError(f"Parent Query context not found for {self}")
            return parent.__getattribute__(item)
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if key == "usr_prompt" or key == "usr_input_data" or key == "root_cache" or key == "response" or key == "context_root" or key == "session":
            parent = super().__getattribute__("parent_context")
            if parent is None:
                raise AttributeError(f"Parent Query context not found for {self}")
            return parent.__setattr__(key,value)
        return super().__setattr__(key,value)


class FunctionNodeContext(QueryContext):
    task_id: int = 0
    def set_query_response(self, response_data:DataInterface ):
        if self.session is not None:
            self.session.query_result[self.task_id] = QueryResult(data_instance=DataInstanceContext(),source_query_context=self,cached_data=response_data)
        else:
            raise ValueError("No session context found")


