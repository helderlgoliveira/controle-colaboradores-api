import json

import pytest
from django.contrib.auth.hashers import make_password
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from controle_colaboradores_api.apps.perfis.models import Perfil


@pytest.fixture
def api_client():
    return APIClient()


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


class TestPerfilViewSet:
    # TODO
    pass


class TestEnderecoViewSet:
    # TODO
    pass


class TestTelefoneViewSet:
    # TODO
    pass


class TestOutroEmailViewSet:
    # TODO
    pass


class TestCargoViewSet:
    # TODO
    pass


class TestDepartamentoViewSet:

    def test_list(self,
                  db,
                  api_client,
                  usuario,
                  grupo_administradores,
                  grupo_colaboradores,
                  departamento):
        endpoint_url = reverse('departamento-list')

        # Por Anônimo
        response = api_client.get(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url)
        assert response.status_code == 200
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 2
        assert results[0]['name'] == "Administradores"