from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from functools import lru_cache
from configuration.logger import get_logger

logger = get_logger(os.path.basename(__file__))


class _Settings(BaseSettings):
    """Classe que representa as configurações gerais da aplicação exceto as configurações de log"""
    downloaded_data_path: str
    application_name: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache
def get_config():
    """ Captura todas as configurações definidas em variáveis de ambiente ou no arquivo .env
    Variáveis de ambiente tem precedência em relação às que estão no arquivo .env
    Todas as configurações são cacheadas usando lru_cache

    Returns:
        dict: Um dicionário com todas as configurações
    """

    settings = _Settings()
    logger.info(f"Configuration: {settings}")
    return settings
