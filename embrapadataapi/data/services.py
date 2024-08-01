import logging

from embrapadataapi.data.models import *
from embrapadataapi.data.repositories import *


class GenericService:
    generic_repository: GenericRepository

    def __init__(self, generic_repository: GenericRepository):
        self.generic_repository = generic_repository

    def select_by_filters(self, limit: int, skip: int, filters: dict):
        total = self.generic_repository.get_fetched_rows(filters)
        result = self.generic_repository.get_filtered_results(limit, skip, filters)
        return total, result

    def get_repository_columns(self):
        return self.generic_repository.table_entity.__table__.columns.keys()


class ServiceFactory:
    logger: logging.Logger
    engine: Engine

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = get_engine()

    def get_service(self, model: type[Base]):
        return GenericService(GenericRepository(self.engine, model))

