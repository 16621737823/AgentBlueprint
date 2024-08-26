from typing import Type
from data_module import QueryContext, DataInterface, DataManagerInterface, DataNodeContext, FunctionNodeContext
from . import Calendar, CalendarList

class CalendarManager(DataManagerInterface):
    @staticmethod
    def set_service_response(response, ctx: FunctionNodeContext):
        if isinstance(response, (Calendar, CalendarList)):
            ctx.set_query_response(response)
        else:
            raise ValueError("Response must be an instance of DataInterface")

    @staticmethod
    def get_descriptor_class(desc_index:int)->Type:
        if desc_index == 0:
            return Calendar
        elif desc_index == 1:
            return CalendarList
        else:
            raise ValueError("Invalid Descriptor Index")
    @staticmethod
    def get_descriptor(desc_index:int, ctx:DataNodeContext) -> DataInterface :
        if desc_index == 0:
            return CalendarManager._single(ctx)
        elif desc_index == 1:
            return CalendarManager._list(ctx)
        elif desc_index == 2:
            return CalendarManager._previous(ctx)
        else:
            raise ValueError("Invalid Descriptor Index")

    @staticmethod
    def _single( ctx: DataNodeContext) -> DataInterface :
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    @staticmethod
    def _list(ctx: DataNodeContext) -> DataInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    @staticmethod
    def _previous(ctx: DataNodeContext) -> DataInterface:
        return ctx.get_reference_context(ctx.source_index)

