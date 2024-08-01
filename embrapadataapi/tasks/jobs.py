from embrapadataapi.configuration.environment import JobConfig


class AbstractJob:
    config: JobConfig

    def __init__(self, config: JobConfig):
        self.config = config
        pass

    def run(self):
        pass
