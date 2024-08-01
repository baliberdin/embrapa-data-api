import datetime
import os
import traceback
from functools import reduce

import pandas as pd

from embrapadataapi.data.database import get_connection
from embrapadataapi.data.models import *

settings = get_config()
logger = get_logger(__name__)

column_translate_map = {'produto': 'product',
                        'país': 'country',
                        'cultivar': 'cultivation',
                        'categoria':'category'}


def execute_production_model_etl(download_path: str):
    """Função que processa os dados de produção de vinhos e salva os dados no banco sqlite
    Args:
        download_path: str - Caminho onde os arquivos CSV da embrapa estão localizados
    """

    # Nome do arquivo CSV que será lido de dentro da pasta de downloads
    file_name = 'Producao.csv'

    try:
        # Carrega o arquivo CSV e cria um DataFrame pandas
        data = _load_file_data(file_name, download_path, {})
        # Traduz os nomes das colunas para normalização
        data = _translate_columns(data)
        # Realiza o tratamento inicial dos dados do CSV
        data = _pivot_category(data)
        # Pivota novamente os dados, mas dessa vez, transformando as colunas de anos
        # em valores de uma coluna ano
        data = data.melt(id_vars=['control', 'product', 'category', 'created_at'],
                         var_name='year', value_name='quantity')
        # Escreve os dados na base sqlite3
        _save_data(data, Production)
    except Exception:
        # Printa a stack de erro
        traceback.print_exc()
        logger.warn(f"Erro ao processar os dados da aba de produção da embrapa")


def execute_process_model_etl(download_path: str):
    file_names = [{"file": "ProcessaAmericanas.csv", "separator": "\t", "type": "Americanas e Híbridas"},
                  {"file": "ProcessaMesa.csv", "separator": "\t", "type": "Uvas de Mesa"},
                  {"file": "ProcessaSemclass.csv", "separator": "\t", "type": "Sem Classificação"},
                  {"file": "ProcessaViniferas.csv", "separator": ";", "type": "Viníferas"}]

    try:
        data = reduce(
            lambda a, b: pd.concat([a, b]),
            map(lambda f: _load_file_data(file_name=f['file'], download_path=download_path, separator=f['separator'],
                                          static_columns={"type": f["type"]}), file_names)
        )

        data = _translate_columns(data)
        data = _pivot_category(data)
        data = data.melt(id_vars=['control', 'cultivation', 'category', 'created_at', 'type'],
                         var_name='year', value_name='quantity')
        _save_data(data, Processed)
    except Exception:
        traceback.print_exc()
        logger.warn(f"Erro ao processar os dados da aba de processamento da embrapa")


def execute_commercial_model_etl(download_path: str):
    file_name = 'Comercio.csv'

    try:
        data = _load_file_data(file_name, download_path, {})
        data = _translate_columns(data)
        data = _pivot_category(data)
        data = data.melt(id_vars=['control', 'product', 'category', 'created_at'],
                         var_name='year', value_name='quantity')
        _save_data(data, Commercial)
    except Exception:
        traceback.print_exc()
        logger.warn(f"Erro ao processar os dados da aba de comercio da embrapa")


def execute_importation_model_etl(download_path: str):
    file_names = [{"file": "ImpEspumantes.csv", "separator": ";", "type": "Espumantes"},
                  {"file": "ImpFrescas.csv", "separator": ";", "type": "Uvas Frescas"},
                  {"file": "ImpPassas.csv", "separator": ";", "type": "Uvas Passas"},
                  {"file": "ImpSuco.csv", "separator": ";", "type": "Sucos de Uva"},
                  {"file": "ImpVinhos.csv", "separator": ";", "type": "Vinhos de Mesa"}]

    try:
        data = reduce(
            lambda a, b: pd.concat([a, b]),
            map(lambda f: _load_file_data(file_name=f['file'], download_path=download_path, separator=f['separator'],
                                          static_columns={"type": f["type"]}), file_names)
        )
        data = _translate_columns(data)
        data.drop(columns=['id'], inplace=True)
        data = _deduplicate_columns(data)
        _save_data(data, Importation)
    except Exception:
        traceback.print_exc()
        logger.warn(f"Erro ao processar os dados da aba de importação da embrapa")


def execute_exportation_model_etl(download_path: str):
    file_names = [{"file": "ExpEspumantes.csv", "separator": ";", "type": "Espumantes"},
                  {"file": "ExpUva.csv", "separator": ";", "type": "Uvas Frescas"},
                  {"file": "ExpSuco.csv", "separator": ";", "type": "Sucos de Uva"},
                  {"file": "ExpVinho.csv", "separator": ";", "type": "Vinhos de Mesa"}]

    try:
        data = reduce(
            lambda a, b: pd.concat([a, b]),
            map(lambda f: _load_file_data(file_name=f['file'], download_path=download_path, separator=f['separator'],
                                          static_columns={"type": f["type"]}), file_names)
        )
        data = _translate_columns(data)
        data.drop(columns=['id'], inplace=True)
        data = _deduplicate_columns(data)
        _save_data(data, Exportation)
    except Exception:
        traceback.print_exc()
        logger.warn(f"Erro ao processar os dados da aba de exportação da embrapa")


def _translate_columns(data: pd.DataFrame):
    columns_to_drop = []
    for index, row in data.iterrows():
        for column in row.keys():
            col = str(column).lower().strip()
            if col in column_translate_map.keys():
                columns_to_drop.append(column)
                data.at[index, column_translate_map[col]] = data.at[index, column]

    data = data.drop(columns=columns_to_drop)
    return data


def _load_file_data(file_name: str, download_path: str, static_columns: dict, separator: str = ';'):
    """Função que carrega o CSV do disco para um formato Dataframe (Pandas)

    Args:
        file_name: str - Nome do arquivo que será carregado
        download_path: str - Caminho onde o arquivo está armazenado
        static_columns: dict - Parâmetro opcional contendo valores estáticos que podem ser
        adicionados ao Dataframe final
        separator: str - Separador de valores do CSV, por padrão será usado o ;
    Return:
        DataFrame: Pandas DataFrame contendo o arquivo indicado adicionado da coluna com a data de
        criação do arquivo e, se for preenchido, as colunas estáticas
    """

    logger.info(f"Loading file: {file_name}")
    # Caminho completo do arquivo
    file_path = os.path.join(download_path, file_name)
    # Data de criação do arquivo
    file_time = os.path.getmtime(file_path)
    file_created_at = datetime.datetime.fromtimestamp(file_time).isoformat()
    # Carrega o CSV para um dataframe
    data = pd.read_csv(file_path, sep=separator, header=0)
    # Transforma todas as colunas para lowercase
    data.columns = map(lambda a: str.lower(a), data.columns)
    # Adiciona uma coluna contendo a data de criação do arquivo
    data['created_at'] = file_created_at
    # Adiciona as colunas estáticas
    if static_columns:
        for f in static_columns.keys():
            data[f] = static_columns[f]
    logger.info(f"File loaded successfully: {file_name}")
    return data


def _pivot_category(data: pd.DataFrame):
    """ Função que trata o Dataframe removendo algumas linhas intermediárias
    que são na verdade agregações das linhas seguintes e converte em uma coluna de categoria.
    Args:
        data: DataFrame - Dataframe que será submetido ao tratamento.
    Return:
        Dataframe: O dataframe tratado
    """
    category = None
    for index, row in data.iterrows():
        if str(row['control']).isupper():
            category = row['control']
            data.at[index, 'agg'] = True
        else:
            data.at[index, 'agg'] = False

        data.at[index, 'category'] = str(category).strip()
    data = data[data['agg'] != True]
    data = data.drop(columns=['id', 'agg'])
    return data


def _deduplicate_columns(data: pd.DataFrame):
    amount_columns = list(filter(lambda c: str(c).endswith('.1'), data.columns))
    quantity_columns = list(map(lambda c: str(c).replace('.1', ''), amount_columns))

    data_quantity = data.drop(columns=amount_columns)
    data_amount = data.drop(columns=quantity_columns)

    data_quantity = data_quantity.melt(id_vars=['country', 'type', 'created_at'], var_name='year',
                                       value_name='quantity')
    data_amount = data_amount.melt(id_vars=['country', 'type', 'created_at'], var_name='year', value_name='amount')

    for index, row in data_amount.iterrows():
        data_amount.at[index, 'year'] = data_amount.at[index, 'year'].replace('.1', '').strip()
        data_amount.at[index, 'key'] = \
            f"{data_amount.at[index, 'type']}_{data_amount.at[index, 'country']}_{data_amount.at[index, 'year']}"

    for index, row in data_quantity.iterrows():
        data_quantity.at[index, 'year'] = data_quantity.at[index, 'year'].strip()
        data_quantity.at[index, 'key'] = \
            f"{data_quantity.at[index, 'type']}_{data_quantity.at[index, 'country']}_{data_quantity.at[index, 'year']}"

    data_amount = data_amount.drop(columns=['year', 'country', 'type', 'created_at'])
    data = pd.merge(data_quantity, data_amount, on=["key"])
    data.drop(columns=['key'], inplace=True)
    return data


def _save_data(data: pd.DataFrame, model: type[Base]):
    """Função para salvar os dados do Dataframe no banco de dados.
    Args:
        data: Dataframe - Dados para serem salvos no banco
        model: Modelo que representa a tabela no banco de dados
    """

    # Pega a conexão do banco de dados
    with get_connection() as conn:
        # Pega o nome da tabela a partir do modelo
        table_name = model.__tablename__
        logger.info(f"Saving transformed data into table {table_name}")
        # Executa a inserção dos dados no banco
        data.to_sql(name=table_name, if_exists='replace',
                    index_label="id", index=True, con=conn, dtype=model.get_table_schema(model))
        # Fecha a conexão com o banco
        conn.close()
        logger.info(f"Table {table_name} ETL success.")
