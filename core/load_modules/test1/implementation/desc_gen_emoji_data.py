from pydantic import BaseModel
from data_module import DataInterface, DataListInterface

class EmojiData(DataInterface,BaseModel):
    emoji_description: str
    emoji_unicode: str
    def __init__(self, data: dict = None):
        default_prop = {"emoji_description": None,"emoji_unicode": None,}
        default_prop.update(data)
        super().__init__(default_prop)
        self.description_overwrite()
    def description_overwrite(self):
        #def property_name(self):
        #    return f" EmojiData NEW Description is : {self.get_data_str('property_name')}"
        # self.overwrite(property_name)
        return
    def get_property_str_from_index(self,index: int)->(any, str):
        if index == 0:
            return self,self.default_str()
        elif index == 1:
            return self.get("emoji_description"),self.emoji_description
        elif index == 2:
            return self.get("emoji_unicode"),self.emoji_unicode

class EmojiDataList(DataListInterface):
    def __init__(self, data: list):
        super().__init__(data)
