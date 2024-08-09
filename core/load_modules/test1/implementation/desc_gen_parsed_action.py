from pydantic import BaseModel
from data_module import DataInterface, DataListInterface

class ParsedAction(DataInterface,BaseModel):
    from .desc_gen_emoji_data import EmojiData
    emoji_list: EmojiData
    def __init__(self, data: dict = None):
        default_prop = {"emoji_list": None,}
        default_prop.update(data)
        super().__init__(default_prop)
        self.description_overwrite()
    def description_overwrite(self):
        #def property_name(self):
        #    return f" ParsedAction NEW Description is : {self.get_data_str('property_name')}"
        # self.overwrite(property_name)
        return
    def get_property_str_from_index(self,index: int)->(any, str):
        if index == 0:
            return self,self.default_str()
        elif index == 1:
            return self.get("emoji_list"),self.emoji_list

class ParsedActionList(DataListInterface):
    def __init__(self, data: list):
        super().__init__(data)
