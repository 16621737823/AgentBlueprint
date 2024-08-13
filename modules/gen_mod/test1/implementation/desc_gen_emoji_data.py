import json
from typing import Optional
from pydantic import BaseModel, Field,ConfigDict
from data_module import DataInterface, DataListInterface

class EmojiData(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)
    _data : dict
    _desc_data : dict
    emoji_description: str = Field(default=None,description="")
    emoji_unicode: str = Field(default=None,description="")
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
            "emoji_description": f"EmojiData's EmojiDescription is {str(self.emoji_description)}",
            "emoji_unicode": f"EmojiData's EmojiUnicode is {str(self.emoji_unicode)}",
        }
    def get_property_from_index(self,index: int)->(any, str):
        if index == 0:
            return self,str(self)
        elif index == 1:
            return self.emoji_description,self.emoji_description
        elif index == 2:
            return self.emoji_unicode,self.emoji_unicode
    @staticmethod
    def to_json_struct()->str:
        return json.dumps(EmojiData.model_json_schema(mode='serialization'), indent=2)

class EmojiDataList(DataListInterface):
    def __init__(self, data: list):
        super().__init__(data)
