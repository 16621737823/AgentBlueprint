from data_module.agent_interface import AgentInterface
from data_module.context_interface import QueryContext
from data_module.data_interface import DataInterface


class BaseDataManager:
    def __init__(self):
        pass

    def get_descriptor(self, desc_index:int, d:AgentInterface, ctx:QueryContext) -> DataInterface:
        raise NotImplementedError

    def set_service_response(self, response:DataInterface, ctx:QueryContext):
        raise NotImplementedError
