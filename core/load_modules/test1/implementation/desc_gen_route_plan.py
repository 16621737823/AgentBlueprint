from typing import Optional
from pydantic import BaseModel, Field,ConfigDict,model_validator
from data_module import DataInterface

class RoutePlan(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')
    _desc_data : dict
    action_description: str = Field(description="")
    duration: int = Field(description="")
    start_time: int = Field(description="")
    end_time: int = Field(description="")
    def __init__(self,**data):
        super().__init__(**data)
        self._init_desc_data()
    def __str__(self):
        return "".join(self._desc_data[key] + "." for key in self.model_fields.keys() if getattr(self,key) is not None).strip(".")
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
            return self.action_description,str(self.action_description)
        elif index == 2:
            return self.duration,str(self.duration)
        elif index == 3:
            return self.start_time,str(self.start_time)
        elif index == 4:
            return self.end_time,str(self.end_time)
class RoutePlanList(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True, extra='forbid')
    route_plan_list: list[RoutePlan] = Field(description="")
    def __init__(self, **data):
        super().__init__(**data)
    def get_property_from_index(self, index: int)->(any, str):
        list_str = f"{self.__class__.__name__}"
        list_item = list()
        for (i, item) in enumerate(self.route_plan_list):
            item,item_str = item.get_property_from_index(index)
            list_str += f"{i}: {item_str}\n"
            list_item.append(item)
        return list_item,list_str
