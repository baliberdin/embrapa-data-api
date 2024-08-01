from sqlalchemy import String, Integer, BigInteger, Double
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from embrapadataapi.configuration.environment import get_config, get_logger
from embrapadataapi.data.database import get_engine

settings = get_config()
logger = get_logger(__name__)
engine = get_engine()


class Base(DeclarativeBase):
    pass

    @staticmethod
    def get_table_schema(model: type[DeclarativeBase]):
        schema = {}
        for column in model.__table__.columns:
            schema[column.name] = column.type
        return schema


class Production(Base):
    __tablename__ = 'production'
    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(100))
    control: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(BigInteger())
    created_at: Mapped[str] = mapped_column(String(25))


class Processed(Base):
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
    __tablename__ = 'commercial'
    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(100))
    control: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(BigInteger())
    created_at: Mapped[str] = mapped_column(String(25))


class Importation(Base):
    __tablename__ = 'importation'
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(BigInteger())
    amount: Mapped[int] = mapped_column(Double())
    created_at: Mapped[str] = mapped_column(String(25))


class Exportation(Base):
    __tablename__ = 'exportation'
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(BigInteger())
    amount: Mapped[int] = mapped_column(Double())
    created_at: Mapped[str] = mapped_column(String(25))


logger.info("Creating database tables")
Base.metadata.create_all(engine)
