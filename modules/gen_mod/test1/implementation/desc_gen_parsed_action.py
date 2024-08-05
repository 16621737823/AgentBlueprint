from data_module.data_interface import DataInterface, overwrite_descriptor, DataListInterface

class ParsedAction(DataInterface):
    def __init__(self, data: dict = None):
        default_prop = {"emoji_list": None,}
        default_prop.update(data)
        super().__init__(default_prop)
        self.description_overwrite()
    def description_overwrite(self):
        #@overwrite_descriptor #add this decorator at the overwriting properties
        #def parsed_action_description(self):
        #    return f" ParsedAction NEW Description is : {self.get_data_str('parsed_action_description')}"
        # parsed_action_description(self)
        return
    def get_property_from_index(self,index: int):
        if index == 0:
            return self.default(),self.default_str()
        elif index == 1:
            return self.default(),self.emoji_list

class ParsedActionList(DataListInterface):
    def __init__(self, data: list):
        super().__init__(data)
