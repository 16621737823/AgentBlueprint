

class DataInterface:
    def __init__(self,data:dict=None):
        self._construct_data(data)

    def _construct_data(self,data:dict):
        for key in data.keys():
            setattr(self,key,data[key])

    def get_property_from_index(self):
        raise NotImplementedError

    def get(self,key:str):
        return getattr(self,key)


class DescriptorInterface:
    def __init__(self):
        self.data = DataInterface()
    def _get_descriptor(self,desc_index:int, ) -> DataInterface:
        raise NotImplementedError

    def _get_properties(self) -> (DataInterface, str):
        raise NotImplementedError

    def _get_service_response(self):
        raise NotImplementedError
