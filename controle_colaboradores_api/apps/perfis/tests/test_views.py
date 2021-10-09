import json

import pytest
from django.contrib.auth.hashers import make_password
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from controle_colaboradores_api.apps.perfis.models import (
    Perfil, Departamento, Cargo, OutroEmail
)


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
def outro_perfil(outro_usuario):
    return baker.make('Perfil',
                      usuario=outro_usuario,
                      nome='Beltrano',
                      sobrenome='de Longe',
                      cpf='111')


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


@pytest.fixture
def cargo():
    return baker.make('Cargo',
                      nome='Desenvolvedor Python',
                      classe='Classe A',
                      salario='13500.80')


@pytest.fixture
def outro_email(perfil):
    return baker.make('OutroEmail',
                      perfil=perfil,
                      email='outro_email@email.com')


@pytest.fixture
def telefone(perfil):
    return baker.make('Telefone',
                      perfil=perfil,
                      numero='(88) 88888-8888')


@pytest.fixture
def outro_telefone(outro_perfil):
    return baker.make('Telefone',
                      perfil=outro_perfil,
                      numero='(99) 99999-9999')


@pytest.fixture
def endereco(perfil):
    return baker.make('Endereco',
                      perfil=perfil,
                      is_principal=True)


@pytest.fixture
def outro_endereco(outro_perfil):
    return baker.make('Endereco',
                      perfil=outro_perfil,
                      is_principal=True)


class TestPerfilViewSet:
    # TODO
    pass


class TestEnderecoViewSet:
    # TODO Continuar daqui, copiar do OutroEmail/Telefone
    pass


class TestTelefoneViewSet:

    def test_list(self,
                  db,
                  api_client,
                  usuario,
                  outro_perfil,
                  telefone,
                  outro_telefone,
                  grupo_administradores,
                  grupo_colaboradores):

        endpoint_url = reverse('telefone-list')

        # Por Anônimo
        response = api_client.get(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 1
        assert results[0]['numero'] == '(88) 88888-8888'

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 2
        assert results[1]['numero'] == '(99) 99999-9999'

    def test_retrieve(self,
                      db,
                      api_client,
                      usuario,
                      outro_perfil,
                      telefone,
                      outro_telefone,
                      grupo_administradores,
                      grupo_colaboradores):

        endpoint_url_telefone = reverse('telefone-detail', args=[telefone.id])
        endpoint_url_outro_telefone = reverse('telefone-detail', args=[outro_telefone.id])

        # Por Anônimo
        response = api_client.get(endpoint_url_telefone)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        # - consultando telefone do próprio usuário
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url_telefone)
        assert response.status_code == 200
        assert json.loads(response.content)['numero'] == "(88) 88888-8888"
        # - consultando telefone de outro usuário
        response = api_client.get(endpoint_url_outro_telefone)
        assert response.status_code == 404

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url_outro_telefone)
        assert response.status_code == 200
        assert json.loads(response.content)['numero'] == "(99) 99999-9999"

    # TODO continuar dos outros methods igual OutroEmail

class TestOutroEmailViewSet:

    def test_list(self,
                  db,
                  api_client,
                  usuario,
                  outro_perfil,
                  outro_email,
                  grupo_administradores,
                  grupo_colaboradores):
        baker.make('OutroEmail', perfil=outro_perfil, email="email_diferente@email.com")
        endpoint_url = reverse('outroemail-list')

        # Por Anônimo
        response = api_client.get(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 1
        assert results[0]['email'] == "outro_email@email.com"

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 2
        assert results[1]['email'] == "email_diferente@email.com"

    def test_retrieve(self,
                      db,
                      api_client,
                      usuario,
                      outro_perfil,
                      outro_email,
                      grupo_administradores,
                      grupo_colaboradores):
        endpoint_url = reverse('outroemail-detail', args=[outro_email.id])

        # Por Anônimo
        response = api_client.get(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        # - consultando email do próprio usuário
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url)
        assert response.status_code == 200
        assert json.loads(response.content)['email'] == "outro_email@email.com"
        # - consultando email de outro usuário
        outro_email.perfil = outro_perfil
        outro_email.save()
        response = api_client.get(endpoint_url)
        assert response.status_code == 404

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        assert response.status_code == 200
        assert json.loads(response.content)['email'] == "outro_email@email.com"

    def test_create(self,
                    db,
                    api_client,
                    usuario,
                    perfil,
                    outro_email,
                    grupo_administradores,
                    grupo_colaboradores):
        endpoint_url = reverse('outroemail-list')
        usuario_url = 'http://testserver' + reverse('customusuario-detail',
                                                    args=[usuario.id])
        perfil_url = 'http://testserver' + reverse('perfil-detail',
                                                   args=[perfil.id])
        json_para_post = {
            'perfil': perfil_url,
            'email': 'novo_email@email.com'
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
        email_criado = OutroEmail.objects.last()
        email_criado_url = 'http://testserver' + \
                           reverse('outroemail-detail',
                                   args=[email_criado.id])
        expected_json = {
            'url': email_criado_url,
            'id': email_criado.id,
            'criacao': email_criado.criacao.astimezone().isoformat(),
            'modificacao': email_criado.modificacao.astimezone().isoformat(),
            'perfil': perfil_url,
            'email': email_criado.email
        }
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        json_para_post['email'] = "outro_novo_email@email.com"
        response = api_client.post(
            endpoint_url,
            data=json_para_post,
            format='json'
        )
        email_criado = OutroEmail.objects.last()
        email_criado_url = 'http://testserver' + \
                           reverse('outroemail-detail',
                                   args=[email_criado.id])
        expected_json = {
            'url': email_criado_url,
            'id': email_criado.id,
            'criacao': email_criado.criacao.astimezone().isoformat(),
            'modificacao': email_criado.modificacao.astimezone().isoformat(),
            'perfil': perfil_url,
            'email': email_criado.email
        }
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_delete(self,
                    db,
                    api_client,
                    usuario,
                    grupo_administradores,
                    grupo_colaboradores,
                    outro_email):
        endpoint_url = reverse('outroemail-detail', args=[outro_email.id])

        segundo_email = baker.make('OutroEmail', perfil=usuario.perfil)
        endpoint_url_segundo_email = reverse('outroemail-detail', args=[segundo_email.id])

        # Por Anônimo
        response = api_client.delete(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.delete(endpoint_url)
        assert response.status_code == 204
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.delete(endpoint_url_segundo_email)
        assert response.status_code == 204


class TestCargoViewSet:

    def test_list(self,
                  db,
                  api_client,
                  usuario,
                  perfil,
                  grupo_administradores,
                  grupo_colaboradores,
                  cargo):
        endpoint_url = reverse('cargo-list')

        # Por Anônimo
        response = api_client.get(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        # - sem nenhum cargo atrelado ao perfil
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 0
        # - com cargo atrelado ao perfil
        usuario.perfil.cargos.add(cargo)
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 1
        assert results[0]['nome'] == "Desenvolvedor Python"

        # do grupo Administradores
        usuario.perfil.cargos.clear()  # limpando, porque admins listam mesmo sem vínculo
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 1
        assert results[0]['nome'] == "Desenvolvedor Python"

    def test_retrieve(self,
                      db,
                      api_client,
                      usuario,
                      perfil,
                      grupo_administradores,
                      grupo_colaboradores,
                      cargo):
        endpoint_url = reverse('cargo-detail', args=[cargo.id])

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
        usuario.perfil.cargos.add(cargo)
        response = api_client.get(endpoint_url)
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Desenvolvedor Python"

        # do grupo Administradores
        usuario.perfil.cargos.clear()  # limpando, porque admins listam mesmo sem vínculo
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Desenvolvedor Python"

    def test_create(self,
                    db,
                    api_client,
                    usuario,
                    perfil,
                    grupo_administradores,
                    grupo_colaboradores):
        endpoint_url = reverse('cargo-list')
        usuario_url = 'http://testserver' + reverse('customusuario-detail',
                                                    args=[usuario.id])

        json_para_post = {
            'nome': 'Desenvolvedor Web - Django',
            'classe': 'Classe A',
            'salario': '13500.80'
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
        cargo_criado = Cargo.objects.last()
        cargo_criado_url = 'http://testserver' + \
                           reverse('cargo-detail',
                                   args=[cargo_criado.id])
        expected_json = {
            'url': cargo_criado_url,
            'id': cargo_criado.id,
            'criacao': cargo_criado.criacao.astimezone().isoformat(),
            'modificacao': cargo_criado.modificacao.astimezone().isoformat(),
            'ativo': cargo_criado.ativo,
            'usuario_modificacao': usuario_url,
            'nome': cargo_criado.nome,
            'classe': cargo_criado.classe,
            'salario': str(cargo_criado.salario)
        }
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_update(self,
                    db,
                    api_client,
                    usuario,
                    perfil,
                    outro_perfil,
                    grupo_administradores,
                    grupo_colaboradores,
                    cargo):
        endpoint_url = reverse('cargo-detail', args=[cargo.id])

        json_para_put = {
            'nome': 'Desenvolvedor Full-stack - Django/Vue.js',
            'classe': 'Classe A',
            'salario': '18500.80'
        }

        # Por Anônimo
        response = api_client.put(
            endpoint_url,
            data=json_para_put,
            format='json'
        )
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.put(
            endpoint_url,
            data=json_para_put,
            format='json'
        )
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.put(
            endpoint_url,
            data=json_para_put,
            format='json'
        )
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Desenvolvedor Full-stack - Django/Vue.js"

    def test_partial_update(self,
                            db,
                            api_client,
                            usuario,
                            perfil,
                            outro_perfil,
                            grupo_administradores,
                            grupo_colaboradores,
                            cargo):
        endpoint_url = reverse('cargo-detail', args=[cargo.id])
        json_para_patch = {
            'salario': '20180.80'
        }

        # Por Anônimo
        response = api_client.patch(
            endpoint_url,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.patch(
            endpoint_url,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.patch(
            endpoint_url,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 200
        assert json.loads(response.content)['salario'] == '20180.80'

    def test_ativar(self,
                    db,
                    api_client,
                    usuario,
                    grupo_administradores,
                    grupo_colaboradores,
                    cargo):
        endpoint_url = reverse('cargo-ativar', args=[cargo.id])

        # Por Anônimo
        response = api_client.patch(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.patch(endpoint_url)
        assert response.status_code == 403
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        cargo.ativo = False
        cargo.save()
        assert cargo.ativo is False
        response = api_client.patch(endpoint_url)
        assert response.status_code == 200
        cargo.refresh_from_db()
        assert cargo.ativo is True

    def test_desativar(self,
                       db,
                       api_client,
                       usuario,
                       grupo_administradores,
                       grupo_colaboradores,
                       cargo):
        endpoint_url = reverse('cargo-desativar', args=[cargo.id])

        # Por Anônimo
        response = api_client.patch(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.patch(endpoint_url)
        assert response.status_code == 403
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.patch(endpoint_url)
        assert response.status_code == 200
        cargo.refresh_from_db()
        assert cargo.ativo is False


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

    def test_update(self,
                    db,
                    api_client,
                    usuario,
                    perfil,
                    outro_perfil,
                    grupo_administradores,
                    grupo_colaboradores,
                    departamento):
        endpoint_url = reverse('departamento-detail', args=[departamento.id])
        perfil_url = 'http://testserver' + reverse('perfil-detail',
                                                   args=[perfil.id])
        outro_perfil_url = 'http://testserver' + reverse('perfil-detail',
                                                         args=[outro_perfil.id])
        json_para_put = {
            'nome': 'Departamento Muito Bom',
            'diretor': outro_perfil_url,
            'diretor_substituto': perfil_url,
            'departamento_superior': None,
            'ativo': True
        }

        # Por Anônimo
        response = api_client.put(
            endpoint_url,
            data=json_para_put,
            format='json'
        )
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.put(
            endpoint_url,
            data=json_para_put,
            format='json'
        )
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.put(
            endpoint_url,
            data=json_para_put,
            format='json'
        )
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Departamento Muito Bom"
        assert json.loads(response.content)['diretor'] == outro_perfil_url
        assert json.loads(response.content)['diretor_substituto'] == perfil_url

    def test_partial_update(self,
                            db,
                            api_client,
                            usuario,
                            perfil,
                            outro_perfil,
                            grupo_administradores,
                            grupo_colaboradores,
                            departamento):
        endpoint_url = reverse('departamento-detail', args=[departamento.id])
        json_para_patch = {
            'nome': 'Departamento Excelente'
        }

        # Por Anônimo
        response = api_client.patch(
            endpoint_url,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.patch(
            endpoint_url,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.patch(
            endpoint_url,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Departamento Excelente"

    def test_ativar(self,
                    db,
                    api_client,
                    usuario,
                    grupo_administradores,
                    grupo_colaboradores,
                    departamento):
        endpoint_url = reverse('departamento-ativar', args=[departamento.id])

        # Por Anônimo
        response = api_client.patch(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.patch(endpoint_url)
        assert response.status_code == 403
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        departamento.ativo = False
        departamento.save()
        assert departamento.ativo is False
        response = api_client.patch(endpoint_url)
        assert response.status_code == 200
        departamento.refresh_from_db()
        assert departamento.ativo is True

    def test_desativar(self,
                       db,
                       api_client,
                       usuario,
                       grupo_administradores,
                       grupo_colaboradores,
                       departamento):
        endpoint_url = reverse('departamento-desativar', args=[departamento.id])

        # Por Anônimo
        response = api_client.patch(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.patch(endpoint_url)
        assert response.status_code == 403
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.patch(endpoint_url)
        assert response.status_code == 200
        departamento.refresh_from_db()
        assert departamento.ativo is False
