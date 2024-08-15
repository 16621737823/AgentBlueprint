import logging
import os.path
import re
import uuid

import yaml

from util.dict_util import update_without_overwrite

class conf:
    mod_name = ""
    gen_path = ""
    gen_uuid = ""

data_conf_path = "conf/"
ver_file = "gen_mod/version.txt"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('modules.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def _convert_2_python_type(type: str)->(bool,str):
    if type == "string":
        return True, "str"
    elif type == "bool":
        return True,"bool"
    elif type == "int32" or type == "uint32" or type == "int64" or type == "uint64":
        return True,"int"
    elif type == "float32" or type == "float64":
        return True,"float"
    else:
        return False,type

def _desc_gen(data_list: dict):

    for (_, val_dict) in data_list.items():
        for (key, value) in val_dict.items():
            snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
            camel_key = key.replace("_", " ").title().replace(" ", "")
            with open(conf.gen_path + f"desc_gen_{snake_key}.py", "w+") as file:
                file.write("from pydantic import BaseModel, Field,ConfigDict\n")
                file.write("from data_module import DataInterface, DataListInterface\n\n")
                params = ""
                for (prop_key, prop) in value["property"].items():
                    snake_prop_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', prop_key).lower()
                    # camel_prop_key = snake_prop_key.replace("_", " ").title().replace(" ", "")
                    is_base_type, prop_type = _convert_2_python_type(prop["type"])
                    snake_type_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', prop["type"]).lower()
                    if is_base_type:
                        params += f"    {snake_prop_key}: {prop_type} = Field(description=\"\")\n"
                    else:
                        file.write(f"from .desc_gen_{snake_type_key} import {prop_type}\n")
                        params += f"    {snake_prop_key}: {prop_type} = Field(description=\"\")\n"
                file.write(f"class {key}(BaseModel,DataInterface):\n")
                file.write("    model_config = ConfigDict(json_schema_serialization_defaults_required=True,extra='forbid')\n")
                file.write("    _data : dict\n")
                file.write("    _desc_data : dict\n")
                file.write(f"{params}")
                file.write("    def __init__(self, data: dict):\n")
                file.write("        super().__init__(**data)\n")
                file.write("        self._init_desc_data()\n")
                file.write("    def __str__(self):\n")
                file.write("        return \"\".join(self._desc_data[key] + \".\" for key in self._data.keys() if self._data[key] is not None).strip(\".\")\n")
                file.write("    def get_str(self,key:str):\n")
                file.write("        if getattr(self,key) is not None:\n")
                file.write("            return self._desc_data[key]\n")
                file.write("        else:\n")
                file.write("            return \"\"\n")
                file.write("    def _init_desc_data(self):\n")
                file.write("        #Can be overriden to add more description\n")
                file.write("        self._desc_data = {\n")
                for (prop_key, prop) in value["property"].items():
                    snake_prop_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', prop_key).lower()
                    file.write(f"            \"{snake_prop_key}\": f\"{key}'s {prop_key} is {{str(self.{snake_prop_key})}}\",\n")
                file.write("        }\n")
                file.write("    def get_property_from_index(self,index: int)->(any, str):\n")
                file.write("        if index == 0:\n")
                file.write("            return self,str(self)\n")
                for (prop_key, prop) in value["property"].items():
                    snake_prop_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', prop_key).lower()
                    file.write(f"        elif index == {prop['index']}:\n")
                    file.write(f"            return self.{snake_prop_key},self.{snake_prop_key}\n")
                file.write("    @staticmethod\n")
                file.write("    def to_dict_struct()->dict[str,any]:\n")
                file.write(f"        return {key}.model_json_schema(mode='serialization')\n")
                file.write("\n")
                file.write(f"class {key}List(BaseModel,DataListInterface):\n")
                file.write("    model_config = ConfigDict(json_schema_serialization_defaults_required=True, extra='forbid')\n")
                file.write(f"    {snake_key}_list: list[{key}] = Field(description=\"\")\n")
                file.write("    def __init__(self, data: list):\n")
                file.write("        super().__init__(data)\n")
                file.write("    @staticmethod\n")
                file.write("    def to_dict_struct() -> dict[str, any]:\n")
                file.write(f"        return {key}List.model_json_schema(mode='serialization')\n")

            with open(conf.gen_path + "__init__.py", "a") as file:
                file.write(f"from .desc_gen_{snake_key} import {key}, {key}List\n")

def _mgr_gen(data_list: dict, desc_list: dict):
    dict_str = "{"
    import_list_str = "from . import "
    for (type, val_dict) in data_list.items():
        if type == "InternalData":
            continue
        for (key, value) in val_dict.items():
            snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
            camel_key = snake_key.replace("_", " ").title().replace(" ", "")
            with open(conf.gen_path + f"mgr_gen_{snake_key}.py", "w+") as file:
                file.write("from data_module import QueryContext, DataInterface, DataListInterface, DataManagerInterface\n")
                file.write(f"from . import {key}, {key}List\n\n")
                file.write(f"class {camel_key}Manager(DataManagerInterface):\n")
                file.write("    @staticmethod\n")
                file.write("    def get_class()->DataInterface:\n")
                file.write(f"        return {key}.__mro__[0]\n")
                file.write("    @staticmethod\n")
                file.write("    def get_class_list()->DataListInterface:\n")
                file.write(f"        return {key}List.__mro__[0]\n")
                file.write("    @staticmethod\n")
                file.write("    def set_service_response(response, ctx: QueryContext):\n")
                file.write(f"        if isinstance(response, ({key}, {key}List)):\n")
                file.write("            ctx.set_response(response)\n")
                file.write("        else:\n")
                file.write("            raise ValueError(\"Response must be an instance of DataInterface or DataListInterface\")\n")
                file.write("\n")
                if type == "ConnectorData":
                    file.write("    @staticmethod\n")
                    file.write("    def fetch_connected_data(ctx: QueryContext):\n")
                    for (param_key, param) in value["parameters"].items():
                        snake_param_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', param_key).lower()
                        file.write(f"        {snake_param_key} = ctx.get_param_data({param['index']})\n")
                        file.write(f"        if {snake_param_key} is None:\n")
                        file.write(f"            raise ValueError(\"Missing required value for parameter {param_key}\")\n")
                    file.write("        # returned values are tuples containing (original value, string value)\n")
                    file.write("        return{\n")
                    for (param_key, param) in value["parameters"].items():
                        snake_param_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', param_key).lower()
                        file.write(f"            \"{snake_param_key}\": {snake_param_key},\n")
                    file.write("        }\n")
                    file.write("\n")
                    file.write("    @staticmethod\n")
                    file.write("    def get_descriptor(desc_index:int, ctx:QueryContext) -> DataInterface or DataListInterface:\n")
                    file.write(f"        connected_params = {key}.fetch_connected_data(ctx)\n")
                    file.write("        if desc_index == 0:\n")
                    file.write(f"            return {key}._single(ctx, connected_params)\n")
                    file.write("        elif desc_index == 1:\n")
                    file.write(f"            return {key}._list(ctx, connected_params)\n")
                    for desc_type in value["descriptor"] if value["descriptor"] is not None else []:
                        for (desc_key, desc) in desc_list[desc_type].items():
                            snake_desc_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', desc_key).lower()
                            file.write(f"        elif desc_index == {desc}:\n")
                            file.write(f"            return {key}._{snake_desc_key}(ctx, connected_params)\n")
                    file.write("        else:\n")
                    file.write("            raise ValueError(\"Invalid Descriptor Index\")\n")
                    file.write("\n")
                    file.write("    @staticmethod\n")
                    file.write("    def _single(ctx: QueryContext,connected_params:dict = None) -> DataInterface or DataListInterface:\n")
                    file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                    file.write("        raise NotImplementedError\n")
                    file.write("\n")
                    file.write("    @staticmethod\n")
                    file.write("    def _list(ctx: QueryContext,connected_params:dict= None) -> DataInterface or DataListInterface:\n")
                    file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                    file.write("        raise NotImplementedError\n")
                    file.write("\n")
                    for desc_type in value["descriptor"] if value["descriptor"] is not None else []:
                        for (desc_key, desc) in desc_list[desc_type].items():
                            snake_desc_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', desc_key).lower()
                            file.write("    @staticmethod\n")
                            file.write(f"    def _{snake_desc_key}(ctx: QueryContext,connected_params:dict= None) -> DataInterface or DataListInterface:\n")
                            file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                            file.write(f"        raise NotImplementedError\n")
                            file.write("\n")
                else:
                    file.write("    @staticmethod\n")
                    file.write("    def get_descriptor(desc_index:int, ctx:QueryContext) -> DataInterface or DataListInterface:\n")
                    file.write("        if desc_index == 0:\n")
                    file.write(f"            return {key}._single(ctx)\n")
                    file.write("        elif desc_index == 1:\n")
                    file.write(f"            return {key}._list(ctx)\n")
                    for desc_type in value["descriptor"] if value["descriptor"] is not None else []:
                        for (desc_key, desc) in desc_list[desc_type].items():
                            snake_desc_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', desc_key).lower()
                            file.write(f"        elif desc_index == {desc}:\n")
                            file.write(f"            return {key}._{snake_desc_key}(ctx)\n")
                    file.write("        else:\n")
                    file.write("            raise ValueError(\"Invalid Descriptor Index\")\n")
                    file.write("\n")
                    file.write("    @staticmethod\n")
                    file.write("    def _single( ctx: QueryContext) -> DataInterface or DataListInterface:\n")
                    file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                    file.write("        raise NotImplementedError\n")
                    file.write("\n")
                    file.write("    @staticmethod\n")
                    file.write("    def _list(ctx: QueryContext) -> DataInterface or DataListInterface:\n")
                    file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                    file.write("        raise NotImplementedError\n")
                    file.write("\n")

                    for desc_type in value["descriptor"] if value["descriptor"] is not None else []:
                        for (desc_key, desc) in desc_list[desc_type].items():
                            snake_desc_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', desc_key).lower()
                            file.write("    @staticmethod\n")
                            file.write(f"    def _{snake_desc_key}(ctx: QueryContext) -> DataInterface or DataListInterface:\n")
                            file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                            file.write(f"        raise NotImplementedError\n")
                            file.write("\n")
            with open(conf.gen_path + "__init__.py", "a") as init_file:
                init_file.write(f"from .mgr_gen_{snake_key} import {camel_key}Manager\n")
            import_list_str += f" {camel_key}Manager,"
            dict_str += f" {value['index']}: {camel_key}Manager,"
    import_list_str = import_list_str.strip(",")
    dict_str = dict_str.strip(",")
    dict_str += "}"
    with open(conf.gen_path + f"mgr_list_gen.py", "w+") as list_file:
        list_file.write("import uuid\n")
        list_file.write(f"{import_list_str}")

        list_file.write("\n")
        list_file.write("def get_mgr_list():\n")
        list_file.write(f"    return \"{conf.gen_uuid}\",{dict_str}\n")
    with open(conf.gen_path + "__init__.py", "a") as file:
        file.write(f"from .mgr_list_gen import get_mgr_list\n")
    with open(ver_file, "r+") as file:
        lines = file.readlines()
    with open(ver_file,"w") as file:
        #TODO There should be a unique id associated with each module after open up market place, plus a version id
        for line in lines:
            if conf.mod_name not in line:
                file.write(line)
        file.write(f"{conf.mod_name} : {conf.gen_uuid}\n")




def generate(mod_name="default"):
    conf.mod_name = mod_name
    conf.gen_path = f"gen_mod/{mod_name}/implementation/"
    conf.gen_uuid = uuid.uuid1()
    data_list = {
        "GeneralData": {},
        "InternalData": {},
        "ConnectorData": {}
    }
    desc_list = {}
    with open(conf.gen_path + "__init__.py", "w+") as file:
        file.write("######## package import ########\n")
    for file in os.listdir(data_conf_path):
        dataConf = yaml.load(open(data_conf_path + file, 'r'), Loader=yaml.FullLoader)
        try:
            update_without_overwrite(data_list["GeneralData"], dataConf["GeneralData"])
        except ValueError as e:
            logger.warning(f"[codeGen]Warning on reading multiple Conf files for Data Generation: {e}")
        try:
            update_without_overwrite(data_list["InternalData"], dataConf["InternalData"])
        except ValueError as e:
            logger.warning(f"[codeGen]Warning on reading multiple Conf files for Internal Data Generation: {e}")
        try:
            update_without_overwrite(data_list["ConnectorData"], dataConf["ConnectorData"])
        except ValueError as e:
            logger.warning(f"[codeGen]Warning on reading multiple Conf files for Connector Data Generation: {e}")
        try:
            update_without_overwrite(desc_list, dataConf["DataDescriptor"])
        except ValueError as e:
            logger.warning(f"[codeGen]Warning on reading multiple Conf files On descriptor Generation: {e}")
    _desc_gen(data_list)
    _mgr_gen(data_list, desc_list)


generate("test1")