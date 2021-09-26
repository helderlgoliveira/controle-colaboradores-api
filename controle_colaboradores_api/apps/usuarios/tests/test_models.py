from datetime import timedelta
from django.utils import timezone

import pytest
from model_bakery import baker
import controle_colaboradores_api.apps.usuarios.models


from controle_colaboradores_api.apps.usuarios.models import CustomUsuario


@pytest.fixture
def usuario(db):
    return baker.make('CustomUsuario',
                      email="helder.lima@dominio.com.br",
                      perfil__nome="Hélder",
                      perfil__sobrenome="Lima")


@pytest.fixture
def password_reset_token(db, usuario):
    return baker.make('PasswordResetToken',
                      usuario=usuario,
                      criacao=timezone.now())


class TestCustomUsuarioManager:

    def test_create_user(self, db):
        novo_usuario = CustomUsuario.objects.create_user(email="helder.lima@dominio.com.br",
                                                         password="senha")
        assert novo_usuario.is_staff is False
        assert novo_usuario.is_superuser is False

    def test_create_user_informando_email_nulo(self, db):
        with pytest.raises(ValueError):
            CustomUsuario.objects.create_user(email=None, password="senha")

    def test_create_user_sem_informar_senha(self, db):
        with pytest.raises(Exception):
            CustomUsuario.objects.create_user(email="helder.lima@dominio.com.br")

    def test_create_superuser(self, db):
        novo_usuario = CustomUsuario.objects.create_superuser(email="helder.lima@dominio.com.br",
                                                              password="senha")
        assert novo_usuario.is_staff is True
        assert novo_usuario.is_superuser is True

    def test_create_superuser_informando_superuser_false(self, db):
        with pytest.raises(ValueError):
            CustomUsuario.objects.create_superuser(email="email",
                                                   password="senha",
                                                   is_superuser=False)

    def test_create_superuser_informando_staff_false(self, db):
        with pytest.raises(ValueError):
            CustomUsuario.objects.create_superuser(email="email",
                                                   password="senha",
                                                   is_staff=False)


class TestCustomUsuario:

    def test_str(self, usuario):
        assert str(usuario) == "helder.lima@dominio.com.br"


class TestPasswordResetToken:

    def test_expirado(self, password_reset_token):
        assert password_reset_token.expirado is False

        password_reset_token.criacao -= timedelta(days=1)
        assert password_reset_token.expirado is True

    def test_gerar_token(self, password_reset_token):
        token_length = len(password_reset_token.gerar_token())
        assert 40 <= token_length <= 60

    def test_save(self, mocker, password_reset_token):
        spy = mocker.spy(controle_colaboradores_api.apps.usuarios.models, 'send_mail')
        password_reset_token.save()

        assert spy.call_count == 1
        assert spy.spy_return == 1

        assert 40 <= len(password_reset_token.token) <= 60
