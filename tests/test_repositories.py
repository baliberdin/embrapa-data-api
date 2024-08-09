from embrapadataapi.data.repositories import *
from embrapadataapi.data.models import *


def test_should_parse_valid_filters():
    subject = GenericRepository(None, Production)
    where, filters = subject._prepare_filters({"category": "2023"})

    assert where == ' WHERE category = :category '
    assert filters == {'category': '2023'}


def test_should_ignore_invalid_filters_when_parse():
    subject = GenericRepository(None, Production)
    where, filters = subject._prepare_filters({"foo": "bar"})

    assert where == ''
    assert filters == {}


def test_should_clean_invalid_filters_and_preserve_valid_ones_when_parse():
    subject = GenericRepository(None, Production)
    where, filters = subject._prepare_filters({"foo": "bar", "category": "2023"})

    assert where == ' WHERE category = :category '
    assert filters == {'category': '2023'}
