import os
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings

from embrapadataapi.configuration.logger import get_logger

logger = get_logger(__name__)


class JobConfig(BaseModel):
    """
    Classe que define as configurações dos jobs que vâo ser executados em segundo plano
    """
    # Nome do Job
    name: str
    # Parâmetros customizados que job possa necessitar para ser executado
    params: dict
    # Intervalo em segundos em que o job deve ser executado
    seconds_interval: int
    # Caminho do módulo onde está a classe que implementa o Job
    module: str
    # Nome da classe que implementa o Job
    clazz: str


class AuthenticationConfig(BaseModel):
    """
    Classe que define os dados de autenticação
    """
    # Nome do usuário para login
    username: str
    # Senha do usuário em formato de hash
    password: str
    # Key para criar o hash das senhas
    secret_key: str
    # Tipo de algoritmo utilizado na autenticação
    algorithm: str
    # Tempo de vida em minutos para a validade do token, por padrão 2 minutos
    expires_minutes: int = 2


class AppConfig(BaseModel):
    """
    Classe que define as configurações da API
    """
    # Nome da aplicação. Será exibida na tela de documentação /docs
    application_name: str
    # Caminho do arquivo de dados usado pelo Sqlite3 ou :memory: caso queira usar banco em memória
    database_name: str
    # Configurações de autenticação
    auth: AuthenticationConfig
    # Lista de jobs para serem agendados.
    jobs: list[JobConfig]


class SettingsLoader(YamlBaseSettings):
    """
    Classe que carrega as configurações gerais da aplicação exceto as configurações de log
    """
    # Atributo que guarda as configurações da aplicação
    app_config: AppConfig
    # Carrega as configurações a partir do arquivo env.yaml
    model_config = SettingsConfigDict(secrets_dir='./secrets', yaml_file='./env.yaml', env_file_encoding='utf-8')


@lru_cache
def get_config() -> AppConfig:
    """ Captura todas as configurações definidas em variáveis de ambiente ou no arquivo .env
    Variáveis de ambiente tem precedência em relação às que estão no arquivo .env
    Todas as configurações são cacheadas usando lru_cache

    Returns:
        AppConfig: Todas as configurações da aplicação
    """

    settings = SettingsLoader().app_config
    logger.debug(f"Configuration: {settings}")
    return settings
