class AgentInterface:
    def __init__(self):
        self.data_manager = dict()
    def _get_data_manager(self):
        raise NotImplementedError