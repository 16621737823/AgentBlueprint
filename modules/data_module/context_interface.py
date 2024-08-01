from data_interface import DataInterface, DataListInterface
from enum import Enum
import threading

from events import EventChannel

class ContextState(Enum):
    INITIALIZED = 0,
    IN_PROGRESS = 1,
    ACTIVE = 2,
    COMPLETED = 3,
    INTERRUPTED = 4,
    BACKLOGGED = 5,
    ERROR = -1

class DataInstanceContext:
    def __init__(self,**kwargs):
        if "parent_context" in kwargs:
            if isinstance(kwargs['parent_context'],DataInstanceContext):
                self.parent_context = kwargs['parent_context']
            else:
                raise ValueError("parent_context must be an instance of DataInstanceContext")
        if "children_context" in kwargs:
            if isinstance(kwargs['children_context'],list):
                if all(isinstance(item,DataInstanceContext) for item in kwargs['children_context']):
                    self.children_context = kwargs['children_context']
                else:
                    raise ValueError("All elements in children_context must be instances of DataInstanceContext")
            else:
                raise ValueError("children_context must be a list")
        if "reference_context" in kwargs:
            if isinstance(kwargs['reference_context'],DataInstanceContext):
                self.reference_context = kwargs['reference_context']
            else:
                raise ValueError("reference_context must be an instance of DataNodeContext")
        if "events" in kwargs:
            if isinstance(kwargs['events'], EventChannel):
                self.callback = kwargs['callback']
            else:
                raise ValueError("events must be a EventChannel")
        self.lock = threading.Lock()
    def try_lock(self):
        return self.lock.acquire(blocking=False)
    def release_lock(self):
        self.lock.release()

class QueryContext:
    def __init__(self,**kwargs):
        pass





class DataNodeContext(QueryContext):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        if "reference" in kwargs:
            if isinstance(kwargs['reference'],(DataInterface,DataListInterface)):
                self.reference = kwargs['reference']
            else:
                raise ValueError("reference must be an instance of DataInterface or DataListInterface")
        if "parent_context" in kwargs:
            if isinstance(kwargs['parent_context'],DataInstanceContext):
                self.parent_context = kwargs['parent_context']
            else:
                raise ValueError("parent_context must be an instance of DataInstanceContext")
        else:
            raise ValueError("parent_context is required")
    def __getitem__(self, item):
        if item == "reference":
            return self.reference
        else:
            return self.parent_context[item]



class FunctionNodeContext(QueryContext):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        if 'input_text' in kwargs:
            if isinstance(kwargs['input_text'],str):
                self.input_text = kwargs['input_text']
            else:
                raise ValueError("input_text must be a string")
        if "input_data" in kwargs:
            if isinstance(kwargs['input_data'],(DataInterface,DataListInterface)):
                self.input_data = kwargs['input_data']
            else:
                raise ValueError("input_data must be an instance of DataInterface or DataListInterface")
        if "root_cache" in kwargs:
            if isinstance(kwargs['root_cache'],dict):
                self.root_cache = kwargs['root_cache']
            else:
                raise ValueError("root_cache must be a dictionary")
        if "target_index" in kwargs:
            if isinstance(kwargs['target_index'],int):
                self.target_index = kwargs['target_index']
            else:
                raise ValueError("target_index must be an integer")
        if "context_root" in kwargs:
            if isinstance(kwargs['context_root'],DataInstanceContext):
                self.context_root = kwargs['context_root']
            else:
                raise ValueError("context_root must be an instance of DataInstanceContext")

