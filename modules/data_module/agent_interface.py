class AgentInterface:
    def __init__(self):
        self.data_manager = dict()

    def get_data_manager(self):
        raise NotImplementedError
