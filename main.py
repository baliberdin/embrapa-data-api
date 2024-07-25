import traceback

from fastapi import FastAPI, HTTPException

import embrapadataapi.api.parameters as parameters
from embrapadataapi.api.models import *
from embrapadataapi.configuration import environment
from embrapadataapi.data.models import *
from embrapadataapi.data.services import ServiceFactory
from embrapadataapi.errors.exceptions import InvalidFilterException
from embrapadataapi.tasks import scheduler

settings = environment.get_config()
app = FastAPI(title=settings.application_name)
services = ServiceFactory()
scheduler.start()


# Cria um dict com os Recursos a serem listados e disponíveis na API.
resources = {}
for r in [Production, Processed, Commercial, Importation, Exportation]:
    resources[r.__tablename__] = r


@app.get("/")
async def root() -> list[ResourceLink]:
    """Função que define o endpoint raiz da API. A partir desse endpoint é possível navegar para todos
        os outros pontos da API.
    Returns: list[ResourceLink]
    """
    links = list(map(lambda a: ResourceLink(href=f"/{a}", rel="resource"), resources.keys()))
    links.append(ResourceLink(href="/", rel="self"))
    return links


@app.get("/{resource_name}")
async def generic_resource(resource_name: str, limit: int = parameters.default_limit_value,
                           skip: int = parameters.default_skip_value, filters: str | None = None) -> WebResponse:
    """Método que implementa o endpoint genérico de um recurso e coordena as chamadas aos Services correspondente

    Args:
        resource_name: str - Nome do recurso que será chamado.
        limit: int - Quantidade limit de registros que deve ser retornado. Padrão 10
        skip: int - Quantidade de registros que devem ser ignorados antes de começar a contar o limit.
            Deve ser usado junto com o limit para criar a paginação dos recursos
        filters: str - Lista de filtros a serem aplicados aos recursos. Em caso de múltiplos filtros,
            deve-se, separá-los por vírgula. Exemplo: filters=ano:2023,classe:Suco
    Returns:
        WebResponse: JSON que representa os dados consultados contendo a lista dos registros encontrados, metadados
            sobre as quantidades e links de navegação
    Raises:
        InvalidFilterException: Se um filtro inválido for passado via querystring
        HTTPException: Exception que será lançada caso algum problema ocorra durante o processamento da requisição
    """
    if resource_name in resources:
        try:
            resource = resources[resource_name]
            service = services.get_service(resource)
            params = ParameterParser(limit=limit, skip=skip, filters=filters,
                                     filter_keys=service.get_repository_columns())
            total, data = service.select_by_filters(params.limit, params.skip, params.filters)
            return WebResponse.build(resource_name, params, data, total)
        except InvalidFilterException as e:
            traceback.print_exc()
            raise HTTPException(status_code=422, detail=e.__str__())
        except Exception:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Server error. Try again in a feel minutes.")
    else:
        raise HTTPException(status_code=404, detail="Resource not found")
