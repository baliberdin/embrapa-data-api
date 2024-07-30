from embrapadataapi.api.parameters import ParameterParser
import embrapadataapi.api.parameters as parameters
from embrapadataapi.errors.exceptions import InvalidFilterException
import pytest


def test_should_parse_missing_parameters():
    subject = ParameterParser()

    assert subject.limit == parameters.default_limit_value
    assert subject.skip == parameters.default_skip_value
    assert subject.filters == {}


def test_should_parse_invalid_parameters():
    subject = ParameterParser(skip=-1, limit=-10, filters="ano=2023")

    assert subject.limit == parameters.default_limit_value
    assert subject.skip == parameters.default_skip_value
    assert subject.filters == {}


def test_should_parse_valid_parameters():
    subject = ParameterParser(skip=10, limit=10, filters="ano:2023")

    assert subject.limit == 10
    assert subject.skip == 10
    assert subject.filters == {"ano": "2023"}


def test_should_parse_valid_parameters_with_empty_filter_keys():
    subject = ParameterParser(skip=10, limit=10, filters="ano:2023", filter_keys=[])

    assert subject.limit == 10
    assert subject.skip == 10
    assert subject.filters == {"ano": "2023"}


def test_should_parse_valid_parameters_with_none_filters():
    subject = ParameterParser(skip=10, limit=10, filters=None)

    assert subject.limit == 10
    assert subject.skip == 10
    assert subject.filters == {}


def test_should_parse_valid_parameters_with_none_filter_keys():
    subject = ParameterParser(skip=10, limit=10, filters="ano:2023", filter_keys=None)

    assert subject.limit == 10
    assert subject.skip == 10
    assert subject.filters == {"ano":"2023"}


def test_should_parse_valid_parameters_with_filter_keys():
    subject = ParameterParser(skip=10, limit=10, filters="ano:2023", filter_keys=["ano"])

    assert subject.limit == 10
    assert subject.skip == 10
    assert subject.filters == {"ano": "2023"}


def test_should_raise_exception_for_invalid_parameters_with_filter_keys():
    with pytest.raises(InvalidFilterException):
        assert ParameterParser(skip=10, limit=10, filters="ano:2023", filter_keys=["categoria"])


def test_should_raise_exception_for_invalid_parameter_value_with_filter_keys():
    with pytest.raises(InvalidFilterException):
        assert ParameterParser(skip=10, limit=10, filters="ano:", filter_keys=["ano"])


def test_should_raise_exception_for_invalid_parameter_value_without_filter_keys():
    with pytest.raises(InvalidFilterException):
        assert ParameterParser(skip=10, limit=10, filters="ano:")


def test_should_raise_exception_for_invalid_parameter_key_without_filter_keys():
    with pytest.raises(InvalidFilterException):
        assert ParameterParser(skip=10, limit=10, filters=":2023")

    with pytest.raises(InvalidFilterException):
        assert ParameterParser(skip=10, limit=10, filters=" :2023")


def test_should_parse_valid_multi_parameter_filters():
    subject = ParameterParser(skip=10, limit=10, filters="categoria:teste,ano:2023",
                              filter_keys=["categoria", "ano"])

    assert subject.limit == 10
    assert subject.skip == 10
    assert subject.filters == {"categoria": "teste", "ano": "2023"}
