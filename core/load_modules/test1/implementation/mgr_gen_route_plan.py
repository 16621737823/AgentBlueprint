from data_module import QueryContext, DataInterface, DataListInterface, DataManagerInterface
from . import RoutePlan, RoutePlanList

class RoutePlanManager(DataManagerInterface):
    @staticmethod
    def get_class()->DataInterface:
        return RoutePlan.__mro__[0]
    @staticmethod
    def set_service_response(response, ctx: QueryContext):
        if isinstance(response, (RoutePlan, RoutePlanList)):
            ctx.set_response(response)
        else:
            raise ValueError("Response must be an instance of DataInterface or DataListInterface")

    @staticmethod
    def fetch_connected_data(ctx: QueryContext):
        origin = ctx.get_param_data(1)
        if origin is None:
            raise ValueError("Missing required value for parameter Origin")
        destination = ctx.get_param_data(2)
        if destination is None:
            raise ValueError("Missing required value for parameter Destination")
        # returned values are tuples containing (original value, string value)
        return{
            "origin": origin,
            "destination": destination,
        }

    @staticmethod
    def get_descriptor(desc_index:int, ctx:QueryContext) -> DataInterface or DataListInterface:
        connected_params = RoutePlan.fetch_connected_data(ctx)
        if desc_index == 0:
            return RoutePlan._single(ctx, connected_params)
        elif desc_index == 1:
            return RoutePlan._list(ctx, connected_params)
        elif desc_index == 20:
            return RoutePlan._current(ctx, connected_params)
        else:
            raise ValueError("Invalid Descriptor Index")

    @staticmethod
    def _single(ctx: QueryContext,connected_params:dict = None) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    @staticmethod
    def _list(ctx: QueryContext,connected_params:dict= None) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    @staticmethod
    def _current(ctx: QueryContext,connected_params:dict= None) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

