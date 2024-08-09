from typing import Optional
from pydantic import BaseModel
from data_module import DataInterface, DataListInterface

class EmojiData(BaseModel,DataInterface):
    _data : dict
    _desc_data : dict
    emoji_description: Optional[str] = None
    emoji_unicode: Optional[str] = None
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
    def to_json_struct(self):
        print(self.model_dump_json())

class EmojiDataList(DataListInterface):
    def __init__(self, data: list):
        super().__init__(data)
