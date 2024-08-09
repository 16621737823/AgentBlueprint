from data_module import DataInterface, DataListInterface

class RoutePlan(DataInterface):
    __slots__ = ["action_description","ActionDescription","duration","Duration","start_time","StartTime","end_time","EndTime",]
    def __init__(self, data: dict = None):
        default_prop = {"action_description": None,"duration": None,"start_time": None,"end_time": None,}
        default_prop.update(data)
        super().__init__(default_prop)
        self.description_overwrite()
    def description_overwrite(self):
        #def property_name(self):
        #    return f" RoutePlan NEW Description is : {self.get_data_str('property_name')}"
        # self.overwrite(property_name)
        return
    def get_property_str_from_index(self,index: int)->(any, str):
        if index == 0:
            return self,self.default_str()
        elif index == 1:
            return self.get("action_description"),self.action_description
        elif index == 2:
            return self.get("duration"),self.duration
        elif index == 3:
            return self.get("start_time"),self.start_time
        elif index == 4:
            return self.get("end_time"),self.end_time

class RoutePlanList(DataListInterface):
    def __init__(self, data: list):
        super().__init__(data)
