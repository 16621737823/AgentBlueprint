from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NodeConnector(_message.Message):
    __slots__ = ("input_data",)
    class InputDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: DataNode
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[DataNode, _Mapping]] = ...) -> None: ...
    INPUT_DATA_FIELD_NUMBER: _ClassVar[int]
    input_data: _containers.MessageMap[int, DataNode]
    def __init__(self, input_data: _Optional[_Mapping[int, DataNode]] = ...) -> None: ...

class TaskNode(_message.Message):
    __slots__ = ("node_id", "node_structure", "function_param")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_STRUCTURE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_PARAM_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    node_structure: NodeConnector
    function_param: FunctionParams
    def __init__(self, node_id: _Optional[int] = ..., node_structure: _Optional[_Union[NodeConnector, _Mapping]] = ..., function_param: _Optional[_Union[FunctionParams, _Mapping]] = ...) -> None: ...

class DataNode(_message.Message):
    __slots__ = ("node_id", "uuid", "node_structure")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    NODE_STRUCTURE_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    uuid: str
    node_structure: NodeConnector
    def __init__(self, node_id: _Optional[int] = ..., uuid: _Optional[str] = ..., node_structure: _Optional[_Union[NodeConnector, _Mapping]] = ...) -> None: ...

class apmFile(_message.Message):
    __slots__ = ("nodes",)
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[TaskNode]
    def __init__(self, nodes: _Optional[_Iterable[_Union[TaskNode, _Mapping]]] = ...) -> None: ...

class FunctionParams(_message.Message):
    __slots__ = ("user_prompt", "system_prompt")
    USER_PROMPT_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_PROMPT_FIELD_NUMBER: _ClassVar[int]
    user_prompt: str
    system_prompt: str
    def __init__(self, user_prompt: _Optional[str] = ..., system_prompt: _Optional[str] = ...) -> None: ...
