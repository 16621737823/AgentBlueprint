from typing import Type
from data_module import QueryContext, DataInterface, DataManagerInterface, DataNodeContext, FunctionNodeContext
from . import RoutePlan, RoutePlanList
import requests
from datetime import datetime
import json
from . import TransitDetails

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
        url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
        api_key = 'api_key'

        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': api_key,
            'X-Goog-FieldMask': 'routes.legs.steps.transitDetails'
        }

        data = {
            "origin": {
                "address": "Humberto Delgado Airport, Portugal"
            },
            "destination": {
                "address": "Basílica of Estrela, Praça da Estrela, 1200-667 Lisboa, Portugal"
            },
            "travelMode": "TRANSIT",
            "computeAlternativeRoutes": True,
            "transitPreferences": {
                "routingPreference": "LESS_WALKING",
                "allowedTravelModes": ["TRAIN"]
            }
        }

        # 发送请求
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # 检查请求是否成功
        if response.status_code == 200:
            # 请求成功，处理响应
            result = response.json()
            routes = result.get('routes', [])
            string_array = []
            if routes:
                route=routes[0]
                legs = route.get('legs', [])
                for leg in legs:
                    steps = leg.get('steps', [])
                    for step in steps:
                        transit_details = step.get('transitDetails', [])
                        if transit_details:
                            stop_details = transit_details.get('stopDetails', {})
                            # 以string获取ArrivalStop和DepartureStopTravelMethod
                            arrival_stop_name = stop_details.get('arrivalStop', {}).get('name', "")
                            departure_stop_name = stop_details.get('departureStop', {}).get('name', "")
                            travel_method = transit_details.get('transitLine', {}).get('vehicle', {}).get('name',{}).get('text', "")

                            # 以时间戳（timestamp）获取ArrivalTime和DepartureTime
                            arrival_time_str = stop_details.get('arrivalTime', "")
                            departure_time_str = stop_details.get('departureTime', "")

                            arrival_time = int(datetime.strptime(arrival_time_str,"%Y-%m-%dT%H:%M:%SZ").timestamp()) if arrival_time_str else None
                            departure_time = int(datetime.strptime(departure_time_str,"%Y-%m-%dT%H:%M:%SZ").timestamp()) if departure_time_str else None

                            # 以int32获取StopCount
                            stop_count = int(transit_details.get('stopCount', 0))
                            transit_detail = TransitDetails(arrival_stop=arrival_stop_name,departure_stop=departure_stop_name,travel_method=travel_method,arrival_time=arrival_time,departure_time=departure_time,stop_count=stop_count)

                            string_array.append(str(transit_detail))
            else:
                # 请求失败，输出错误信息
                raise RuntimeError
        return RoutePlan(action_description='111',duration=111,start_time=111,end_time=111,transit_details=string_array)


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

