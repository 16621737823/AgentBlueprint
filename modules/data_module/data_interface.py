import re


class DataInterface:
    def __init__(self,data:dict=None):
        self._data = dict()
        self._desc_data = dict()
        self._construct_data(data)
    def __str__(self):
        return self.default_str()
    def _construct_data(self,data:dict):
        for key in data.keys():
            snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
            camel_key = snake_key.replace("_"," ").title().replace(" ","")
            self._data[snake_key] = data[key]
            self._desc_data[snake_key] = f"{self.__class__.__name__}'s {camel_key} is {str(self._data[snake_key])}"
            prop = property(lambda self: self._desc_data[snake_key])
            setattr(self,snake_key,prop)
            setattr(self,camel_key,prop)

    def get_property_from_index(self, index:int)->(any, str):
        raise NotImplementedError

    def get(self,key:str):
        snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
        return self._data[snake_key]
    def set(self,key:str,value):
        snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
        self._data[snake_key] = value

    def default(self):
        return self._data
    def default_str(self):
        return "".join(self._desc_data[key] + "." for key in self._data.keys() if self._data[key] is not None).strip(".")
    def overwrite(self, func):
        snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', func.__name__).lower()
        self._desc_data[snake_key] = func(self)


class DataListInterface:
    def __init__(self, data: list):
        if all(isinstance(item, DataInterface) for item in data):
            self._data = data
        else:
            raise ValueError("All elements in data must be instances of DataInterface")

    def set(self,data:list):
        if all(isinstance(item, dict) for item in data):
            self._data = [DataInterface(item) for item in data]
        else:
            raise ValueError("All elements in data must be dictionaries")

    def get_property_str_from_index(self, index: int):
        list_str = f"{self.__class__.__name__}"
        for (i, item) in enumerate(self._data):
            _,item_str = item.get_property_from_index(index)
            list_str += f"{i}: {item_str}\n"
        return list_str
