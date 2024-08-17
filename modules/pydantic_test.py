
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ValidationError, ConfigDict, create_model, Field

class EmojiData(BaseModel):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True, extra='forbid')

    emoji_description: str = Field(description="")
    emoji_unicode: str = Field(description="")
    def __init__(self,**data):
        super().__init__(**data)
class ParsedAction(BaseModel):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True, extra='forbid')

    emoji_list: Optional[EmojiData] = Field(description="")
    def __init__(self,**data):
        super().__init__(**data)
class ParsedActionList(BaseModel):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True, extra='forbid')

    parsed_action_list: List[ParsedAction] = Field(..., description="A list of parsed actions")
    def __init__(self,**data):
        super().__init__(**data)
        # self._init_desc_data()

ResponseModel = create_model(
    "ResponseModel",
    agent_response=(str, Field(..., description="the response to the instruction")),
    data_response=(Optional[ParsedActionList], Field(..., description="the structured summarization of the answer above")),
    model_config =ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')
)


m = ResponseModel.model_validate_json('{"agent_response":"Here is the processed response based on the provided details.","data_response":{"parsed_action_list":[{"emoji_list":{"emoji_description":"test_emoji_desc","emoji_unicode":"test_emoji_unicode"}},{"emoji_list":null}]}}')
print(m)
#> id=123 name='James' signup_ts=None
