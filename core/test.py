import importlib
import json
import os

import openai
from dotenv import load_dotenv

import load_modules.test1.implementation
from agent.agent_instance import AgentNetwork
from factory.chat_completion import FunctionCall
from factory.deserializer import deserialize_session
from util.test_util import get_version_uuid
from write_test_apm import read_test_apm, write_test_apm

load_dotenv()
agent = AgentNetwork()
agent.check_version_file("load_modules/version.txt")
uuid = get_version_uuid("test1")
mgr = agent.get_data_manager(uuid, 1003)
struct_json = mgr.get_class_list().to_dict_struct()
# print(FunctionCall({}).run(struct_json))
write_test_apm()
apm_struct = read_test_apm()
deserialize_session(apm_struct,agent)
