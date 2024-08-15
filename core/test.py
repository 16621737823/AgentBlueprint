import importlib
import json
import os

import openai
from dotenv import load_dotenv

import load_modules.test1.implementation
from agent.agent_instance import AgentNetwork
from factory.chat_completion import FunctionCall

load_dotenv()
agent = AgentNetwork()
agent.check_version_file("load_modules/version.txt")
mgr = agent.get_data_manager("16308260-594f-11ef-a2df-047c168941e2", 1003)
struct_json = mgr.get_class_list().to_dict_struct()
print(FunctionCall({}).run(struct_json))
