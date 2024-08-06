from data_module import DataInterface, DataListInterface

class EmojiData(DataInterface):
    __slots__ = ["emoji_description","EmojiDescription","emoji_unicode","EmojiUnicode",]
    def __init__(self, data: dict = None):
        default_prop = {"emoji_description": None,"emoji_unicode": None,}
        default_prop.update(data)
        super().__init__(default_prop)
        self.description_overwrite()
    def description_overwrite(self):
        #def property_name(self):
        #    return f" EmojiData NEW Description is : {self.get_data_str('property_name')}"
        # self.overwrite(property_name)
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
