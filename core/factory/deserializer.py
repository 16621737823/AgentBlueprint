import logging

import message.APMFactory_pb2
from data_module import DataInterface, DataListInterface, QueryContext, parse_data_index, \
    AgentNetworkInterface, FunctionNodeContext, SessionContext, DataNodeContext
from factory.main_service_caller import main_servicer_caller
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def deserialize_session(node:message.APMFactory_pb2.apmFile,network:AgentNetworkInterface):
    session_ctx = SessionContext()
    for task_node in node.nodes:
        deserialize_function_node(task_node,network,FunctionNodeContext(task_id= task_node.node_id,session=session_ctx))
        print("Function Executed")
def deserialize_function_node(node:message.APMFactory_pb2.TaskNode,network:AgentNetworkInterface, context: FunctionNodeContext):
    # func_type,func_id = parse_func_index(node.node_id)
    #func_type deprecated, all merged into mainserivcer
    function_prompt = node.function_param.user_prompt
    system_prompt = node.function_param.system_prompt
    user_input = context.usr_prompt

    if len(node.node_structure.input_data) > 0:
        # this index starts from 1 to n to match prompt format
        for (index,data_node) in node.node_structure.input_data.items():
            data_ctx = DataNodeContext(parent_context=context,source_index=data_node.source_id)
            data,prop,prop_str = deserialize_data_node(data_node,network, data_ctx)
            function_prompt = function_prompt.replace("{" + str(index) + "}", " " + prop_str)
            system_prompt = system_prompt.replace("{" + str(index) + "}", " " + prop_str)

    context = {
        "prompt": function_prompt,
        "system": system_prompt,
        "text_input": user_input,
    }
    print(context)
    result, result_str = main_servicer_caller(context)
    return result, result_str


def fetch_data(node:message.APMFactory_pb2.DataNode,network:AgentNetworkInterface, context:DataNodeContext)-> ((DataInterface or DataListInterface),any, str):
    data_type,data_id,data_desc,data_prop = parse_data_index(node.data_id)
    try:
        data_mgr = network.get_data_manager(node.package_uuid,data_id)
    except Exception as e:
        logger.error(f"Failed to fetch data {node.package_uuid} from network, {e}")
        raise e
    data_instance = data_mgr.get_descriptor(data_desc,context)
    if data_type != 12: #ConnectorData does not goes in cache
        #root_cache is contained within a single query, uuid is not needed
        context.root_cache[data_id]=data_instance
    prop,prop_str = data_instance.get_property_from_index(data_prop)
    return data_instance, prop,prop_str




def deserialize_data_node(node:message.APMFactory_pb2.DataNode,network:AgentNetworkInterface, context:DataNodeContext)-> (DataInterface or DataListInterface,any, str):
    data_type,_,_,_ = parse_data_index(node.data_id)
    if data_type == 11: #GeneralData
        data,prop,prop_str = fetch_data(node,network,context)
        return data,prop,prop_str
    elif data_type == 12: #ConnectorData
        if node.node_structure is None or node.node_structure.input_data is None or len(node.node_structure.input_data) == 0:
            logger.error("ConnectorData must have input data for Connector Type")
            raise ValueError("ConnectorData must have input data for Connector Type")
        for (index,data_node) in node.node_structure.input_data.items():
            connect_data_ctx = DataNodeContext(parent_context=context,source_index=data_node.source_id)
            _,prop,prop_str = deserialize_data_node(data_node,network, connect_data_ctx)
            context.param_data[index]=(prop, prop_str)
        data,prop,prop_str = fetch_data(node,network,context)
        return data,prop,prop_str
