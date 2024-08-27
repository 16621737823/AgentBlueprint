from typing import Optional
from pydantic import BaseModel, Field,ConfigDict,model_validator
from data_module import DataInterface

from typing import List
class Calendar(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')
    _desc_data : dict
    summary: str = Field(description="")
    location: str = Field(description="")
    description: str = Field(description="")
    start_time: int = Field(description="")
    end_time: int = Field(description="")
    attendees: List[str] = Field(description="")
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
            "summary": f"Calendar's Summary is {str(self.summary)}",
            "location": f"Calendar's Location is {str(self.location)}",
            "description": f"Calendar's Description is {str(self.description)}",
            "start_time": f"Calendar's StartTime is {str(self.start_time)}",
            "end_time": f"Calendar's EndTime is {str(self.end_time)}",
            "attendees": f"Calendar's attendees is {str(self.attendees)}",
        }
    def get_property_from_index(self,index: int)->(any, str):
        if index == 0:
            return self,str(self)
        elif index == 1:
            return self.summary,str(self.summary)
        elif index == 2:
            return self.location,str(self.location)
        elif index == 3:
            return self.description,str(self.description)
        elif index == 4:
            return self.start_time,str(self.start_time)
        elif index == 5:
            return self.end_time,str(self.end_time)
        elif index == 6:
            return self.attendees,str(self.attendees)
class CalendarList(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True, extra='forbid')
    calendar_list: list[Calendar] = Field(description="")
    def __init__(self, **data):
        super().__init__(**data)
    def get_property_from_index(self, index: int)->(any, str):
        list_str = f"{self.__class__.__name__}"
        list_item = list()
        for (i, item) in enumerate(self.calendar_list):
            item,item_str = item.get_property_from_index(index)
            list_str += f"{i}: {item_str}\n"
            list_item.append(item)
        return list_item,list_str
