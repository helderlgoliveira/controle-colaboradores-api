from datetime import timedelta

import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError as rest_ValidationError
from django.core.exceptions import ValidationError
from model_bakery import baker


@pytest.fixture
def usuario():
    return baker.make('CustomUsuario',
                      email="usuario@email.com",
                      password=make_password("usuario"))


@pytest.fixture
def token(usuario):
    return baker.make('PasswordResetToken',
                      usuario=usuario)


@pytest.fixture
def grupo_colaboradores():
    return baker.make('auth.Group',
                      name="Colaboradores")


from controle_colaboradores_api.apps.usuarios.serializers import (
    CustomUsuarioSerializer,
    CustomUsuarioMudarPasswordSerializer,
    CustomUsuarioMudarPasswordAposResetSerializer,
    CustomUsuarioMudarEmailSerializer,
    CustomUsuarioMudarGrupoSerializer,
    CustomUsuarioMudarAtivacaoSerializer,
    PasswordResetTokenSerializer
)


class TestCustomUsuarioSerializer:
    serializer = CustomUsuarioSerializer()

    def test_validate_password(self):
        with pytest.raises(ValidationError):
            self.serializer.validate_password('1234')
        assert self.serializer.validate_password('aczxc1234')

    def test_create(self, db, grupo_colaboradores):
        validated_data = {
            'email': 'fulano@email.com',
            'password': 'aczxc1234',
            'groups': [grupo_colaboradores.id]
        }
        usuario = self.serializer.create(validated_data)
        assert usuario.id
        assert usuario.groups.filter(id=grupo_colaboradores.id).exists()


class TestCustomUsuarioMudarPasswordSerializer:

    @pytest.fixture
    def serializer(self, db, usuario):
        return CustomUsuarioMudarPasswordSerializer(usuario)

    def test_validate_password(self, serializer):
        with pytest.raises(rest_ValidationError):
            assert serializer.validate_password('0000')
        assert serializer.validate_password('usuario')

    def test_validate_nova_senha(self, serializer):
        with pytest.raises(ValidationError):
            serializer.validate_nova_senha('1234')
        assert serializer.validate_nova_senha('aczxc1234')

    def test_update(self, serializer):
        assert serializer.instance.check_password('usuario')
        validated_data = {'nova_senha': 'aczxc1234'}
        serializer.update(serializer.instance, validated_data)
        assert serializer.instance.check_password('aczxc1234')


class TestCustomUsuarioMudarPasswordAposResetSerializer:

    @pytest.fixture
    def serializer(self, db, usuario):
        return CustomUsuarioMudarPasswordAposResetSerializer(usuario)

    def test_validate_nova_senha(self, serializer):
        with pytest.raises(ValidationError):
            serializer.validate_nova_senha('1234')
        assert serializer.validate_nova_senha('aczxc1234')

    def test_update(self, serializer):
        assert serializer.instance.check_password('usuario')
        validated_data = {'nova_senha': 'aczxc1234'}
        serializer.update(serializer.instance, validated_data)
        assert serializer.instance.check_password('aczxc1234')


class TestCustomUsuarioMudarEmailSerializer:

    @pytest.fixture
    def serializer(self, db, usuario):
        return CustomUsuarioMudarEmailSerializer(usuario)

    def test_update(self, serializer):
        assert serializer.instance.email == 'usuario@email.com'
        validated_data = {'email': 'novoemail@novoemail.com'}
        serializer.update(serializer.instance, validated_data)
        assert serializer.instance.email == 'novoemail@novoemail.com'


class TestCustomUsuarioMudarGrupoSerializer:

    @pytest.fixture
    def serializer(self, db, usuario):
        return CustomUsuarioMudarGrupoSerializer(usuario)

    def test_update(self, db, serializer, grupo_colaboradores):
        assert serializer.instance.groups.count() == 0
        validated_data = {'groups': [grupo_colaboradores.id]}
        serializer.update(serializer.instance, validated_data)
        assert serializer.instance.groups \
            .filter(id=grupo_colaboradores.id).exists()


class TestCustomUsuarioMudarAtivacaoSerializer:

    @pytest.fixture
    def serializer(self, db, usuario):
        return CustomUsuarioMudarAtivacaoSerializer(usuario)

    def test_update(self, serializer, grupo_colaboradores):
        assert serializer.instance.is_active is True
        validated_data = {'is_active': False}
        serializer.update(serializer.instance, validated_data)
        assert serializer.instance.is_active is False


class TestPasswordResetTokenSerializer:

    @pytest.fixture
    def serializer(self, db, token):
        return PasswordResetTokenSerializer(token)

    def test_validate(self, serializer, token):
        # Token válido
        assert serializer.validate({"usuario": token.usuario,
                                    "token": token.token})
        # Token inativo (já utilizado)
        token.ativo = False
        token.save()
        with pytest.raises(rest_ValidationError) as e_info:
            serializer.validate({"usuario": token.usuario,
                                 "token": token.token})
            assert e_info.value == "Token já utilizado."
        # Token com prazo expirado
        token.ativo = True
        token.criacao -= timedelta(days=1)
        token.save()
        with pytest.raises(rest_ValidationError) as e_info:
            serializer.validate({"usuario": token.usuario,
                                 "token": token.token})
            assert e_info.value == "Token expirado."

    def test_create(self, serializer, token):
        # Se houver token ativo pendente, ele será retornado
        assert serializer.create({"usuario": token.usuario}) == token

        # Se não houver token ativo pendente, será criado um novo
        token.ativo = False
        token.save()
        novo_token = serializer.create({"usuario": token.usuario})
        assert novo_token.id
        assert novo_token != token


    def test_update(self, serializer, token):
        assert token.ativo is True
        serializer.update(token, {'ativo': False})
        assert token.ativo is False

