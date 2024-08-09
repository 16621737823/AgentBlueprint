from typing import Optional
from pydantic import BaseModel
from data_module import DataInterface, DataListInterface

class RoutePlan(BaseModel,DataInterface):
    _data : dict
    _desc_data : dict
    action_description: Optional[str] = None
    duration: Optional[int] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    def __init__(self, data: dict):
        super().__init__(**data)
        self._init_desc_data()
    def __str__(self):
        return "".join(self._desc_data[key] + "." for key in self._data.keys() if self._data[key] is not None).strip(".")
    def get_str(self,key:str):
        if getattr(self,key) is not None:
            return self._desc_data[key]
        else:
            return ""
    def _init_desc_data(self):
        #Can be overriden to add more description
        self._desc_data = {
            "action_description": f"RoutePlan's ActionDescription is {str(self.action_description)}",
            "duration": f"RoutePlan's Duration is {str(self.duration)}",
            "start_time": f"RoutePlan's StartTime is {str(self.start_time)}",
            "end_time": f"RoutePlan's EndTime is {str(self.end_time)}",
        }
    def get_property_from_index(self,index: int)->(any, str):
        if index == 0:
            return self,str(self)
        elif index == 1:
            return self.action_description,self.action_description
        elif index == 2:
            return self.duration,self.duration
        elif index == 3:
            return self.start_time,self.start_time
        elif index == 4:
            return self.end_time,self.end_time
    def to_json_struct(self):
        print(self.model_dump_json())

class RoutePlanList(DataListInterface):
    def __init__(self, data: list):
        super().__init__(data)
