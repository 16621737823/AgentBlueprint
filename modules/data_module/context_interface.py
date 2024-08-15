import threading
from typing import Optional, Any, Dict

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from pydantic._internal._model_construction import ModelMetaclass
from pydantic.dataclasses import dataclass
from .data_interface import DataInterface,DataListInterface
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

class DataInstanceContext(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    parent_context: Optional["DataInstanceContext"] = None
    children_context: Optional[list["DataInstanceContext"]] = []
    reference_context: Optional["DataInstanceContext"] = None
    # callback: EventChannel = None
    # TODO: should connect to DataTrigger instead of function Query, use for POC only
    data_reference_id: int = 0
    _lock: threading.Lock = PrivateAttr(default_factory=threading.Lock)
    def get_previous_context(self,target_index:int):
        if self.data_reference_id == target_index:
            return self
        if self.parent_context is not None:
            return self.parent_context.get_previous_context(target_index)
        else:
            raise ValueError("No context with the specified task_id found")
    def try_lock(self):
        return self.lock.acquire(blocking=False)
    def release_lock(self):
        self.lock.release()

class QueryContext(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    usr_prompt: Optional[str] = ""
    usr_input_data: Optional[Dict[int, DataInterface or DataListInterface]] = None
    context_root: DataInstanceContext = None
    root_cache: Optional[Dict[int, DataInterface or DataListInterface]] = None
    response: Optional[Any] = None

class DataNodeContext(QueryContext):
    param_data: Optional[Dict[int,Any]] = None
    source_index: Optional[int] = 0
    parent_context: QueryContext = None

    def __getattribute__(self, item):
        if item == "usr_prompt" or item == "usr_input_data" or item == "root_cache" or item == "response" or item == "context_root":
            parent = super().__getattribute__("parent_context")
            if parent is None:
                raise AttributeError(f"Parent Query context not found for {self}")
            return parent.__getattribute__(item)
        return super().__getattribute__(item)


class FunctionNodeContext(QueryContext):
    task_id: int = 0
