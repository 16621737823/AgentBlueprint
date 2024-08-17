from dotenv import load_dotenv
load_dotenv()
from agent.agent_instance import AgentNetwork
from factory.deserializer import run_session
from util.test_util import get_version_uuid
from write_test_apm import read_test_apm, write_test_apm


agent = AgentNetwork()
agent.check_version_file("load_modules/version.txt")
uuid = get_version_uuid("test1")
mgr = agent.get_data_manager(uuid, 1003)
# print(FunctionCall({}).run(struct_json))
write_test_apm()
apm_struct = read_test_apm()
run_session(apm_struct, agent)
