from data_module.context_interface import DataNodeContext, FunctionNodeContext, QueryContext, DataInstanceContext
from gen_mod.test1.implementation import ParsedActionManager

ass = ParsedActionManager()


# # print(ass.get_class_list().to_dict_struct())
# a = DataInstanceContext(data_reference_id = 1)
# b = DataInstanceContext(data_reference_id = 2)
# e = DataInstanceContext(data_reference_id = 3)
# f = DataInstanceContext(data_reference_id = 4)
# b.parent_context = a
# e.parent_context = b
# f.parent_context = e
# kk= f.get_previous_context(1)
c = FunctionNodeContext(usr_prompt= "44")
d = DataNodeContext(usr_prompt = "666",parent_context=c)
d.usr_prompt = "55555"
print(c.usr_prompt)