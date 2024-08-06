import importlib

import load_modules.test1.implementation
from agent.agent_instance import AgentNetwork

agent = AgentNetwork()
agent.check_version_file("load_modules/version.txt")

