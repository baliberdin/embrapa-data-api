from sqlalchemy import Engine, text

from embrapadataapi.configuration.logger import get_logger
from embrapadataapi.data.models import Base

logger = get_logger(__name__)


class GenericRepository:
    """Classe de repositório genérica que dependerá da entidade passada no momento da instanciação"""
    # Engine de acesso ao banco
    engine: Engine
    # Tabela do banco de dados ao qual o repositório estã associado
    table_entity: type[Base]
    # Colunas da tabela
    columns: list

    def __init__(self, engine: Engine, table_entity: type[Base]):
        self.engine = engine
        self.table_entity = table_entity

    def _execute_query(self, parsed_query: str, filters):
        """Método que executa uma query no banco de dados
        Args:
            parsed_query: Query em formato de string já parseado
            filters: Valores que serão interpolados nos filtros da query parseada
        Returns:
            dataset
        """
        # Pega uma conexão do banco de dados
        conn = self.engine.connect()
        # Cria um cursor com a query
        cursor = conn.execute(text(parsed_query), filters)
        # Faz a chamada para capturar os dados retornados da query
        results = cursor.fetchall()
        # Fecha a conexão
        conn.close()
        return results

    def get_filtered_results(self, rows: int = 10, skip: int = 0, *kwargs):
        """Método para selecianar dados do repositõrio baseado em filtros
        Args:
            rows: número de registros para serem retornados
            skip: número de registros que devem ser ignorados
            kwargs: filtros que serão aplicados na query
        Returns:
            result: array de dict com os registros encontrados
        """
        # Cria template básico da query
        query = f"SELECT * FROM {self.table_entity.__tablename__} "
        # Cria template da paginação
        limit = "LIMIT :skip,:limit"

        # Chama o método que prepara os filtros passando os que recebemos do service
        where, filters = self._prepare_filters(kwargs[0])

        # Adiciona a paginação
        filters['skip'] = skip
        filters['limit'] = rows

        # Concatena os templates da query para montar a query final
        parsed_query = query+where+limit
        # Log de debug para ver como a query ficou
        logger.debug(f"{parsed_query} <= {filters}")
        # Executa aquery
        results = self._execute_query(parsed_query, filters)
        # Retorna os resultados em formato de array de dict
        return [r._asdict() for r in results]

    def get_fetched_rows(self, *kwargs):
        """Método que contabiliza o total de resultados existentes para um determinado filtro
        Args:
            kwargs: filtros que serão passadaos para a query
        Returns:
            total: O valor total de registros existentes baseado nos filtros
        """
        # Cria o template básico de contagem
        query = f"SELECT COUNT(1) AS total FROM {self.table_entity.__tablename__} "
        # Chama o método que prepara os filtros passando os que recebemos do service
        where, filters = self._prepare_filters(kwargs[0])

        # Concatena os elementos da query
        parsed_query = query+where
        # Log da query para debug
        logger.debug(f"{parsed_query} <= {filters}")
        # Executa a query
        results = self._execute_query(parsed_query, filters)
        # Retorna apenas o valor do total calculado
        return results[0][0]

    def _prepare_filters(self, raw_filters: dict):
        # Pega as colunas da tabela
        columns = self.table_entity.__table__.columns
        # Somente os filtros que dão match com alguma coluna da tabela é que serão utilizados
        # Reune todas keys dos filtros passados
        filter_keys = list(filter(lambda k: k in columns, raw_filters.keys()))
        filters = {}
        # Cria o templete dos filtros
        where = ""

        # Itera os filtros de forma a construir a clausula WHERE da query e o dict de filtros
        for f in filter_keys:
            filters[f] = raw_filters[f]
            if len(where) == 0:
                where += f" WHERE {f} = :{f} "
            else:
                where += f"AND {f} = :{f} "

        return where, filters
