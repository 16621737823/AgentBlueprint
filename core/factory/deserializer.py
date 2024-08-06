import message.APMFactory_pb2
from data_module import DataInterface, DataListInterface
from factory.main_service_caller import main_servicer_caller


def DeserializeFunctionNode(node:message.APMFactory_pb2.TaskNode):
    function_prompt = node.function_param.user_prompt
    system_prompt = node.function_param.system_prompt
    # this index starts from 1 to n to match prompt format
    for index in node.node_structure.input_data:
        result, result_str = DeserializeDataNode(node.node_structure.input_data[index])
        function_prompt = function_prompt.replace("{" + str(index) + "}", " " + result_str)
        system_prompt = system_prompt.replace("{" + str(index) + "}", " " + result_str)

    context = {
        "prompt": function_prompt,
        "system": system_prompt
    }
    result, result_str = main_servicer_caller(context)
    return result, result_str

def DeserializeDataNode(node:message.APMFactory_pb2.DataNode)-> (DataInterface or DataListInterface, str):

    pass
