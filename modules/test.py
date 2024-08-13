from gen_mod.test1.implementation.desc_gen_route_plan import RoutePlan
from gen_mod.test1.implementation.mgr_gen_route_plan import RoutePlanManager

ass = RoutePlanManager()
a =  RoutePlan({"action_description" : "DNISNDFISNDFINSD","duration": 10})
a.get_str("action_description")

print(a.to_json_struct())