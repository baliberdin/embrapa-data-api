from embrapadataapi.configuration.environment import JobConfig


class AbstractJob:
    """Classe abstrata para jobs"""
    # Configuração do Job
    config: JobConfig

    def __init__(self, config: JobConfig):
        self.config = config
        pass

    def run(self):
        """Método que executa o job propriamente dito"""
        pass
