import logging
import os.path
import re

import yaml

from util.dict_util import update_without_overwrite

mod_name = "test1"
data_conf_path = "conf/"
gen_path = f"gen_mod/{mod_name}/implementation/"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('modules.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def desc_gen(data_list: dict):

    for (key, value) in data_list.items():
        snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
        camel_key = key.replace("_", " ").title().replace(" ", "")
        with open(gen_path + f"desc_gen_{snake_key}.py", "w+") as file:
            file.write("from data_module.data_interface import DataInterface, overwrite_descriptor, DataListInterface\n\n")
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
            file.write("        #@overwrite_descriptor #add this decorator at the overwriting properties\n")
            file.write(f"        #def {snake_key}_description(self):\n")
            file.write(f"        #    return f\" {key} NEW Description is : {{self.get_data_str('{snake_key}_description')}}\"\n")
            file.write(f"        # {snake_key}_description(self)\n")
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


def mgr_gen(data_list: dict,desc_list: dict):
    for (key, value) in data_list.items():
        snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
        camel_key = key.replace("_", " ").title().replace(" ", "")
        with open(gen_path + f"mgr_gen_{snake_key}.py", "w+") as file:
            file.write("from data_module.agent_interface import AgentInterface\n")
            file.write("from data_module.context_interface import QueryContext\n")
            file.write("from data_module.data_interface import DataInterface, DataListInterface\n")
            file.write("from data_module.manager_interface import BaseDataManager\n")
            file.write(f"from desc_gen_{snake_key} import {key}, {key}List\n\n")
            file.write(f"class {camel_key}Manager(BaseDataManager):\n")
            file.write("    def set_service_response(self, response, ctx: QueryContext):\n")
            file.write(f"        if isinstance(response, ({key}, {key}List)):\n")
            file.write("            ctx.set_response(response)\n")
            file.write("        else:\n")
            file.write("            raise ValueError(\"Response must be an instance of DataInterface or DataListInterface\")\n")
            file.write("\n")
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




def generate():
    data_list = {}
    data_list_with_internal = {}
    desc_list = {}
    for file in os.listdir(data_conf_path):
        dataConf = yaml.load(open(data_conf_path + file, 'r'), Loader=yaml.FullLoader)
        try:
            update_without_overwrite(data_list, dataConf["DataIndex"])
        except ValueError as e:
            logger.warning(f"[codeGen]Warning on reading multiple Conf files for Data Generation: {e}")
        try:
            update_without_overwrite(data_list_with_internal, dataConf["DataIndex"])
        except ValueError as e:
            logger.warning(f"[codeGen]Warning on reading multiple Conf files for Internal Data Generation: {e}")
        try:
            update_without_overwrite(data_list_with_internal, dataConf["InternalDataIndex"])
        except ValueError as e:
            logger.warning(f"[codeGen]Warning on reading multiple Conf files for Internal Data Generation: {e}")
        try:
            update_without_overwrite(desc_list, dataConf["DataDescriptor"])
        except ValueError as e:
            logger.warning(f"[codeGen]Warning on reading multiple Conf files On descriptor Generation: {e}")
    desc_gen(data_list_with_internal)
    mgr_gen(data_list,desc_list)

generate()