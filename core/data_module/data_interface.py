import re

from pydantic import BaseModel


class DataInterface:

    def get_property_from_index(self, index:int)->(any, str):
        raise NotImplementedError

    @staticmethod
    def to_dict_struct()->dict[str,any]:
        raise NotImplementedError



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

    @staticmethod
    def to_dict_struct() -> dict[str, any]:
        raise NotImplementedError

    def get_property_str_from_index(self, index: int):
        list_str = f"{self.__class__.__name__}"
        for (i, item) in enumerate(self._data):
            _,item_str = item.get_property_from_index(index)
            list_str += f"{i}: {item_str}\n"
        return list_str
