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


def _desc_gen(data_list: dict):

    for (_, val_dict) in data_list.items():
        for (key, value) in val_dict.items():
            snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
            camel_key = key.replace("_", " ").title().replace(" ", "")
            with open(conf.gen_path + f"desc_gen_{snake_key}.py", "w+") as file:
                file.write("from data_module import DataInterface, DataListInterface\n\n")
                file.write(f"class {key}(DataInterface):\n")
                file.write("    def __init__(self, data: dict = None):\n")

                prop_dict = "{"
                for (prop_key, prop) in value["property"].items():
                    snake_prop_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', prop_key).lower()
                    prop_dict += f"\"{snake_prop_key}\": None,"
                prop_dict.strip(",")
                prop_dict += "}"
                file.write(f"        default_prop = {prop_dict}\n")
                file.write("        default_prop.update(data)\n")
                file.write("        super().__init__(default_prop)\n")
                file.write("        self.description_overwrite()\n")
                file.write("    def description_overwrite(self):\n")
                file.write(f"        #def property_name(self):\n")
                file.write(f"        #    return f\" {key} NEW Description is : {{self.get_data_str('property_name')}}\"\n")
                file.write(f"        # self.overwrite(property_name)\n")
                file.write("        return\n")
                file.write("    def get_property_from_index(self,index: int):\n")
                file.write("        if index == 0:\n")
                file.write("            return self.default(),self.default_str()\n")
                for (prop_key, prop) in value["property"].items():
                    snake_prop_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', prop_key).lower()
                    file.write(f"        elif index == {prop['index']}:\n")
                    file.write(f"            return self.default(),self.{snake_prop_key}\n")
                file.write("\n")
                file.write(f"class {key}List(DataListInterface):\n")
                file.write("    def __init__(self, data: list):\n")
                file.write("        super().__init__(data)\n")
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
                file.write("from data_module import AgentInterface, QueryContext, DataInterface, DataListInterface, BaseDataManager\n")
                file.write(f"from . import {key}, {key}List\n\n")
                file.write(f"class {camel_key}Manager(BaseDataManager):\n")
                file.write("    def set_service_response(self, response, ctx: QueryContext):\n")
                file.write(f"        if isinstance(response, ({key}, {key}List)):\n")
                file.write("            ctx.set_response(response)\n")
                file.write("        else:\n")
                file.write("            raise ValueError(\"Response must be an instance of DataInterface or DataListInterface\")\n")
                file.write("\n")
                if type == "ConnectorData":
                    file.write("    def fetch_input_params(self, ctx: QueryContext):\n")
                    for (param_key, param) in value["parameters"].items():
                        snake_param_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', param_key).lower()
                        file.write(f"        {snake_param_key} = ctx.input_params.get(\"{param['index']}\", None)\n")
                        file.write(f"        if {snake_param_key} is None:\n")
                        file.write(f"            raise ValueError(\"Missing required value for parameter {param_key}\")\n")
                    file.write("        return{\n")
                    for (param_key, param) in value["parameters"].items():
                        snake_param_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', param_key).lower()
                        file.write(f"            \"{snake_param_key}\": {snake_param_key},\n")
                    file.write("        }\n")
                    file.write("\n")
                    file.write("    def get_descriptor(self, desc_index:int, d:AgentInterface, ctx:QueryContext) -> DataInterface or DataListInterface:\n")
                    file.write("        input_params = self.fetch_input_params(ctx)\n")
                    file.write("        if desc_index == 0:\n")
                    file.write("            return self._single(ctx, input_params)\n")
                    file.write("        elif desc_index == 1:\n")
                    file.write("            return self._list(ctx, input_params)\n")
                    for desc_type in value["descriptor"] if value["descriptor"] is not None else []:
                        for (desc_key, desc) in desc_list[desc_type].items():
                            snake_desc_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', desc_key).lower()
                            file.write(f"        elif desc_index == {desc}:\n")
                            file.write(f"            return self._{snake_desc_key}(ctx, input_params)\n")
                    file.write("        else:\n")
                    file.write("            raise ValueError(\"Invalid Descriptor Index\")\n")
                    file.write("\n")
                    file.write("    def _single(self, ctx: QueryContext,input_params:dict = None) -> DataInterface or DataListInterface:\n")
                    file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                    file.write("        raise NotImplementedError\n")
                    file.write("\n")
                    file.write("    def _list(self, ctx: QueryContext,input_params:dict= None) -> DataInterface or DataListInterface:\n")
                    file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                    file.write("        raise NotImplementedError\n")
                    file.write("\n")
                    for desc_type in value["descriptor"] if value["descriptor"] is not None else []:
                        for (desc_key, desc) in desc_list[desc_type].items():
                            snake_desc_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', desc_key).lower()
                            file.write(f"    def _{snake_desc_key}(self, ctx: QueryContext,input_params:dict= None) -> DataInterface or DataListInterface:\n")
                            file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                            file.write(f"        raise NotImplementedError\n")
                            file.write("\n")
                else:
                    file.write("    def get_descriptor(self, desc_index:int, d:AgentInterface, ctx:QueryContext) -> DataInterface or DataListInterface:\n")
                    file.write("        if desc_index == 0:\n")
                    file.write("            return self._single(ctx)\n")
                    file.write("        elif desc_index == 1:\n")
                    file.write("            return self._list(ctx)\n")
                    for desc_type in value["descriptor"] if value["descriptor"] is not None else []:
                        for (desc_key, desc) in desc_list[desc_type].items():
                            snake_desc_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', desc_key).lower()
                            file.write(f"        elif desc_index == {desc}:\n")
                            file.write(f"            return self._{snake_desc_key}(ctx)\n")
                    file.write("        else:\n")
                    file.write("            raise ValueError(\"Invalid Descriptor Index\")\n")
                    file.write("\n")
                    file.write("    def _single(self, ctx: QueryContext) -> DataInterface or DataListInterface:\n")
                    file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                    file.write("        raise NotImplementedError\n")
                    file.write("\n")
                    file.write("    def _list(self, ctx: QueryContext) -> DataInterface or DataListInterface:\n")
                    file.write("        #TODO: implement me, this is where connects to a datasource, could be a database or a service\n")
                    file.write("        raise NotImplementedError\n")
                    file.write("\n")
                    for desc_type in value["descriptor"] if value["descriptor"] is not None else []:
                        for (desc_key, desc) in desc_list[desc_type].items():
                            snake_desc_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', desc_key).lower()
                            file.write(f"    def _{snake_desc_key}(self, ctx: QueryContext) -> DataInterface or DataListInterface:\n")
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