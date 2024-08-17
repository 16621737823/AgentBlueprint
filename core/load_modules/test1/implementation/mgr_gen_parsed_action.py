from typing import Type
from data_module import QueryContext, DataInterface, DataManagerInterface, DataNodeContext, FunctionNodeContext
from . import ParsedAction, ParsedActionList

from .desc_gen_emoji_data import EmojiData
class ParsedActionManager(DataManagerInterface):
    @staticmethod
    def set_service_response(response, ctx: FunctionNodeContext):
        if isinstance(response, (ParsedAction, ParsedActionList)):
            ctx.set_query_response(response)
        else:
            raise ValueError("Response must be an instance of DataInterface")

    @staticmethod
    def get_descriptor_class(desc_index:int)->Type:
        if desc_index == 0:
            return ParsedAction
        elif desc_index == 1:
            return ParsedActionList
        else:
            raise ValueError("Invalid Descriptor Index")
    @staticmethod
    def get_descriptor(desc_index:int, ctx:DataNodeContext) -> DataInterface :
        if desc_index == 0:
            return ParsedActionManager._single(ctx)
        elif desc_index == 1:
            return ParsedActionManager._list(ctx)
        elif desc_index == 2:
            return ParsedActionManager._previous(ctx)
        else:
            raise ValueError("Invalid Descriptor Index")

    @staticmethod
    def _single( ctx: DataNodeContext) -> DataInterface :
        return ParsedAction(emoji_list=EmojiData(emoji_description="test_emoji_desc",emoji_unicode="test_emoji_unicode"))

    @staticmethod
    def _list(ctx: DataNodeContext) -> DataInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    @staticmethod
    def _previous(ctx: DataNodeContext) -> DataInterface:
        return ctx.get_reference_context(ctx.source_index)

