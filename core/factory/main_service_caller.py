import os
from typing import Optional

import openai
from pydantic import Field, create_model, ConfigDict

ResponseModel = config = {}
model = config.get("model","gpt-4o-mini")
client = openai.Client(
    api_key=os.getenv("OPENAI_API_KEY")
)
_struct_template = {
    "type": "json_schema",
    "json_schema": {
        "name": "model_response",
        "strict": True
    },
}
def create_response_model(nested_cls, **kwargs):
    return create_model(
    "ResponseModel",
    agent_response=(str, Field(..., description="the response to the instruction")),
    data_response=(Optional[nested_cls], Field(..., description="the structured summarization of the answer above")),
    model_config =ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')
)
def extract_data(data:str,nested_cls):
    response_model = create_response_model(nested_cls).model_validate_json(data)
    struct_data = response_model
    return struct_data.data_response
def add_data_struct_to_template(struct_dict:dict):
   _struct_template["json_schema"]["schema"]= struct_dict
   _struct_template["json_schema"]["strict"]= True
   return _struct_template

def main_servicer_caller(context:dict,output_struct):
    try:
        response_struct = create_response_model(output_struct)
        struct = add_data_struct_to_template(response_struct.model_json_schema(mode='serialization'))
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": context["system"]},
                {"role": "user", "content": context["prompt"]},
            ],
            response_format=struct,
        )
        print(response)
        return response.choices[0].message.content
    except Exception as e:
        return e