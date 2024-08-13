from data_module import QueryContext, DataInterface, DataListInterface, DataManagerInterface
from . import ParsedAction, ParsedActionList

class ParsedActionManager(DataManagerInterface):
    @staticmethod
    def get_class()->DataInterface:
        return ParsedAction.__mro__[0]
    @staticmethod
    def set_service_response(response, ctx: QueryContext):
        if isinstance(response, (ParsedAction, ParsedActionList)):
            ctx.set_response(response)
        else:
            raise ValueError("Response must be an instance of DataInterface or DataListInterface")

    @staticmethod
    def get_descriptor(desc_index:int, ctx:QueryContext) -> DataInterface or DataListInterface:
        if desc_index == 0:
            return ParsedAction._single(ctx)
        elif desc_index == 1:
            return ParsedAction._list(ctx)
        else:
            raise ValueError("Invalid Descriptor Index")

    @staticmethod
    def _single( ctx: QueryContext) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    @staticmethod
    def _list(ctx: QueryContext) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

