import logging
from typing import Type, Optional

from pydantic import create_model, Field, ConfigDict

import message.APMFactory_pb2
from data_module import DataInterface, QueryContext, parse_data_index, \
    AgentNetworkInterface, FunctionNodeContext, SessionContext, DataNodeContext
from factory.main_service_caller import main_servicer_caller, extract_data, create_response_model
from load_modules.test1.implementation import ParsedActionList

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def run_session(node:message.APMFactory_pb2.apmFile, network:AgentNetworkInterface):
    session_ctx = SessionContext()
    for task_node in node.nodes:
        run_function_node(task_node, network, FunctionNodeContext(task_id= task_node.node_id, session=session_ctx))
        print("Function Executed")
def run_function_node(node:message.APMFactory_pb2.TaskNode, network:AgentNetworkInterface, context: FunctionNodeContext):
    # func_type,func_id = parse_func_index(node.node_id)
    #func_type deprecated, all merged into mainserivcer
    function_prompt = node.function_param.user_prompt
    system_prompt = node.function_param.system_prompt
    user_input = context.usr_prompt

    if len(node.node_structure.input_data) > 0:
        # this index starts from 1 to n to match prompt format
        for (index,data_node) in node.node_structure.input_data.items():
            data_ctx = DataNodeContext(parent_context=context,source_index=data_node.source_id)
            data,prop,prop_str = instantiate_data_node(data_node, network, data_ctx)
            function_prompt = function_prompt.replace("{" + str(index) + "}", " " + prop_str)
            system_prompt = system_prompt.replace("{" + str(index) + "}", " " + prop_str)

    prompt_context = {
        "prompt": function_prompt,
        "system": system_prompt,
        "text_input": user_input,
    }
    print(prompt_context)
    output_class = fetch_data_class(node.output_data_id, node.package_uuid, network)
    result_str = main_servicer_caller(prompt_context, output_class)
    data_result = parse_data(output_class, result_str)
    context.set_query_response(data_result)
    return data_result


def parse_data(data_class:Type, context:str)-> DataInterface :
    try:
        data = extract_data(context, data_class)
        if isinstance(data, DataInterface):
            return data
        else:
            raise ValueError(f"Response must be an instance of {data_class}")
    except Exception as e:
        raise ValueError(f"Failed to parse content to {data_class}: {e}")

def fetch_data(node_id:int,package_uuid:str,network:AgentNetworkInterface, context:DataNodeContext)-> (DataInterface ,any, str):
    data_type,data_id,data_desc,data_prop = parse_data_index(node_id)
    try:
        data_mgr = network.get_data_manager(package_uuid,data_id)
    except Exception as e:
        logger.error(f"Failed to fetch data {package_uuid} from network, {e}")
        raise e
    data_instance = data_mgr.get_descriptor(data_desc,context)
    if data_type != 12: #ConnectorData does not goes in cache
        #root_cache is contained within a single query, uuid is not needed
        context.root_cache[data_id]=data_instance
    prop,prop_str = data_instance.get_property_from_index(data_prop)
    return data_instance, prop,prop_str

def fetch_data_class(node_id:int, package_uuid:str, network:AgentNetworkInterface)->Type:
    data_type,data_id,data_desc,data_prop = parse_data_index(node_id)
    try:
        data_mgr = network.get_data_manager(package_uuid, data_id)
    except Exception as e:
        logger.error(f"Failed to fetch data {package_uuid} from network, {e}")
        raise e
    return data_mgr.get_descriptor_class(data_desc)





def instantiate_data_node(node:message.APMFactory_pb2.DataNode, network:AgentNetworkInterface, context:DataNodeContext)-> (DataInterface , any, str):
    data_type,_,data_desc,_ = parse_data_index(node.data_id)
    if data_type == 11 or data_desc == 2: #GeneralData or previous data reference
        data,prop,prop_str = fetch_data(node.data_id,node.package_uuid,network,context)
        return data,prop,prop_str
    elif data_type == 12: #ConnectorData
        if len(node.node_structure.input_data) == 0:
            logger.error("ConnectorData must have input data for Connector Type")
            raise ValueError("ConnectorData must have input data for Connector Type")
        for (index,data_node) in node.node_structure.input_data.items():
            connect_data_ctx = DataNodeContext(parent_context=context,source_index=data_node.source_id)
            _,prop,prop_str = instantiate_data_node(data_node, network, connect_data_ctx)
            context.param_data[index]=(prop, prop_str)
        data,prop,prop_str = fetch_data(node.data_id,node.package_uuid,network,context)
        return data,prop,prop_str
