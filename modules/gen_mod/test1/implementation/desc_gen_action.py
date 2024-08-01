from data_module.data_interface import DataInterface, overwrite_descriptor, DataListInterface


class Action(DataInterface):
    def __init__(self, data: dict = None):
        super().__init__(data)
        self.description_overwrite()
    def description_overwrite(self):
        @overwrite_descriptor
        def action_description(self):
            return f" Test Action is : {self.get_data_str('action_description')}"
        action_description(self)
    def get_property_from_index(self,index: int):
        if index == 0:
            return self.default(),self.default_str()
        elif index == 1:
            return self.default(),self.action_description
        elif index == 2:
            return self.default(),self.duration

class ActionList(DataListInterface):
    def __init__(self, data: list):
        super().__init__(data)
