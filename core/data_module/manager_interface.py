
from .context_interface import QueryContext, DataNodeContext
from .data_interface import DataInterface, DataListInterface
class DataManagerInterface:
    def __init__(self):
        print(self.__class__.__name__ + " is initialized")
        pass

    @staticmethod
    def get_descriptor(desc_index:int, ctx:DataNodeContext) -> DataInterface or DataListInterface:
        raise NotImplementedError

    @staticmethod
    def get_class()->DataInterface:
        raise NotImplementedError

    @staticmethod
    def get_class_list()->DataListInterface:
        raise NotImplementedError

    @staticmethod
    def set_service_response(response:DataInterface, ctx:QueryContext):
        raise NotImplementedError

def get_manager(index:int):
    return