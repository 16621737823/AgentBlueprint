class AgentInterface:
    def __init__(self):
        self.data_manager = dict()
        self.task_manager = dict()

    def get_data_manager(self,index: int):
        if index in self.data_manager:
            return self.data_manager[index]
        else:
            raise ValueError("Invalid index from data type")
    def get_task_manager(self,index: int):
        if index in self.task_manager:
            return self.task_manager[index]
        else:
            raise ValueError("Invalid index from task type")

def register_tasks(func):
    def wrapper(self, index: int):
        self.task_manager[index] = func(self)

    return wrapper