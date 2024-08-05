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
            camel_key = key.replace("_"," ").title().replace(" ","")
            snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
            self._data[snake_key] = data[key]
            # self._data[camel_key] = data_prt
            # self._data[snake_key] = data_prt
            self._desc_data[snake_key] = f"{self.__class__.__name__}'s {camel_key} is {str(self._data[snake_key])}"
            # self._desc_data[camel_key] = desc_prt
            # self._desc_data[snake_key] = desc_prt
            prop = property(lambda self: self._desc_data[snake_key])
            setattr(self,snake_key,prop)
            setattr(self,camel_key,prop)
            setattr(self,snake_key,prop)

    def get_property_from_index(self,index:int):
        raise NotImplementedError

    def get(self,key:str):
        return self._data[key]
    def get_data_str(self, key:str):
        return str(self._data[key])
    def get_desc(self,key:str):
        return self._desc_data[key]

    def set(self,key:str,value):
        setattr(self._data,key,value)

    def default(self):
        return self._data
    def default_str(self):
        return "".join(self._desc_data[key] + "." for key in self._data.keys() if self._data[key] is not None).strip(".")
def overwrite_descriptor(func):
    def overwrite(obj,*args):
        snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', func.__name__).lower()
        obj._desc_data[snake_key] = func(obj,*args)
        # setattr(obj,func.__name__,func(obj,*args))
    return overwrite

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

    def get_property_from_index(self, index: int):
        list_str = f"{self.__class__.__name__}"
        for (i, item) in enumerate(self._data):
            list_str += f"{i}: {item.get_property_from_index(index)}\n"
        return self._data,list_str
