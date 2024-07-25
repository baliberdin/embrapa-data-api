from pydantic import BaseModel

from embrapadataapi.api.parameters import ParameterParser


class QueryParams(BaseModel):
    """Classe que define o formato de resposta dos parâmetros que foram passados para a API"""
    limit: int
    skip: int
    filters: dict


class ResourceResultInfo(BaseModel):
    """Classe que define o formato de resposta dos metadados do resultado da API"""
    total_results: int = 0
    fetched: int = 0
    has_more: bool = False


class ResourceLink(BaseModel):
    """Classe que define o formato de resposta dos links da API"""
    href: str
    rel: str


class ResourceResult(BaseModel):
    """Classe que define o formato de resposta dos resultados retornados pela API"""
    info: ResourceResultInfo
    data: list


class WebResponse(BaseModel):
    """Classe que define o formato padrão de resposta dos recursos da API"""
    query: QueryParams | None
    result: ResourceResult
    links: list[ResourceLink]

    @staticmethod
    def build(endpoint: str, params: ParameterParser, data: list, total: int):
        """Função destinada a construir um resultado JSON da nossa API próximo ao padrão HATEOAS

            Args:
                endpoint: str - Nome do endpoint que foi chamado
                params: ParameterParser - Conjunto de parâmetros passados por querystring e validados
                data: list - Lista dos dados retornados de acordo com a consulta. Podem estar paginados, caso os parâmetros
                    limit e skip tenham sido passados
                total: int - Quantidade de itens encontrados de acordo com a consulta
            Returns:
                WebResponse - JSON que representa os dados consultados contendo: a lista dos registros encontrados, metadados
                sobre as quantidades e links de navegação
            """

        info = ResourceResultInfo(total_results=total, fetched=len(data), has_more=(params.limit + params.skip) < total)
        result = ResourceResult(info=info, data=data)

        links = [ResourceLink(rel="self", href=f"/{endpoint}"),
                 ResourceLink(rel="query_example", href=f"/{endpoint}?limit=10&skip=0&filters=ano:2023"),
                 ResourceLink(rel="parent", href="/")]

        query = QueryParams(filters=params.filters, limit=params.limit, skip=params.skip)
        return WebResponse(query=query, result=result, links=links)
