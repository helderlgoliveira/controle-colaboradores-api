import pytest
from model_bakery import baker


@pytest.fixture
def municipio(db):
    return baker.make('localidades_brasileiras.Municipio',
                      nome="Município X",
                      uf__sigla="AZ")


@pytest.fixture
def perfil(db, municipio):
    return baker.make('Perfil',
                      usuario__email="helder.lima@dominio.com.br",
                      nome="Hélder",
                      sobrenome="Lima",
                      municipios_onde_trabalha=[municipio])


@pytest.fixture
def telefone(db, perfil):
    return baker.make('Telefone',
                      perfil=perfil,
                      numero="(82) 99999-9999")


@pytest.fixture
def outro_email(db, perfil):
    return baker.make('OutroEmail',
                      perfil=perfil,
                      email="helder.lima@outrodominio.com.br")


@pytest.fixture
def endereco(db, perfil, municipio):
    return baker.make('Endereco',
                      perfil=perfil,
                      is_principal=False,
                      logradouro="Rua X",
                      numero="99",
                      bairro="Bairro Y",
                      complemento="Loteamento Z",
                      municipio=municipio,
                      cep="57000-000")


@pytest.fixture
def cargo(db, perfil):
    return baker.make('Cargo',
                      nome="Desenvolvedor Sênior",
                      classe="Classe A",
                      salario=12300.50)


@pytest.fixture
def departamento(db, perfil):
    return baker.make('Departamento',
                      nome="Diretoria de TI",
                      diretor=perfil.usuario)


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


class TestEndereco:

    def test_str(self, endereco):
        assert str(endereco) == \
               f"helder.lima@dominio.com.br - Rua X, 99, Bairro Y, " \
               f"Loteamento Z, Município X-AZ, 57000-000."


class TestCargo:

    def test_str(self, cargo):
        assert str(cargo) == "Desenvolvedor Sênior - Classe A"


class TestDepartamento:

    def test_str(self, departamento):
        assert str(departamento) == "Diretoria de TI"
