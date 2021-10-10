import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError as rest_ValidationError
from model_bakery import baker
from pycpfcnpj import gen

from controle_colaboradores_api.apps.perfis.serializers import (
    EnderecoSerializer,
    TelefoneSerializer,
    CargoSerializer,
    CargoMudarAtivacaoSerializer,
    DepartamentoSerializer,
    DepartamentoMudarAtivacaoSerializer,
    PerfilSerializer
)

@pytest.fixture
def usuario():
    return baker.make('CustomUsuario',
                      email="usuario@email.com",
                      password=make_password("usuario"))

@pytest.fixture
def outro_usuario():
    return baker.make('CustomUsuario',
                      email="outro_usuario@email.com",
                      password=make_password("outro_usuario"))


@pytest.fixture
def perfil(usuario):
    return baker.make('Perfil',
                      usuario=usuario,
                      nome='Fulano',
                      sobrenome='de Tal',
                      cpf='000')


@pytest.fixture
def outro_perfil(outro_usuario):
    return baker.make('Perfil',
                      usuario=outro_usuario,
                      nome='Beltrano',
                      sobrenome='de Longe',
                      cpf='111')


@pytest.fixture
def cargo():
    return baker.make('Cargo')


@pytest.fixture
def departamento(perfil):
    return baker.make('Departamento',
                      nome='Departamento Produtivo',
                      diretor=perfil,
                      diretor_substituto=perfil)


class TestEnderecoSerializer:

    @pytest.fixture
    def serializer(self):
        return EnderecoSerializer()

    def test_validate_cep(self, serializer):
        assert serializer.validate_cep("00000-000")
        with pytest.raises(rest_ValidationError):
            serializer.validate_cep('00000000')


class TestTelefoneSerializer:

    @pytest.fixture
    def serializer(self):
        return TelefoneSerializer()

    def test_validate_numero(self, serializer):
        assert serializer.validate_numero("(00) 0000-0000")
        assert serializer.validate_numero("(00) 00000-0000")
        with pytest.raises(rest_ValidationError):
            serializer.validate_numero('00000000')


class TestCargoSerializer:

    @pytest.fixture
    def serializer(self):
        return CargoSerializer()

    def test_validate_salario(self, serializer):
        assert serializer.validate_salario(1)
        with pytest.raises(rest_ValidationError):
            serializer.validate_salario(0)


class TestCargoMudarAtivacaoSerializer:

    @pytest.fixture
    def serializer(self, db, cargo):
        return CargoMudarAtivacaoSerializer(cargo)

    def test_update(self, serializer):
        assert serializer.instance.ativo is True
        validated_data = {'ativo': False}
        serializer.update(serializer.instance, validated_data)
        assert serializer.instance.ativo is False


class TestDepartamentoSerializer:

    @pytest.fixture
    def serializer(self, db, departamento):
        return DepartamentoSerializer(departamento)

    def test_validate_departamento_superior(self, serializer, departamento, outro_perfil):
        with pytest.raises(rest_ValidationError):
            serializer.validate_departamento_superior(departamento)
        outro_departamento = baker.make('Departamento', nome="Outro Departamento", diretor=outro_perfil)
        serializer.instance.departamento_superior = outro_departamento
        serializer.instance.save()
        assert serializer.validate_departamento_superior(outro_departamento)

    def test_validate(self, serializer, perfil, outro_perfil):
        with pytest.raises(rest_ValidationError):
            serializer.validate({"diretor": perfil, "diretor_substituto": perfil})
        assert serializer.validate({"diretor": perfil, "diretor_substituto": outro_perfil})

    def test_validate_diretor(self, serializer, perfil):
        with pytest.raises(rest_ValidationError):
            serializer.validate({"diretor": perfil})
        serializer.instance.diretor_substituto = None
        serializer.instance.save()
        assert serializer.validate({"diretor": perfil})

    def test_validate_diretor_substituto(self, serializer, perfil, outro_perfil):
        with pytest.raises(rest_ValidationError):
            serializer.validate({"diretor_substituto": perfil})
        serializer.instance.diretor = outro_perfil
        serializer.instance.save()
        assert serializer.validate({"diretor_substituto": perfil})


class TesteDepartamentoMudarAtivacaoSerializer:

    @pytest.fixture
    def serializer(self, db, departamento):
        return DepartamentoMudarAtivacaoSerializer(departamento)

    def test_update(self, serializer):
        assert serializer.instance.ativo is True
        validated_data = {'ativo': False}
        serializer.update(serializer.instance, validated_data)
        assert serializer.instance.ativo is False


class TestePerfilSerializer:

    @pytest.fixture
    def serializer(self):
        return PerfilSerializer()

    def test_validate_cpf(self, serializer):
        assert serializer.validate_cpf(gen.cpf_with_punctuation())
        with pytest.raises(rest_ValidationError):
            serializer.validate_cpf('00000000000')
            serializer.validate_cpf('000.000.000-00')





