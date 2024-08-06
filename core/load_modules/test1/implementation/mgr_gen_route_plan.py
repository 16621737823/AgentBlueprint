from data_module import AgentNetworkInterface, QueryContext, DataInterface, DataListInterface, DataManagerInterface
from . import RoutePlan, RoutePlanList

class RoutePlanManager(DataManagerInterface):
    def set_service_response(self, response, ctx: QueryContext):
        if isinstance(response, (RoutePlan, RoutePlanList)):
            ctx.set_response(response)
        else:
            raise ValueError("Response must be an instance of DataInterface or DataListInterface")

    def fetch_input_params(self, ctx: QueryContext):
        origin = ctx.input_params.get("1", None)
        if origin is None:
            raise ValueError("Missing required value for parameter Origin")
        destination = ctx.input_params.get("2", None)
        if destination is None:
            raise ValueError("Missing required value for parameter Destination")
        return{
            "origin": origin,
            "destination": destination,
        }

    def get_descriptor(self, desc_index:int, d:AgentNetworkInterface, ctx:QueryContext) -> DataInterface or DataListInterface:
        input_params = self.fetch_input_params(ctx)
        if desc_index == 0:
            return self._single(ctx, input_params)
        elif desc_index == 1:
            return self._list(ctx, input_params)
        elif desc_index == 20:
            return self._current(ctx, input_params)
        else:
            raise ValueError("Invalid Descriptor Index")

    def _single(self, ctx: QueryContext,input_params:dict = None) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    def _list(self, ctx: QueryContext,input_params:dict= None) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    def _current(self, ctx: QueryContext,input_params:dict= None) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

