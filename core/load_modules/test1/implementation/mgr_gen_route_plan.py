from typing import Type
from data_module import QueryContext, DataInterface, DataManagerInterface, DataNodeContext, FunctionNodeContext
from . import RoutePlan, RoutePlanList

class RoutePlanManager(DataManagerInterface):
    @staticmethod
    def set_service_response(response, ctx: FunctionNodeContext):
        if isinstance(response, (RoutePlan, RoutePlanList)):
            ctx.set_query_response(response)
        else:
            raise ValueError("Response must be an instance of DataInterface")

    @staticmethod
    def get_descriptor_class(desc_index:int)->Type:
        if desc_index == 0:
            return RoutePlan
        elif desc_index == 1:
            return RoutePlanList
        else:
            raise ValueError("Invalid Descriptor Index")
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
    def get_descriptor(desc_index:int, ctx:DataNodeContext) -> DataInterface :
        if desc_index == 2:
            return RoutePlanManager._previous(ctx)
        connected_params = RoutePlanManager.fetch_connected_data(ctx)
        if desc_index == 0:
            return RoutePlanManager._single(ctx, connected_params)
        elif desc_index == 1:
            return RoutePlanManager._list(ctx, connected_params)
        elif desc_index == 20:
            return RoutePlanManager._current(ctx, connected_params)
        else:
            raise ValueError("Invalid Descriptor Index")

    @staticmethod
    def _single(ctx: DataNodeContext,connected_params:dict = None) -> DataInterface:
        return RoutePlan(action_description="test_action_description", duration=1, start_time=1, end_time=1)

    @staticmethod
    def _list(ctx: DataNodeContext,connected_params:dict= None) -> DataInterface :
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    @staticmethod
    def _previous(ctx: DataNodeContext,connected_params:dict= None) -> DataInterface :
        return ctx.get_reference_context(ctx.source_index)

    @staticmethod
    def _current(ctx: DataNodeContext,connected_params:dict= None) -> DataInterface :
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

