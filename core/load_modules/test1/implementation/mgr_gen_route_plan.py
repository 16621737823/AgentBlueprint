from data_module import QueryContext, DataInterface, DataListInterface, DataManagerInterface, DataNodeContext, FunctionNodeContext
from . import RoutePlan, RoutePlanList

class RoutePlanManager(DataManagerInterface):
    @staticmethod
    def get_class()->DataInterface:
        return RoutePlan.__mro__[0]
    @staticmethod
    def get_class_list()->DataListInterface:
        return RoutePlanList.__mro__[0]
    @staticmethod
    def set_service_response(response, ctx: FunctionNodeContext):
        if isinstance(response, (RoutePlan, RoutePlanList)):
            ctx.set_query_response(response)
        else:
            raise ValueError("Response must be an instance of DataInterface or DataListInterface")

    @staticmethod
    def fetch_connected_data(ctx: DataNodeContext):
        origin = ctx.param_data.get(1)
        if origin[0] is None or origin[1] is None:
            raise ValueError("Missing required value for parameter Origin")
        destination = ctx.param_data.get(2)
        if destination[0] is None or destination[1] is None:
            raise ValueError("Missing required value for parameter Destination")
        # returned values are tuples containing (original value, string value)
        return{
            "origin": origin,
            "destination": destination,
        }

    @staticmethod
    def get_descriptor(desc_index:int, ctx:DataNodeContext) -> DataInterface or DataListInterface:
        connected_params = RoutePlanManager.fetch_connected_data(ctx)
        if desc_index == 0:
            return RoutePlanManager._single(ctx, connected_params)
        elif desc_index == 1:
            return RoutePlanManager._list(ctx, connected_params)
        elif desc_index == 2:
            return RoutePlanManager._previous(ctx, connected_params)
        elif desc_index == 20:
            return RoutePlanManager._current(ctx, connected_params)
        else:
            raise ValueError("Invalid Descriptor Index")

    @staticmethod
    def _single(ctx: DataNodeContext,connected_params:dict = None) -> DataInterface or DataListInterface:
        return RoutePlan(action_description="test_action_description",duration=1,start_time=1,end_time=1)

    @staticmethod
    def _list(ctx: DataNodeContext,connected_params:dict= None) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    @staticmethod
    def _previous(ctx: DataNodeContext,connected_params:dict= None) -> DataInterface or DataListInterface:
        return ctx.get_reference_context(ctx.source_index)

    @staticmethod
    def _current(ctx: DataNodeContext,connected_params:dict= None) -> DataInterface or DataListInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

