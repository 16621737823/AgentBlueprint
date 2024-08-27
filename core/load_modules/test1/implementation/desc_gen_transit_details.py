from typing import Optional
from pydantic import BaseModel, Field,ConfigDict,model_validator
from data_module import DataInterface

class TransitDetails(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')
    _desc_data : dict
    arrival_stop: str = Field(description="")
    departure_stop: str = Field(description="")
    arrival_time: int = Field(description="")
    departure_time: int = Field(description="")
    travel_method: str = Field(description="")
    stop_count: int = Field(description="")
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
            "arrival_stop": f"TransitDetails's ArrivalStop is {str(self.arrival_stop)}",
            "departure_stop": f"TransitDetails's DepartureStop is {str(self.departure_stop)}",
            "arrival_time": f"TransitDetails's ArrivalTime is {str(self.arrival_time)}",
            "departure_time": f"TransitDetails's DepartureTime is {str(self.departure_time)}",
            "travel_method": f"TransitDetails's TravelMethod is {str(self.travel_method)}",
            "stop_count": f"TransitDetails's StopCount is {str(self.stop_count)}",
        }
    def get_property_from_index(self,index: int)->(any, str):
        if index == 0:
            return self,str(self)
        elif index == 1:
            return self.arrival_stop,str(self.arrival_stop)
        elif index == 2:
            return self.departure_stop,str(self.departure_stop)
        elif index == 3:
            return self.arrival_time,str(self.arrival_time)
        elif index == 4:
            return self.departure_time,str(self.departure_time)
        elif index == 5:
            return self.travel_method,str(self.travel_method)
        elif index == 6:
            return self.stop_count,str(self.stop_count)
class TransitDetailsList(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True, extra='forbid')
    transit_details_list: list[TransitDetails] = Field(description="")
    def __init__(self, **data):
        super().__init__(**data)
    def get_property_from_index(self, index: int)->(any, str):
        list_str = f"{self.__class__.__name__}"
        list_item = list()
        for (i, item) in enumerate(self.transit_details_list):
            item,item_str = item.get_property_from_index(index)
            list_str += f"{i}: {item_str}\n"
            list_item.append(item)
        return list_item,list_str
