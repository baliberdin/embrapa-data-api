from sqlalchemy import String, Integer, BigInteger, Double
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from embrapadataapi.configuration.environment import get_config, get_logger
from embrapadataapi.data.database import get_engine

settings = get_config()
logger = get_logger(__name__)
engine = get_engine()


class Base(DeclarativeBase):
    """Classe base para os modelos que serão armazenados no banco de dados"""
    pass

    @staticmethod
    def get_table_schema(model: type[DeclarativeBase]):
        """Método que retorna o schema da tabela em um formato de dicionário
        Args:
            model: Uma instância que implemente DeclarativeBase
        Returns:
            dict: Schema do modelo
        """
        # Inicia um dict vazio que será populado com o schema
        schema = {}
        # Itera sobre as colunas do modelo
        for column in model.__table__.columns:
            # Adiciona ao dict uma referência do nome da coluna com o tipo do dado.
            schema[column.name] = column.type
        # Retorna o schema
        return schema


class Production(Base):
    """Classe que será responsável por representar o modelo de Produção dos dados da embrapa"""
    # Nome da tabela no banco de dados e em seguida os campos
    __tablename__ = 'production'
    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(100))
    control: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(BigInteger())
    created_at: Mapped[str] = mapped_column(String(25))


class Processed(Base):
    """Classe que será responsável por representar o modelo de Processamento dos dados da embrapa"""
    # Nome da tabela no banco de dados e em seguida os campos
    __tablename__ = 'processed'
    id: Mapped[int] = mapped_column(primary_key=True)
    cultivation: Mapped[str] = mapped_column(String(100))
    control: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(BigInteger())
    created_at: Mapped[str] = mapped_column(String(25))
    type: Mapped[str] = mapped_column(String(100))


class Commercial(Base):
    """Classe que será responsável por representar o modelo de Comercialização dos dados da embrapa"""
    # Nome da tabela no banco de dados e em seguida os campos
    __tablename__ = 'commercial'
    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(100))
    control: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(BigInteger())
    created_at: Mapped[str] = mapped_column(String(25))


class Importation(Base):
    """Classe que será responsável por representar o modelo de Importação dos dados da embrapa"""
    # Nome da tabela no banco de dados e em seguida os campos
    __tablename__ = 'importation'
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(BigInteger())
    amount: Mapped[int] = mapped_column(Double())
    created_at: Mapped[str] = mapped_column(String(25))


class Exportation(Base):
    """Classe que será responsável por representar o modelo de Exportação dos dados da embrapa"""
    # Nome da tabela no banco de dados e em seguida os campos
    __tablename__ = 'exportation'
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(BigInteger())
    amount: Mapped[int] = mapped_column(Double())
    created_at: Mapped[str] = mapped_column(String(25))


logger.info("Creating database tables")
# Executa a criação das tabelas no banco sqlite3
Base.metadata.create_all(engine)
