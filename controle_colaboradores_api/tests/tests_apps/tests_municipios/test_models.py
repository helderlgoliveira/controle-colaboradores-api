import pytest
from model_bakery import baker

from controle_colaboradores_api.apps.municipios.models import \
    Macrorregiao, \
    Mesorregiao, \
    Microrregiao, \
    RegiaoSaude, \
    UnidadeFederativa, \
    Municipio


@pytest.fixture
def macrorregiao(db):
    return baker.make(Macrorregiao,
                      nome="Macrorregião X")

@pytest.fixture
def mesorregiao(db):
    return baker.make(Mesorregiao,
                      nome="Mesorregião X")


@pytest.fixture
def microrregiao(db):
    return baker.make(Microrregiao,
                      nome="Microrregião X")


@pytest.fixture
def regiao_saude(db):
    return baker.make(RegiaoSaude,
                      numero=1)


@pytest.fixture
def unidade_federativa(db):
    return baker.make(UnidadeFederativa,
                      nome="Unidade Federativa X")


@pytest.fixture
def municipio(db):
    return baker.make(Municipio,
                      nome="Município X")


class TestMacrorregiao:

    def test_str(self, macrorregiao):
        assert str(macrorregiao) == "Macrorregião X"


class TestMesorregiao:

    def test_str(self, mesorregiao):
        assert str(mesorregiao) == "Mesorregião X"


class TestMicrorregiao:

    def test_str(self, microrregiao):
        assert str(microrregiao) == "Microrregião X"


class TestRegiaoSaude:

    def test_str(self, regiao_saude):
        assert str(regiao_saude) == '1'


class TestUnidadeFederativa:

    def test_str(self, unidade_federativa):
        assert str(unidade_federativa) == "Unidade Federativa X"


class TestMunicipio:

    def test_str(self, municipio):
        assert str(municipio) == "Município X"
