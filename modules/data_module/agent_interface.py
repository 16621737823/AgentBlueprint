import logging

from . import DataManagerInterface

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
class AgentNetworkInterface:
    def __init__(self):
        self.subscribed_data = []
        self.data_manager = dict()
        self.task_manager = dict()

    def get_data_manager(self,uuid:str,index: int)->DataManagerInterface:
        if uuid in self.data_manager:
            if isinstance(self.data_manager[uuid],dict):
                if index in self.data_manager[uuid]:
                    return self.data_manager[uuid][index]
                else:
                    raise ValueError(f"Data Manager {uuid} has no dataTypeIndex {index}")
            else:
                raise ValueError(f"Data Manager {uuid} is not a dictionary")
        else:
            raise ValueError(f"Invalid uuid from this agent, or uuid is out of date")

    def get_task_manager(self,index: int):
        if index in self.task_manager:
            return self.task_manager[index]
        else:
            raise ValueError("Invalid index from task type")

    def register_tasks(self,tasks:dict):
        self.task_manager.update(tasks)

    def register_data_managers(self,data_uuid:str, data_managers:dict):
        if data_uuid in self.data_manager:
            logger.warning(f"Data Manager {data_uuid} is already registered, overwriting")
        if not isinstance(data_managers,dict):
            raise ValueError("Data Managers must be a dictionary")
        self.data_manager[data_uuid] = data_managers

    def remove_data_manager(self,uuid:str):
        if uuid in self.data_manager:
            del self.data_manager[uuid]
        else:
            raise ValueError(f"Data Manager {uuid} not found")