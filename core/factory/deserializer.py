import logging

import message.APMFactory_pb2
from data_module import DataInterface, DataListInterface, parse_func_index, QueryContext, parse_data_index, \
    AgentNetworkInterface
from factory.main_service_caller import main_servicer_caller
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def deserialize_function_node(node:message.APMFactory_pb2.TaskNode,network:AgentNetworkInterface, context: QueryContext):
    func_type,func_id = parse_func_index(node.node_id)
    #func_type deprecated, all merged into mainserivcer
    function_prompt = node.function_param.user_prompt
    system_prompt = node.function_param.system_prompt
    user_input = context.usr_prompt

    # this index starts from 1 to n to match prompt format
    for (index,data_node) in node.node_structure.input_data:
        result, result_str = deserialize_data_node(data_node,network, context)
        function_prompt = function_prompt.replace("{" + str(index) + "}", " " + result_str)
        system_prompt = system_prompt.replace("{" + str(index) + "}", " " + result_str)

    context = {
        "prompt": function_prompt,
        "system": system_prompt,
        "text_input": user_input,
    }
    result, result_str = main_servicer_caller(context)
    return result, result_str


def fetch_data(node:message.APMFactory_pb2.DataNode,network:AgentNetworkInterface, context:QueryContext)-> (DataInterface or DataListInterface,any, str):
    data_type,data_id,data_desc,data_prop = parse_data_index(node.node_id)
    try:
        data_mgr = network.get_data_manager(node.uuid,data_id)
    except Exception as e:
        logger.error(f"Failed to fetch data {node.uuid} from network, {e}")
        return None ,""
    data_instance = data_mgr.get_descriptor(data_desc,network,context)
    if data_type != 12: #ConnectorData does not goes in cache
        #root_cache is contained within a single query, uuid is not needed
        context.set_cache(data_id,data_instance)
    prop,prop_str = data_instance.get_property_from_index(data_prop)
    return data_instance, prop,prop_str






def deserialize_data_node(node:message.APMFactory_pb2.DataNode,network:AgentNetworkInterface, context:QueryContext)-> (DataInterface or DataListInterface,any, str):
    data_type,_,_,_ = parse_data_index(node.node_id)
    if data_type == 11: #GeneralData
        data,prop,prop_str = fetch_data(node,network,context)
        return data,prop,prop_str
    elif data_type == 12: #ConnectorData
        if node.node_structure is None or node.node_structure.input_data is None or len(node.node_structure.input_data) == 0:
            logger.error("ConnectorData must have input data for Connector Type")
            return None, None
        for (index,data_node) in node.node_structure.input_data:
            _,prop,prop_str = deserialize_data_node(data_node,network, context)
            context.set_param_data(index, (prop, prop_str))
        data,prop,prop_str = fetch_data(node,network,context)
        return data,prop,prop_str
