from gen_mod.test1.implementation.desc_gen_action import Action
from gen_mod.test1.implementation.mgr_gen_action import ActionManager

ass = ActionManager()
a =  Action({"action_description": "DNISNDFISNDFINSD","duration": 10})
print(a.default_str())