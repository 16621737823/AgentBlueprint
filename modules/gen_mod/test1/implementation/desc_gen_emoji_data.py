from data_module.data_interface import DataInterface, overwrite_descriptor, DataListInterface

class EmojiData(DataInterface):
    def __init__(self, data: dict = None):
        default_prop = {"emoji_description": None,"emoji_unicode": None,}
        default_prop.update(data)
        super().__init__(default_prop)
        self.description_overwrite()
    def description_overwrite(self):
        #@overwrite_descriptor #add this decorator at the overwriting properties
        #def emoji_data_description(self):
        #    return f" EmojiData NEW Description is : {self.get_data_str('emoji_data_description')}"
        # emoji_data_description(self)
        return
    def get_property_from_index(self,index: int):
        if index == 0:
            return self.default(),self.default_str()
        elif index == 1:
            return self.default(),self.emoji_description
        elif index == 2:
            return self.default(),self.emoji_unicode

class EmojiDataList(DataListInterface):
    def __init__(self, data: list):
        super().__init__(data)
