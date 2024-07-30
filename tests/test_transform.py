import pandas as pd
import logging
from embrapadataapi.data.transform import _pivot_category, _deduplicate_columns, _translate_columns


def test_should_translate_columns():
    data = pd.DataFrame(data={'id': [1], 'control':
        ['VINHO'], 'produto': ['vinho tinto'], 'País': ['Brasil'], 'cultivar': 'Ancelota'})

    data = _translate_columns(data)

    assert set(data.columns.values) == {'id', 'product', 'control', 'cultivation', 'country'}


def test_should_extract_category_from_upper_value_column_and_remove_id():
    data = pd.DataFrame(data={'id': [1, 2], 'control':
        ['VINHO', 'vinho tinto'], 'produto': ['VINHO', 'vinho tinto'], '1970': [0, 0]})

    data = _translate_columns(data)
    transformed_data = _pivot_category(data)

    assert len(transformed_data.columns) == 4
    assert 'id' not in transformed_data.columns
    assert set(transformed_data.columns.values) == {'control', 'product', 'category', '1970'}


def test_should_deduplicate_year_column_and_generate_metrics():
    data = pd.DataFrame(data={'1970': [1, 2],
                              '1970.1': [4, 5],
                              '1971': [6, 7],
                              '1971.1': [8, 9],
                              'país': ['Brasil', 'EUA'],
                              'type': ['De mesa', 'De mesa'],
                              'created_at': ['2024-07-17T00:00:00.000', '2024-07-17T00:00:00.000']
                              })
    data = _translate_columns(data)
    transformed_data = _deduplicate_columns(data)

    assert len(transformed_data.columns) == 6
    assert 'id' not in transformed_data.columns
    assert set(transformed_data.columns.values) == {'country', 'type', 'created_at', 'quantity', 'amount', 'year'}
    assert transformed_data.at[0, 'quantity'] == 1
    assert transformed_data.at[0, 'amount'] == 4
    assert transformed_data.at[1, 'quantity'] == 2
    assert transformed_data.at[1, 'amount'] == 5
    assert transformed_data.at[2, 'quantity'] == 6
    assert transformed_data.at[2, 'amount'] == 8
    assert transformed_data.at[3, 'quantity'] == 7
    assert transformed_data.at[3, 'amount'] == 9
    assert len(transformed_data.index) == 4
