from data_module import AgentInterface, QueryContext, DataInterface, DataListInterface, BaseDataManager
from . import ParsedAction, ParsedActionList

class ParsedactionManager(BaseDataManager):
    def set_service_response(self, response, ctx: QueryContext):
        if isinstance(response, (ParsedAction, ParsedActionList)):
            ctx.set_response(response)
        else:
            raise ValueError("Response must be an instance of DataInterface or DataListInterface")

    def get_descriptor(self, desc_index:int, d:AgentInterface, ctx:QueryContext) -> DataInterface or DataListInterface:
        if desc_index == 0:
            return self._single(ctx)
        elif desc_index == 1:
            return self._list(ctx)
        else:
            raise ValueError("Invalid Descriptor Index")

    def _single(self, ctx: QueryContext) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    def _list(self, ctx: QueryContext) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

