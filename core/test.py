import importlib

import load_modules.test1.implementation
from agent.agent_instance import AgentNetwork

agent = AgentNetwork()
agent.check_version_file("load_modules/version.txt")
mgr = agent.get_data_manager("57a86cdc-5939-11ef-8eb4-047c168941e2",1003)
print(mgr.get_class())
print(mgr.get_class().to_json_struct())
