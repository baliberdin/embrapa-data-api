import datetime
import os
from functools import reduce

import pandas as pd

from embrapadataapi.data.database import get_connection
from embrapadataapi.data.models import *

settings = get_config()
logger = get_logger(__name__)


def create_production_model(download_path: str):
    file_name = 'Producao.csv'
    data = _load_file_data(file_name, download_path, {})
    data = _pivot_category(data)
    data = data.melt(id_vars=['control', 'produto', 'categoria', 'created_at'],
                     var_name='ano', value_name='quantidade')
    _save_data(data, Production)


def create_process_model(download_path: str):
    file_names = [{"file": "ProcessaAmericanas.csv", "separator": "\t", "classe": "Americanas e Híbridas"},
                  {"file": "ProcessaMesa.csv", "separator": "\t", "classe": "Uvas de Mesa"},
                  {"file": "ProcessaSemclass.csv", "separator": "\t", "classe": "Sem Classificação"},
                  {"file": "ProcessaViniferas.csv", "separator": ";", "classe": "Viníferas"}]

    data = reduce(
        lambda a, b: pd.concat([a, b]),
        map(lambda f: _load_file_data(file_name=f['file'], download_path=download_path, separator=f['separator'],
                                      static_columns={"classe": f["classe"]}), file_names)
    )

    data = _pivot_category(data)
    data = data.melt(id_vars=['control', 'cultivar', 'categoria', 'created_at', 'classe'],
                     var_name='ano', value_name='quantidade')
    _save_data(data, Processed)


def create_commercial_model(download_path: str):
    file_name = 'Comercio.csv'
    data = _load_file_data(file_name, download_path, {})
    data = _pivot_category(data)
    data = data.melt(id_vars=['control', 'produto', 'categoria', 'created_at'],
                     var_name='ano', value_name='quantidade')
    _save_data(data, Commercial)


def create_import_model(download_path: str):
    file_names = [{"file": "ImpEspumantes.csv", "separator": ";", "classe": "Espumantes"},
                  {"file": "ImpFrescas.csv", "separator": ";", "classe": "Uvas Frescas"},
                  {"file": "ImpPassas.csv", "separator": ";", "classe": "Uvas Passas"},
                  {"file": "ImpSuco.csv", "separator": ";", "classe": "Sucos de Uva"},
                  {"file": "ImpVinhos.csv", "separator": ";", "classe": "Vinhos de Mesa"}]

    data = reduce(
        lambda a, b: pd.concat([a, b]),
        map(lambda f: _load_file_data(file_name=f['file'], download_path=download_path, separator=f['separator'],
                                      static_columns={"classe": f["classe"]}), file_names)
    )
    data.drop(columns=['id'], inplace=True)
    data = _deduplicate_columns(data)
    _save_data(data, Importation)


def create_export_model(download_path: str):
    file_names = [{"file": "ExpEspumantes.csv", "separator": ";", "classe": "Espumantes"},
                  {"file": "ExpUva.csv", "separator": ";", "classe": "Uvas Frescas"},
                  {"file": "ExpSuco.csv", "separator": ";", "classe": "Sucos de Uva"},
                  {"file": "ExpVinho.csv", "separator": ";", "classe": "Vinhos de Mesa"}]

    data = reduce(
        lambda a, b: pd.concat([a, b]),
        map(lambda f: _load_file_data(file_name=f['file'], download_path=download_path, separator=f['separator'],
                                      static_columns={"classe": f["classe"]}), file_names)
    )
    data.drop(columns=['id'], inplace=True)
    data = _deduplicate_columns(data)
    _save_data(data, Exportation)


def _load_file_data(file_name: str, download_path: str, static_columns: dict, separator: str = ';'):
    logger.info(f"Loading file: {file_name}")
    file_path = os.path.join(download_path, file_name)
    file_time = os.path.getmtime(file_path)
    file_created_at = datetime.datetime.fromtimestamp(file_time).isoformat()
    data = pd.read_csv(file_path, sep=separator, header=0)
    data.columns = map(lambda a: str.lower(a), data.columns)
    data['created_at'] = file_created_at
    if static_columns:
        for f in static_columns.keys():
            data[f] = static_columns[f]
    logger.info(f"File loaded successfully: {file_name}")
    return data


def _pivot_category(data: pd.DataFrame):
    category = None
    for index, row in data.iterrows():
        if str(row['control']).isupper():
            category = row['control']
            data.at[index, 'agg'] = True
        else:
            data.at[index, 'agg'] = False

        data.at[index, 'categoria'] = str(category).strip()
    data = data[data['agg'] != True]
    data = data.drop(columns=['id'])
    return data


def _deduplicate_columns(data: pd.DataFrame):
    amount_columns = list(filter(lambda c: str(c).endswith('.1'), data.columns))
    quantity_columns = list(map(lambda c: str(c).replace('.1', ''), amount_columns))

    data_quantity = data.drop(columns=amount_columns)
    data_amount = data.drop(columns=quantity_columns)

    data_quantity = data_quantity.melt(id_vars=['país', 'classe', 'created_at'], var_name='ano', value_name='quantidade')
    data_amount = data_amount.melt(id_vars=['país', 'classe', 'created_at'], var_name='ano', value_name='valor')

    for index, row in data_amount.iterrows():
        data_amount.at[index, 'ano'] = data_amount.at[index, 'ano'].replace('.1', '').strip()
        data_amount.at[index, 'key'] = \
            f"{data_amount.at[index, 'classe']}_{data_amount.at[index, 'país']}_{data_amount.at[index, 'ano']}"

    for index, row in data_quantity.iterrows():
        data_quantity.at[index, 'ano'] = data_quantity.at[index, 'ano'].strip()
        data_quantity.at[index, 'key'] = \
            f"{data_quantity.at[index, 'classe']}_{data_quantity.at[index, 'país']}_{data_quantity.at[index, 'ano']}"

    data_amount = data_amount.drop(columns=['ano', 'país', 'classe', 'created_at'])
    data = pd.merge(data_quantity, data_amount, on=["key"])
    data.drop(columns=['key'], inplace=True)
    return data


def _save_data(data: pd.DataFrame, model: type[Base]):
    conn = get_connection()
    table_name = model.__tablename__
    logger.info(f"Saving transformed data into table {table_name}")
    data.to_sql(name=table_name, if_exists='replace',
                index_label="id", index=True, con=conn, dtype=model.get_table_schema(model))
    conn.close()
    logger.info(f"Table {table_name} ETL success.")
