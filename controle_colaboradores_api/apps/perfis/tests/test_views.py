import json

import pytest
from django.contrib.auth.hashers import make_password
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from controle_colaboradores_api.apps.perfis.models import Perfil, Departamento


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
def perfil(usuario):
    return baker.make('Perfil',
                      usuario=usuario,
                      nome='Fulano',
                      sobrenome='de Tal',
                      cpf='000')


@pytest.fixture
def grupo_administradores():
    return baker.make('auth.Group',
                      name="Administradores")


@pytest.fixture
def grupo_colaboradores():
    return baker.make('auth.Group',
                      name="Colaboradores")


@pytest.fixture
def departamento(perfil):
    return baker.make('Departamento',
                      nome='Departamento Produtivo',
                      diretor=perfil,
                      diretor_substituto=perfil)


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
        # - sem nenhum departamento atrelado ao perfil
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 0
        # - com departamento atrelado ao perfil
        usuario.perfil.departamentos.add(departamento)
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 1
        assert results[0]['nome'] == "Departamento Produtivo"

        # do grupo Administradores
        usuario.perfil.departamentos.clear()  # limpando, porque admins listam mesmo sem vínculo
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 1
        assert results[0]['nome'] == "Departamento Produtivo"

    def test_retrieve(self,
                      db,
                      api_client,
                      usuario,
                      grupo_administradores,
                      grupo_colaboradores,
                      departamento):
        endpoint_url = reverse('departamento-detail', args=[departamento.id])

        # Por Anônimo
        response = api_client.get(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        # - sem nenhum departamento atrelado ao perfil
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url)
        assert response.status_code == 404
        # - com departamento atrelado ao perfil
        usuario.perfil.departamentos.add(departamento)
        response = api_client.get(endpoint_url)
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Departamento Produtivo"

        # do grupo Administradores
        usuario.perfil.departamentos.clear()  # limpando, porque admins listam mesmo sem vínculo
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Departamento Produtivo"

    def test_create(self,
                    db,
                    api_client,
                    usuario,
                    perfil,
                    grupo_administradores,
                    grupo_colaboradores):

        endpoint_url = reverse('departamento-list')
        usuario_url = 'http://testserver' + reverse('customusuario-detail',
                                                   args=[usuario.id])
        perfil_url = 'http://testserver' + reverse('perfil-detail',
                                                   args=[perfil.id])
        json_para_post = {
            'nome': 'Departamento Bom',
            'diretor': perfil_url,
            'diretor_substituto': None,
            'departamento_superior': None
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
        departamento_criado = Departamento.objects.last()
        departamento_criado_url = 'http://testserver' + \
                                  reverse('departamento-detail',
                                          args=[departamento_criado.id])
        expected_json = {
            'url': departamento_criado_url,
            'id': departamento_criado.id,
            'criacao': departamento_criado.criacao.astimezone().isoformat(),
            'modificacao': departamento_criado.modificacao.astimezone().isoformat(),
            'ativo': departamento_criado.ativo,
            'usuario_modificacao': usuario_url,
            'nome': departamento_criado.nome,
            'diretor': perfil_url,
            'diretor_substituto': departamento_criado.diretor_substituto,
            'departamento_superior': departamento_criado.departamento_superior,
        }
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json