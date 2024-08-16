from data_module import QueryContext, DataInterface, DataListInterface, DataManagerInterface, DataNodeContext, FunctionNodeContext
from . import ParsedAction, ParsedActionList

from .desc_gen_emoji_data import EmojiData
class ParsedActionManager(DataManagerInterface):
    @staticmethod
    def get_class()->DataInterface:
        return ParsedAction.__mro__[0]
    @staticmethod
    def get_class_list()->DataListInterface:
        return ParsedActionList.__mro__[0]
    @staticmethod
    def set_service_response(response, ctx: FunctionNodeContext):
        if isinstance(response, (ParsedAction, ParsedActionList)):
            ctx.set_query_response(response)
        else:
            raise ValueError("Response must be an instance of DataInterface or DataListInterface")

    @staticmethod
    def get_descriptor(desc_index:int, ctx:DataNodeContext) -> DataInterface or DataListInterface:
        if desc_index == 0:
            return ParsedActionManager._single(ctx)
        elif desc_index == 1:
            return ParsedActionManager._list(ctx)
        elif desc_index == 2:
            return ParsedActionManager._previous(ctx)
        else:
            raise ValueError("Invalid Descriptor Index")

    @staticmethod
    def _single( ctx: DataNodeContext) -> DataInterface or DataListInterface:
        return ParsedAction(emoji_list=EmojiData(emoji_description="test",emoji_unicode="test"))

    @staticmethod
    def _list(ctx: DataNodeContext) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    @staticmethod
    def _previous(ctx: DataNodeContext) -> DataInterface or DataListInterface:
        return ctx.get_reference_context(ctx.source_index)

