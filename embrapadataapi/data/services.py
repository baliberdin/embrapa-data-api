import logging

from embrapadataapi.data.models import *
from embrapadataapi.data.repositories import *


class GenericService:
    """Classe responsável por ter o acesso aos repositõrios de dados. A implementação é uma generalização
    de forma que possamos ter acesso a todos os repositórios apenas passando o recurso
    """
    # Repositório genérico, depende do que será passado no construtor
    generic_repository: GenericRepository

    def __init__(self, generic_repository: GenericRepository):
        self.generic_repository = generic_repository

    def select_by_filters(self, limit: int, skip: int, filters: dict):
        """
        Método que seleciona dados no repositório baseado em filtros
        Args:
            limit: int - Quantidade de registros máxima para retornar
            skip: int - Quantidade de registros que devem ser pulados
            filters: dict - Filtros para serem usados na query dos dados
        Returns:
            tuple(total, result) - Uma tupla com o total de registros para os filtros passados
            e um resultset
        """
        # Retorna a contagem de linhas para os filtros passados
        total = self.generic_repository.get_fetched_rows(filters)
        # Retorna os dados referentes ao limit e skip
        result = self.generic_repository.get_filtered_results(limit, skip, filters)
        # Retorna a tupla com os dados e o total para o filtro passado
        return total, result

    def get_repository_columns(self):
        """Método que retorna as colunas para o Recurso ao qual esse service está apontando
        Returns:
            List: Uma lista de colunas
        """
        return self.generic_repository.table_entity.__table__.columns.keys()


class ServiceFactory:
    """Classe que constrói o service baseado no modelo"""
    logger: logging.Logger
    # Engine de conexão com o banco
    engine: Engine

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = get_engine()

    def get_service(self, model: type[Base]):
        """Método que retorna uma instância de um service baseado no modelo
        Args:
            model: Modelo/Recurso para o qual um service será criado
        Returns:
            GenericService: Um service genérico baseado no modelo passado.
        """
        return GenericService(GenericRepository(self.engine, model))

