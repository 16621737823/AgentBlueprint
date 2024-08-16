from pydantic import BaseModel, Field,ConfigDict,model_validator
from data_module import DataInterface, DataListInterface

from .desc_gen_emoji_data import EmojiData
class ParsedAction(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')
    _desc_data : dict
    emoji_list: EmojiData = Field(description="")
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
            "emoji_list": f"ParsedAction's EmojiList is {str(self.emoji_list)}",
        }
    def get_property_from_index(self,index: int)->(any, str):
        if index == 0:
            return self,str(self)
        elif index == 1:
            return self.emoji_list,str(self.emoji_list)
    @staticmethod
    def to_dict_struct()->dict[str,any]:
        return ParsedAction.model_json_schema(mode='serialization')

class ParsedActionList(BaseModel,DataListInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True, extra='forbid')
    parsed_action_list: list[ParsedAction] = Field(description="")
    def __init__(self, data: list):
        super().__init__(data)
    @staticmethod
    def to_dict_struct() -> dict[str, any]:
        return ParsedActionList.model_json_schema(mode='serialization')
