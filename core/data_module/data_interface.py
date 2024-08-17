import re

from pydantic import BaseModel




class DataInterface:

    def get_property_from_index(self, index:int)->(any, str):
        raise NotImplementedError
