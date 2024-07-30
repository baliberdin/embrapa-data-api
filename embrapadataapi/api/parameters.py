from embrapadataapi.errors.exceptions import InvalidFilterException

default_limit_value = 100
default_skip_value = 0


class ParameterParser:
    """Classe que define o comportamento e a validação dos Query Parameters da API"""
    # Parâmetro que limita o número de registros retornados. Juntamente com o
    # parâmetro skip, são utilizados para paginação
    limit: int
    # Parâmetro que indica quantos registros devem ser ignorados
    skip: int
    # Parâmetro que indica como os registros devem ser filtrados.
    # É aceito múltiplas cláusulas, separados por vírgula, que serão parseados a partir do
    # formato campo1:valor1,campo2:valor2 em um dicionário {campo1:valor1, campo2:valor1}
    filters: dict

    def __init__(self, limit: int = default_limit_value, skip: int = default_skip_value, filters: str = None,
                 filter_keys: list = list | None):
        self.limit = limit if limit > 0 else default_limit_value
        self.skip = skip if skip > 0 else default_skip_value

        # Cria uma lista válida de possíveis filtros (whitelist).
        # Caso o parâmetro filter_keys tenha sido passado e for uma lista válida, então
        # somente esses filtros serão permitidos no dicionario,
        # caso a lista seja vazia ou nula, será permitido qualquer filtro, sem restrição
        valid_filters = []
        if isinstance(filter_keys, list):
            valid_filters.extend(filter_keys)

        # Com a lista de possíveis filtros válidos, verificamos se os filtros passados
        # são válidos ou não. A key ou o value de um filtro não pode ser nula/vazia
        if filters is not None and filters.find(':') >= 0:
            parsed_filters = {}
            for f in list(map(lambda fs: {str(fs.split(':')[0]).strip(): str(fs.split(':')[1]).strip()},
                              filters.split(','))):
                for k in list(f.keys()):
                    # Se a lista de filtros que podem ser válidos estiver preenchida
                    # não vamos permitir nenhum parâmetro diferente destes e uma Exception deve ser lançada
                    if len(valid_filters) > 0 and k not in valid_filters:
                        raise InvalidFilterException(f"The filter [{k}:{f[k]}] is not valid for list: {valid_filters}")
                    # Além dos critérios anteriores as chaves e os valores dos filtros não podem ser vazios
                    if (len(k) > 0 and (k in valid_filters or len(valid_filters) == 0)
                            and f[k] and len(f[k]) > 0):
                        parsed_filters[k] = f[k]
                    else:
                        raise InvalidFilterException(f"The filter [{k}:{f[k]}] is not valid for list: {valid_filters}")
            # Armazena todos os filtros válidos
            self.filters = parsed_filters
        else:
            self.filters = {}
