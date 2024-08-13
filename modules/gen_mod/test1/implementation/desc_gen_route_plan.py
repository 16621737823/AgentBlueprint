import json
from typing import Optional
from pydantic import BaseModel, Field,ConfigDict
from data_module import DataInterface, DataListInterface

class RoutePlan(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)
    _data : dict
    _desc_data : dict
    action_description: str = Field(default=None,description="")
    duration: int = Field(default=None,description="")
    start_time: int = Field(default=None,description="")
    end_time: int = Field(default=None,description="")
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
    @staticmethod
    def to_json_struct()->str:
        return json.dumps(RoutePlan.model_json_schema(mode='serialization'), indent=2)

class RoutePlanList(DataListInterface):
    def __init__(self, data: list):
        super().__init__(data)
