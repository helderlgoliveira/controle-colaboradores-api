import pytest
from model_bakery import baker

from controle_colaboradores_api.apps.municipios.models import Municipio
from controle_colaboradores_api.apps.perfis.models import \
    Perfil, \
    Telefone, \
    OutroEmail, \
    MunicipioOndeTrabalha


@pytest.fixture
def municipio(db):
    return baker.make(Municipio,
                      nome="Município X")


@pytest.fixture
def perfil(db):
    return baker.make(Perfil,
                      usuario__email="helder.lima@dominio.com.br",
                      nome="Hélder",
                      sobrenome="Lima")

@pytest.fixture
def telefone(db, perfil):
    return baker.make(Telefone,
                      perfil=perfil,
                      numero="(82) 99999-9999")

@pytest.fixture
def outro_email(db, perfil):
    return baker.make(OutroEmail,
                      perfil=perfil,
                      email="helder.lima@outrodominio.com.br")

@pytest.fixture
def municipio_onde_trabalha(db, perfil, municipio):
    return baker.make(MunicipioOndeTrabalha,
                      perfil=perfil,
                      municipio=municipio)


class TestPerfil:

    def test_str(self, perfil):
        assert str(perfil) == "helder.lima@dominio.com.br - Hélder Lima"

    def test_save(self, perfil):
        perfil.save()
        assert perfil.usuario.first_name == "Hélder"
        assert perfil.usuario.last_name == "Lima"


class TestTelefone:

    def test_str(self, telefone):
        assert str(telefone) == "(82) 99999-9999"


class TestOutroEmail:

    def test_str(self, outro_email):
        assert str(outro_email) == "helder.lima@outrodominio.com.br"


class TestMunicipioOndeTrabalhao:

    def test_str(self, municipio_onde_trabalha):
        assert str(municipio_onde_trabalha) == "helder.lima@dominio.com.br - Município X"