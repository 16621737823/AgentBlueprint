import os

import openai
from openai import OpenAI
from pydantic import BaseModel

_struct_template = {
    "type": "json_schema",
    "json_schema": {
        "name": "model_response",
        "schema": {
            "type": "object",
            "properties": {
                "agent_response": {
                    "type": "string",
                    "description": "the response to the instruction"
                },
                # "data_response": need inserts
            },
            "required": ["agent_response", "data_response"],
            "additionalProperties": False,
        },
        "strict": True
    },
}
def add_data_struct_to_template(struct_dict:dict):
    if "$defs" in struct_dict:
        _struct_template["json_schema"]["schema"]["$defs"] = struct_dict["$defs"]
        del struct_dict["$defs"]
    _struct_template["json_schema"]["schema"]["properties"]["data_response"] = struct_dict
    _struct_template["json_schema"]["schema"]["properties"]["data_response"]["description"] = "the structured summarization of the answer above"
    return _struct_template

class FunctionCall:
    def __init__(self,config:dict):
        self.model = config.get("model","gpt-4o-mini")
        self.client = openai.Client(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def run(self,output_struct:dict):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Can you generate some actions based on the  purpose of life?"},
                ],
                response_format=add_data_struct_to_template(output_struct)
            )
            return response
        except Exception as e:
            return e