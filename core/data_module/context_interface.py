from . import *
from enum import Enum
import threading


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
        self.usr_prompt = ""
        self.param_data = dict()
        self.usr_input_data = dict()
        self.target_index = 0
        self.context_root = None
        self.root_cache = dict()
        self.response = None
    def set_response(self,response):
        self.response = response
    def set_cache(self,key:int,value:DataInterface or DataListInterface):
        self.root_cache[key] = value
    def get_cache(self,key)->DataInterface or DataListInterface:
        return self.root_cache.get(key,None)
    def set_param_data(self, key:int, value):
        self.param_data[key] = value
    def get_param_data(self, key:int):
        return self.param_data.get(key, None)
    def set_usr_input_data(self, key:int, value: DataInterface or DataListInterface):
        self.usr_input_data[key] = value
    def get_usr_input_data(self, key:int)-> DataInterface or DataListInterface:
        return self.usr_input_data.get(key, None)



class DataNodeContext(QueryContext):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        if "reference" in kwargs:
            if isinstance(kwargs['reference'],(DataInterface,DataListInterface)):
                self.reference = kwargs['reference']
            else:
                raise ValueError("reference must be an instance of DataInterface or DataListInterface")

        if "param_data" in kwargs:
            if isinstance(kwargs['param_data'],dict):
                self.param_data = kwargs['param_data']
            else:
                raise ValueError("param_data must be an instance of dict")

        if "parent_context" in kwargs:
            if isinstance(kwargs['parent_context'], DataInstanceContext):
                self.parent_context = kwargs['parent_context']
            else:
                raise ValueError("parent_context must be an instance of DataInstanceContext")
        else:
            raise ValueError("parent_context is required")

        self.usr_prompt = self.parent_context.usr_prompt
        self.usr_input_data = self.parent_context.usr_input_data
        self.root_cache = self.parent_context.root_cache
        self.target_index = self.parent_context.target_index
        self.context_root = self.parent_context.context_root
        self.response = self.parent_context.response
    def __getitem__(self, item):
        if item == "reference":
            return self.reference
        else:
            return self.parent_context[item]






class FunctionNodeContext(QueryContext):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        if 'usr_prompt' in kwargs:
            if isinstance(kwargs['usr_prompt'],str):
                self.usr_prompt = kwargs['usr_prompt']
            else:
                raise ValueError("usr_prompt must be a string")
        if "usr_input_data" in kwargs:
            if isinstance(kwargs['usr_input_data'],dict):
                self.usr_input_data = kwargs['usr_input_data']
            else:
                raise ValueError("usr_input_data must be an instance of dict")
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


