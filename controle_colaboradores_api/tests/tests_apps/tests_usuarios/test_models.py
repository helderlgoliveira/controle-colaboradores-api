import pytest
# from model_bakery import baker

from controle_colaboradores_api.apps.usuarios.models import CustomUsuario


class TestUsuarioCustomizadoManager:

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
