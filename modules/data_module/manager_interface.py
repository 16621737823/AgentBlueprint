
from .context_interface import QueryContext
from .data_interface import DataInterface, DataListInterface
class DataManagerInterface:
    def __init__(self):
        print(self.__class__.__name__ + " is initialized")
        pass

    def get_descriptor(self, desc_index:int, ctx:QueryContext) -> DataInterface:
        raise NotImplementedError

    def set_service_response(self, response:DataInterface, ctx:QueryContext):
        raise NotImplementedError

def get_manager(index:int):
    return