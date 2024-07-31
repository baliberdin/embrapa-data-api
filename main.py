import traceback

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm

import embrapadataapi.api.parameters as parameters
from embrapadataapi.api.auth import *
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
    links.append(ResourceLink(href="/docs", rel="docs"))
    links.append(ResourceLink(href="/", rel="self"))
    return links


@app.post("/token")
async def request_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    Método utilizado para soliscitar um token de autenticação para a API
    Args:
        form_data: Dados do usuário submetidos via post. username, password
    Returns:
        Token: Um token JWT
    """
    # Chama o método de autenticação para verificar se o usuário e senha passados estão corretos
    user = authenticate_user(form_data.username, form_data.password)
    # Caso as credenciais não estejam corretas uma exceção é lançada e um um erro http (401) é devolvido
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Um token é criado caso as credenciais estejam corretas
    return create_access_token(user)


@app.get("/{resource_name}")
async def generic_resource(current_user: Annotated[User, Depends(get_current_user)],
                           resource_name: str, limit: int = parameters.default_limit_value,
                           skip: int = parameters.default_skip_value, filters: str | None = None,
                           ) -> WebResponse:
    """Método que implementa o endpoint genérico de um recurso e coordena as chamadas aos Services correspondente

    Args:
        current_user: User - O usuário referente ao token de acesso recebido, se o token for válido
        resource_name: str - Nome do recurso que será chamado.
        limit: int - Quantidade limite de registros que deve ser retornado. Padrão 100
        skip: int - Quantidade de registros que devem ser ignorados antes de começar a contar o limit.
            Deve ser usado junto com o limit para criar a paginação dos recursos
        filters: str - Lista de filtros a serem aplicados aos recursos. Em caso de múltiplos filtros,
            deve-se, separá-los por vírgula. Exemplo: filters=year:2023,type:Suco
    Returns:
        WebResponse: JSON que representa os dados consultados contendo a lista dos registros encontrados, metadados
            sobre as quantidades e links de navegação
    Raises:
        InvalidFilterException: Se um filtro inválido for passado via querystring
        HTTPException: Exception que será lançada caso algum problema ocorra durante o processamento da requisição
    """
    # Verifica se o recurso que está sendo requisitado existe
    if resource_name in resources:
        try:
            # Pega o recurso da lista de recursos
            resource = resources[resource_name]
            # Soliscita o service para esse recurso
            service = services.get_service(resource)
            # Processa os parâmetros que foram passados para a API via querystring
            params = ParameterParser(limit=limit, skip=skip, filters=filters,
                                     filter_keys=service.get_repository_columns())
            # Solicita o resultset para o Service juntamente com o total de registros
            total, data = service.select_by_filters(params.limit, params.skip, params.filters)
            # Constroi o response a partir dos dados e dos parâmetros
            return WebResponse.build(resource_name, params, data, total)
        except InvalidFilterException as e:
            # Caso os parâmetros de filtros sejam inválidos uma exceção será lançada e um erro http será retornado
            traceback.print_exc()
            raise HTTPException(status_code=422, detail=e.__str__())
        except Exception:
            # Qualquer outro erro que possa acontecer será tratado como erro 500
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Server error. Try again in a feel minutes.")
    else:
        # Retorna 404 se o recurso chamado não existir
        raise HTTPException(status_code=404, detail="Resource not found")
