import json

import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from controle_colaboradores_api.apps.usuarios.models import CustomUsuario


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_forced_csrf():
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def usuario():
    return baker.make('CustomUsuario',
                      email="usuario@email.com",
                      password=make_password("usuario"))


@pytest.fixture
def outro_usuario():
    return baker.make('CustomUsuario',
                      email="outrousuario@email.com")


@pytest.fixture
def grupo_administradores():
    return baker.make('auth.Group',
                      name="Administradores")


@pytest.fixture
def grupo_colaboradores():
    return baker.make('auth.Group',
                      name="Colaboradores")


@pytest.fixture
def password_reset_token(usuario):
    return baker.make('PasswordResetToken',
                      usuario=usuario)


class TestCustomUsuarioViewSet:

    def test_list(self,
                  db,
                  api_client,
                  usuario,
                  grupo_colaboradores,
                  grupo_administradores):
        baker.make('CustomUsuario', _quantity=3)
        endpoint_url = reverse('customusuario-list')

        # Por Anônimo
        response = api_client.get(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url)
        assert response.status_code == 403
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 4
        assert results[0]['email'] == "usuario@email.com"

    def test_retrieve(self,
                      db,
                      api_client,
                      usuario,
                      outro_usuario,
                      grupo_colaboradores,
                      grupo_administradores):
        endpoint_url_usuario = reverse('customusuario-detail', args=[usuario.id])
        endpoint_url_outro_usuario = reverse('customusuario-detail', args=[outro_usuario.id])
        # Por Anônimo
        response = api_client.get(endpoint_url_usuario)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        # - consultando si mesmo:
        response = api_client.get(endpoint_url_usuario)
        assert response.status_code == 200
        assert json.loads(response.content)['email'] == "usuario@email.com"
        # - consultando outro usuário:
        response = api_client.get(endpoint_url_outro_usuario)
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        # - consultando si mesmo:
        response = api_client.get(endpoint_url_usuario)
        assert response.status_code == 200
        assert json.loads(response.content)['email'] == "usuario@email.com"
        # - consultando terceiros:
        response = api_client.get(endpoint_url_outro_usuario)
        assert response.status_code == 200
        assert json.loads(response.content)['email'] == "outrousuario@email.com"

    def test_create(self,
                    db,
                    api_client,
                    usuario,
                    grupo_colaboradores,
                    grupo_administradores):
        novo_usuario = baker.prepare('CustomUsuario')
        endpoint_url = reverse('customusuario-list')

        json_para_post = {
            'email': novo_usuario.email,
            'password': "senha1234",
            'groups': []
        }

        # Por Anônimo
        response = api_client.post(
            endpoint_url,
            data=json_para_post,
            format='json'
        )
        assert response.status_code == 401

        # Usuário autenticado
        api_client.force_authenticate(user=usuario)

        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.post(
            endpoint_url,
            data=json_para_post,
            format='json'
        )
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.post(
            endpoint_url,
            data=json_para_post,
            format='json'
        )
        usuario_criado = CustomUsuario.objects.last()
        usuario_criado_url = 'http://testserver' + \
                             reverse('customusuario-detail',
                                     args=[usuario_criado.id])
        expected_json = {
            'url': usuario_criado_url,
            'id': usuario_criado.id,
            'email': novo_usuario.email,
            'groups': []
        }
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_mudar_password(self,
                            db,
                            api_client,
                            usuario,
                            outro_usuario,
                            grupo_colaboradores,
                            grupo_administradores):
        json_para_patch = {
            'password': 'usuario',
            'nova_senha': 'senha1234'
        }
        endpoint_url_usuario = reverse('customusuario-mudar-password', args=[usuario.id])
        endpoint_url_outro_usuario = reverse('customusuario-mudar-password', args=[outro_usuario.id])
        # Por Anônimo
        response = api_client.patch(
            endpoint_url_usuario,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 401

        # Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # - mudando a própria senha:
        response = api_client.patch(
            endpoint_url_usuario,
            data=json_para_patch,
            format='json'
        )
        usuario.refresh_from_db()
        assert response.status_code == 200
        assert usuario.check_password('senha1234')
        # - mudando a senha de outro usuário:
        response = api_client.patch(
            endpoint_url_outro_usuario,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 403

    def test_mudar_password_apos_reset(self,
                                       db,
                                       api_client,
                                       usuario,
                                       password_reset_token):
        json_para_patch = {
            'nova_senha': 'senha1234'
        }
        endpoint_url = reverse('customusuario-mudar-password-apos-reset', args=[usuario.id])
        endpoint_url_com_token_invalido = endpoint_url+"?token=00000000"
        endpoint_url_com_token_valido = endpoint_url+"?token="+password_reset_token.token

        # Sem token
        response = api_client.patch(
            endpoint_url,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 400
        assert json.loads(response.content)['status'] == "Token não informado."

        # Com token inválido
        response = api_client.patch(
            endpoint_url_com_token_invalido,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 400
        assert json.loads(response.content)['status'] == "Token inválido."

        # Com token válido
        response = api_client.patch(
            endpoint_url_com_token_valido,
            data=json_para_patch,
            format='json'
        )
        usuario.refresh_from_db()
        password_reset_token.refresh_from_db()
        assert response.status_code == 200
        assert usuario.check_password('senha1234')
        assert password_reset_token.ativo is False

    def test_mudar_email(self,
                         db,
                         api_client,
                         usuario,
                         outro_usuario):
        json_para_patch = {
            'email': 'novoemail@email.com',
            'password': 'usuario'
        }
        endpoint_url_usuario = reverse('customusuario-mudar-email', args=[usuario.id])
        endpoint_url_outro_usuario = reverse('customusuario-mudar-email', args=[outro_usuario.id])

        # Por Anônimo
        response = api_client.patch(
            endpoint_url_usuario,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 401

        # Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # - mudando o próprio e-mail:
        response = api_client.patch(
            endpoint_url_usuario,
            data=json_para_patch,
            format='json'
        )
        usuario.refresh_from_db()
        assert response.status_code == 200
        assert usuario.email == "novoemail@email.com"
        # - mudando o e-mail de outro usuário:
        response = api_client.patch(
            endpoint_url_outro_usuario,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 403

    def test_mudar_grupo(self,
                         db,
                         api_client,
                         usuario,
                         grupo_colaboradores,
                         grupo_administradores):
        json_para_patch = {
            'groups': [grupo_colaboradores.id]
        }
        endpoint_url = reverse('customusuario-mudar-grupo', args=[usuario.id])

        # Por Anônimo
        response = api_client.patch(endpoint_url, data=json_para_patch, format='json')
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.patch(endpoint_url, data=json_para_patch, format='json')
        assert response.status_code == 403
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.patch(endpoint_url, data=json_para_patch, format='json')
        usuario.refresh_from_db()
        print(json.loads(response.content))
        print("\n"+str(grupo_colaboradores.id))
        assert response.status_code == 200
        assert usuario.groups.all().count() == 1
        assert usuario.groups.filter(id=grupo_colaboradores.id).exists()


    def test_ativar(self,
                    db,
                    api_client,
                    usuario,
                    grupo_colaboradores,
                    grupo_administradores):
        pass

    def test_desativar(self,
                       db,
                       api_client,
                       usuario,
                       grupo_colaboradores,
                       grupo_administradores):
        pass
