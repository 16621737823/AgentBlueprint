import importlib
import json
import os

import openai
from dotenv import load_dotenv

import load_modules.test1.implementation
from agent.agent_instance import AgentNetwork

load_dotenv()
agent = AgentNetwork()
agent.check_version_file("load_modules/version.txt")
mgr = agent.get_data_manager("16308260-594f-11ef-a2df-047c168941e2", 1003)
struct_json = mgr.get_class_list().to_dict_struct()
print(struct_json)
resp_fmt = {
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
if "$defs" in struct_json:
    resp_fmt["json_schema"]["schema"]["$defs"] = struct_json["$defs"]
    del struct_json["$defs"]
resp_fmt["json_schema"]["schema"]["properties"]["data_response"] = struct_json
resp_fmt["json_schema"]["schema"]["properties"]["data_response"]["description"] = "the structured summarization of the answer above"
print(resp_fmt)
client = openai.Client(
    api_key=os.getenv("OPENAI_API_KEY")
)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Can you generate some actions based on the  purpose of life?"},
        ],
        response_format=resp_fmt
    )
    print(response)
except Exception as e:
    print(e)
