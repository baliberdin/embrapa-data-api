from sqlalchemy import create_engine
from embrapadataapi.configuration.environment import get_config

settings = get_config()
engine = create_engine(f"sqlite+pysqlite:///{settings.database_name}", pool_size=5, echo=False)


def get_engine():
    return engine


def get_connection():
    return engine.connect()
