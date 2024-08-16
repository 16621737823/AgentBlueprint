from pydantic import BaseModel, Field, ConfigDict, model_validator

from data_module import DataInterface

class EmojiData(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')
    _desc_data : dict
    emoji_description: str = Field(description="")
    emoji_unicode: str = Field(description="")

    def __init__(self,**data):
        super().__init__(**data)

    def init_desc_data(self):
        pass
        #Can be overriden to add more description




# Define the subclass with a reference to the base model
class ParsedAction(BaseModel,DataInterface):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')
    _desc_data : dict
    emoji_list: EmojiData = Field(description="")


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
