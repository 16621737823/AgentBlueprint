from pydantic import BaseModel, Field, ConfigDict, model_validator

from data_module import DataInterface


class EmojiData(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')
    _desc_data : dict
    emoji_description: str = Field(description="")
    emoji_unicode: str = Field(description="")
    def __str__(self):
        return "".join(self._desc_data[key] + "." for key in self.model_fields.keys() if getattr(self,key) is not None).strip(".")
    def get_str(self,key:str):
        if getattr(self,key) is not None:
            return self._desc_data[key]
        else:
            return ""


# Define the subclass with a reference to the base model
class ParsedAction(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')
    _desc_data : dict
    emoji_list: EmojiData = Field(description="")
    def __str__(self):
        return "".join(self._desc_data[key] + "." for key in self.model_fields.keys() if getattr(self,key) is not None).strip(".")
    def get_str(self,key:str):
        if getattr(self,key) is not None:
            return self._desc_data[key]
        else:
            return ""

    @model_validator(mode='after')
    def _init_desc_data(self):
        # Can be overriden to add more description
        self._desc_data = {
            "emoji_list": f"ParsedAction's EmojiList is {str(self.emoji_list)}",
        }

    def get_property_from_index(self, index: int) -> (any, str):
        if index == 0:
            return self, str(self)
        elif index == 1:
            return self.emoji_list, self.emoji_list

    @staticmethod
    def to_dict_struct() -> dict[str, any]:
        return ParsedAction.model_json_schema(mode='serialization')

a = EmojiData(emoji_description="test", emoji_unicode="test")
b = ParsedAction(emoji_list=a)

print(b.emoji_list)    # Outputs: Bob (the original Person instance is updated)
