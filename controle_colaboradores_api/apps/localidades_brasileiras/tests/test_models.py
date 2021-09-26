import pytest
from model_bakery import baker


@pytest.fixture
def unidade_federativa(db):
    return baker.make('UnidadeFederativa',
                      nome="Unidade Federativa X")


@pytest.fixture
def municipio(db):
    return baker.make('Municipio',
                      nome="Município X")


class TestUnidadeFederativa:

    def test_str(self, unidade_federativa):
        assert str(unidade_federativa) == "Unidade Federativa X"


class TestMunicipio:

    def test_str(self, municipio):
        assert str(municipio) == "Município X"
