from sqlalchemy import Engine, text

from embrapadataapi.configuration.logger import get_logger
from embrapadataapi.data.models import Base

logger = get_logger(__name__)


class GenericRepository:
    engine: Engine
    table_entity: type[Base]
    columns: list

    def __init__(self, engine: Engine, table_entity: type[Base]):
        self.engine = engine
        self.table_entity = table_entity

    def _execute_query(self, parsed_query: str, filters):
        conn = self.engine.connect()
        cursor = conn.execute(text(parsed_query), filters)
        cursor.keys()
        results = cursor.fetchall()
        conn.close()
        return results

    def get_filtered_results(self, rows: int = 10, skip: int = 0, *kwargs):
        query = f"SELECT * FROM {self.table_entity.__tablename__} "
        limit = "LIMIT :skip,:limit"
        where = ""

        columns = self.table_entity.__table__.columns.keys()
        filter_keys = list(filter(lambda k: k in columns, kwargs[0].keys()))
        filters = {}

        for f in filter_keys:
            filters[f] = kwargs[0][f]
            if len(where) == 0:
                where += f" WHERE {f} = :{f} "
            else:
                where += f"AND {f} = :{f} "

        filters['skip'] = skip
        filters['limit'] = rows

        parsed_query = query+where+limit
        logger.debug(f"{parsed_query} <= {filters}")
        results = self._execute_query(parsed_query, filters)
        return [r._asdict() for r in results]

    def get_fetched_rows(self, *kwargs):
        query = f"SELECT COUNT(1) AS total FROM {self.table_entity.__tablename__} "
        where = ""

        columns = self.table_entity.__table__.columns
        filter_keys = list(filter(lambda k: k in columns, kwargs[0].keys()))
        filters = {}

        for f in filter_keys:
            filters[f] = kwargs[0][f]
            if len(where) == 0:
                where += f" WHERE {f} = :{f} "
            else:
                where += f"AND {f} = :{f} "

        parsed_query = query+where
        logger.debug(f"{parsed_query} <= {filters}")
        results = self._execute_query(parsed_query, filters)
        return results[0][0]
