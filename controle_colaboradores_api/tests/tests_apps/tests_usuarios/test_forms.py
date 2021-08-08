import pytest
# from model_bakery import baker

from controle_colaboradores_api.apps.usuarios.forms import CustomUsuarioCreateForm


class TestCustomUsuarioCreateForm:

    def test_save(self, db):
        novo_usuario = CustomUsuarioCreateForm(data={"username": "helder.lima@dominio.com.br",
                                                     "password1": "senha123123*",
                                                     "password2": "senha123123*"})
        novo_usuario.save()

        assert novo_usuario.cleaned_data['username'] == "helder.lima@dominio.com.br"
        assert novo_usuario.cleaned_data['password1'] == "senha123123*"
