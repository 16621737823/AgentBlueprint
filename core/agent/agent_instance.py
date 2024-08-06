import logging

from data_module import AgentInterface
from module_loader.data_loader import load_data_module_from_path

logger = logging.getLogger(__name__)
handeler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handeler.setFormatter(formatter)
logger.addHandler(handeler)
logger.setLevel(logging.DEBUG)

class Agent(AgentInterface):
    def subscribe_to_data(self, mod_name: str):
        path = f"load_modules.{mod_name}.implementation"
        try:
            mod = load_data_module_from_path(path)
        except ImportError as e:
            logger.error(f"Failed to load data module from path {path}, {e}")
            return
        try:
            self.register_data_managers(*mod.get_mgr_list())
        except Exception as e:
            logger.error(f"Failed to load data module from path {path}, {e}")
            return
        logger.info(f"Subscribed to data module {mod_name}")

    def check_version_file(self,file:str):
        modules_list = []
        with open(file,"r") as f:
            modules = f.readlines()
        for module in modules:
            module_name, moduel_version = module.split(" : ")
            modules_list.append((module_name,moduel_version))
        for module in modules_list:
            for loaded_mod in self.subscribed_data:
                if loaded_mod[0] == module[0] and loaded_mod[1] == module[1]:
                    logger.debug(f"Module {module[0]} found")
                    if loaded_mod[1] != module[1]:
                        logger.warning(f"Version mismatch for module {module[0]}")
                        try:
                            self.remove_data_manager(loaded_mod[1])
                        except ValueError as e:
                            logger.error(f"Failed to remove data manager {loaded_mod[1]}")
                        self.subscribe_to_data(module[0])
                        break
                    else:
                        logger.debug(f"Version match for module {module[0]}")
            logger.debug(f"Module {module[0]} not found,subscribing")
            self.subscribe_to_data(module[0])



