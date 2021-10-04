import json

import pytest
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
                      password="usuario")


@pytest.fixture
def grupo_administradores():
    return baker.make('auth.Group',
                      name="Administradores")


@pytest.fixture
def grupo_colaboradores():
    return baker.make('auth.Group',
                      name="Colaboradores")


class TestCustomUsuarioViewSet:

    def test_list(self,
                  db,
                  api_client,
                  usuario,
                  grupo_colaboradores,
                  grupo_administradores):
        baker.make('CustomUsuario', _quantity=3)

        # Por Anônimo
        response = api_client.get(reverse('customusuario-list'))
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(reverse('customusuario-list'))
        assert response.status_code == 403
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(reverse('customusuario-list'))
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 4
        assert results[0]['email'] == "usuario@email.com"

    def test_retrieve(self,
                      db,
                      api_client,
                      usuario,
                      grupo_colaboradores,
                      grupo_administradores):
        outro_usuario = baker.make('CustomUsuario',
                                   email="outrousuario@email.com")

        # Por Anônimo
        response = api_client.get(
            reverse('customusuario-detail', args=[usuario.id])
        )
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        # - consultando si mesmo:
        response = api_client.get(
            reverse('customusuario-detail', args=[usuario.id])
        )
        assert response.status_code == 200
        assert json.loads(response.content)['email'] == "usuario@email.com"
        # - consultando outro usuário:
        response = api_client.get(
            reverse('customusuario-detail', args=[outro_usuario.id])
        )
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        # - consultando si mesmo:
        response = api_client.get(
            reverse('customusuario-detail', args=[usuario.id])
        )
        assert response.status_code == 200
        assert json.loads(response.content)['email'] == "usuario@email.com"
        # - consultando terceiros:
        response = api_client.get(
            reverse('customusuario-detail', args=[outro_usuario.id])
        )
        assert response.status_code == 200
        assert json.loads(response.content)['email'] == "outrousuario@email.com"

    def test_create(self,
                    db,
                    api_client,
                    usuario,
                    grupo_colaboradores,
                    grupo_administradores):

        novo_usuario = baker.prepare('CustomUsuario')

        json_para_post = {
            'email': novo_usuario.email,
            'password': "senha1234",
            'groups': []
        }

        # Por Anônimo
        response = api_client.post(
            reverse('customusuario-list'),
            data=json_para_post,
            format='json'
        )
        assert response.status_code == 401

        # Usuário autenticado
        api_client.force_authenticate(user=usuario)

        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.post(
            reverse('customusuario-list'),
            data=json_para_post,
            format='json'
        )
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.post(
            reverse('customusuario-list'),
            data=json_para_post,
            format='json'
        )
        usuario_criado = CustomUsuario.objects.last()
        usuario_criado_url = 'http://testserver'+\
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

        # TODO continuar test próximas actions do CustomUsuarioViewSet