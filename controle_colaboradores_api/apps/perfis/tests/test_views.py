import json

import pytest
from django.contrib.auth.hashers import make_password
from model_bakery import baker
from pycpfcnpj import gen
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from controle_colaboradores_api.apps.perfis.models import (
    Perfil, Departamento, Cargo, OutroEmail, Telefone, Endereco
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
                      is_principal=True,
                      logradouro="Rua Um")


@pytest.fixture
def outro_endereco(outro_perfil):
    return baker.make('Endereco',
                      perfil=outro_perfil,
                      is_principal=True,
                      logradouro="Rua Dois")


class TestPerfilViewSet:

    def test_list(self,
                  db,
                  api_client,
                  usuario,
                  perfil,
                  grupo_administradores,
                  grupo_colaboradores):
        endpoint_url = reverse('perfil-list')

        # Por Anônimo
        response = api_client.get(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        # - sem nenhum cargo atrelado ao perfil
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url)
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 1
        assert results[0]['nome'] == "Fulano"

    def test_retrieve(self,
                      db,
                      api_client,
                      usuario,
                      perfil,
                      outro_perfil,
                      grupo_administradores,
                      grupo_colaboradores):
        endpoint_url_perfil_do_usuario = reverse('perfil-detail', args=[perfil.id])
        endpoint_url_perfil_do_outro_usuario = reverse('perfil-detail', args=[outro_perfil.id])

        # Por Anônimo
        response = api_client.get(endpoint_url_perfil_do_usuario)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        # - perfil do usuário
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url_perfil_do_usuario)
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Fulano"
        # - perfil de outro usuário
        response = api_client.get(endpoint_url_perfil_do_outro_usuario)
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url_perfil_do_outro_usuario)
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Beltrano"

    def test_create(self,
                    db,
                    api_client,
                    usuario,
                    outro_usuario,
                    perfil,
                    grupo_administradores,
                    grupo_colaboradores):
        endpoint_url = reverse('perfil-list')
        usuario_url = 'http://testserver' + reverse('customusuario-detail',
                                                    args=[usuario.id])
        outro_usuario_url = 'http://testserver' + reverse('customusuario-detail',
                                                          args=[outro_usuario.id])

        json_para_post = {
            "usuario": outro_usuario_url,
            "nome": "Cicrano",
            "sobrenome": "da Silva",
            "cpf": gen.cpf_with_punctuation(),
            "contrato_identificador": "abcd123",
            "data_admissao": "2021-10-09",
            "dados_bancarios_banco": "Banco Bom",
            "dados_bancarios_agencia": "Ag. 123",
            "dados_bancarios_conta": "CC 123123",
            "cargos": [],
            "municipios_onde_trabalha": [],
            "departamentos": [],
            "diretor_em": [],
            "diretor_substituto_em": [],
            "enderecos": [],
            "telefones": [],
            "outros_emails": []
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
        perfil_criado = Perfil.objects.last()
        perfil_criado_url = 'http://testserver' + \
                            reverse('perfil-detail',
                                    args=[perfil_criado.id])
        response_usuario_descricao = api_client.get(outro_usuario_url, format='json')
        usuario_descricao = json.loads(response_usuario_descricao.content)
        expected_json = {
            "url": perfil_criado_url,
            "id": perfil_criado.id,
            "criacao": perfil_criado.criacao.astimezone().isoformat(),
            "modificacao": perfil_criado.modificacao.astimezone().isoformat(),
            "ativo": perfil_criado.ativo,
            "usuario_modificacao": usuario_url,
            "usuario": usuario_descricao,
            "nome": perfil_criado.nome,
            "sobrenome": perfil_criado.sobrenome,
            "cpf": perfil_criado.cpf,
            "contrato_identificador": perfil_criado.contrato_identificador,
            "data_admissao": perfil_criado.data_admissao.isoformat(),
            "data_demissao": perfil_criado.data_demissao,
            "dados_bancarios_banco": perfil_criado.dados_bancarios_banco,
            "dados_bancarios_agencia": perfil_criado.dados_bancarios_agencia,
            "dados_bancarios_conta": perfil_criado.dados_bancarios_conta,
            "cargos": [],
            "municipios_onde_trabalha": [],
            "departamentos": [],
            "diretor_em": [],
            "diretor_substituto_em": [],
            "enderecos": [],
            "telefones": [],
            "outros_emails": []
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
                    grupo_colaboradores):
        endpoint_url_perfil_do_usuario = reverse('perfil-detail', args=[perfil.id])
        endpoint_url_perfil_do_outro_usuario = reverse('perfil-detail', args=[outro_perfil.id])
        usuario_url = 'http://testserver' + reverse('customusuario-detail',
                                                    args=[usuario.id])

        json_para_put = {
            "usuario": usuario_url,
            "nome": "Cicrano",
            "sobrenome": "da Silva",
            "cpf": gen.cpf_with_punctuation(),
            "contrato_identificador": "abcd123",
            "data_admissao": "2021-10-09",
            "dados_bancarios_banco": "Banco Bom",
            "dados_bancarios_agencia": "Ag. 123",
            "dados_bancarios_conta": "CC 123123",
            "cargos": [],
            "municipios_onde_trabalha": [],
            "departamentos": [],
            "diretor_em": [],
            "diretor_substituto_em": [],
            "enderecos": [],
            "telefones": [],
            "outros_emails": []
        }
        # Por Anônimo
        response = api_client.put(
            endpoint_url_perfil_do_usuario,
            data=json_para_put,
            format='json'
        )
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        # - update o próprio perfil:
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.put(
            endpoint_url_perfil_do_usuario,
            data=json_para_put,
            format='json'
        )
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Cicrano"
        # - update perfil de outro usuário:
        response = api_client.put(
            endpoint_url_perfil_do_outro_usuario,
            data=json_para_put,
            format='json'
        )
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        json_para_put['nome'] = "Fulano"
        response = api_client.put(
            endpoint_url_perfil_do_usuario,
            data=json_para_put,
            format='json'
        )
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Fulano"

    def test_partial_update(self,
                            db,
                            api_client,
                            usuario,
                            perfil,
                            outro_perfil,
                            grupo_administradores,
                            grupo_colaboradores):
        endpoint_url_perfil_do_usuario = reverse('perfil-detail', args=[perfil.id])
        endpoint_url_perfil_do_outro_usuario = reverse('perfil-detail', args=[outro_perfil.id])
        json_para_patch = {
            'sobrenome': 'dos Santos'
        }

        # Por Anônimo
        response = api_client.patch(
            endpoint_url_perfil_do_usuario,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        # - partial update do próprio perfil:
        response = api_client.patch(
            endpoint_url_perfil_do_usuario,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 200
        assert json.loads(response.content)['sobrenome'] == 'dos Santos'
        # - partial update do perfil de outro usuário:
        response = api_client.patch(
            endpoint_url_perfil_do_outro_usuario,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 403

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        json_para_patch['sobrenome'] = "Oliveira"
        response = api_client.patch(
            endpoint_url_perfil_do_usuario,
            data=json_para_patch,
            format='json'
        )
        assert response.status_code == 200
        assert json.loads(response.content)['sobrenome'] == 'Oliveira'


class TestEnderecoViewSet:
    # TODO Continuar daqui, copiar do OutroEmail/Telefone
    pass

    def test_list(self,
                  db,
                  api_client,
                  usuario,
                  outro_perfil,
                  endereco,
                  outro_endereco,
                  grupo_administradores,
                  grupo_colaboradores):
        endpoint_url = reverse('endereco-list')

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
        assert results[0]['logradouro'] == 'Rua Um'

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url)
        results = json.loads(response.content)['results']
        assert response.status_code == 200
        assert len(results) == 2
        assert results[1]['logradouro'] == 'Rua Dois'

    def test_retrieve(self,
                      db,
                      api_client,
                      usuario,
                      outro_perfil,
                      endereco,
                      outro_endereco,
                      grupo_administradores,
                      grupo_colaboradores):
        endpoint_url_endereco = reverse('endereco-detail', args=[endereco.id])
        endpoint_url_outro_endereco = reverse('endereco-detail', args=[outro_endereco.id])

        # Por Anônimo
        response = api_client.get(endpoint_url_endereco)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        # - consultando telefone do próprio usuário
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.get(endpoint_url_endereco)
        assert response.status_code == 200
        assert json.loads(response.content)['logradouro'] == "Rua Um"
        # - consultando telefone de outro usuário
        response = api_client.get(endpoint_url_outro_endereco)
        assert response.status_code == 404

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.get(endpoint_url_outro_endereco)
        assert response.status_code == 200
        assert json.loads(response.content)['logradouro'] == "Rua Dois"

    def test_create(self,
                    db,
                    api_client,
                    usuario,
                    perfil,
                    endereco,
                    grupo_administradores,
                    grupo_colaboradores):
        endpoint_url = reverse('endereco-list')
        perfil_url = 'http://testserver' + reverse('perfil-detail',
                                                   args=[perfil.id])
        municipio_url = 'http://testserver' + reverse('municipio-detail',
                                                      args=[endereco.municipio.id])
        json_para_post = {
            "perfil": perfil_url,
            "is_principal": False,
            "logradouro": "Rua Z",
            "numero": "25",
            "bairro": "Bairro Z",
            "municipio": municipio_url,
            "cep": "57000-000"
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
        endereco_criado = Endereco.objects.last()
        endereco_criado_url = 'http://testserver' + \
                              reverse('endereco-detail',
                                      args=[endereco_criado.id])
        expected_json = {
            'url': endereco_criado_url,
            'id': endereco_criado.id,
            'criacao': endereco_criado.criacao.astimezone().isoformat(),
            'modificacao': endereco_criado.modificacao.astimezone().isoformat(),
            'is_principal': False,
            'perfil': perfil_url,
            'logradouro': endereco_criado.logradouro,
            'numero': endereco_criado.numero,
            'bairro': endereco_criado.bairro,
            'complemento': endereco_criado.complemento,
            'municipio': municipio_url,
            'cep': endereco_criado.cep,
            'endereco_completo': endereco_criado.endereco_completo
        }
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        json_para_post['logradouro'] = "Rua A"
        response = api_client.post(
            endpoint_url,
            data=json_para_post,
            format='json'
        )
        endereco_criado = Endereco.objects.last()
        endereco_criado_url = 'http://testserver' + \
                              reverse('endereco-detail',
                                      args=[endereco_criado.id])
        expected_json = {
            'url': endereco_criado_url,
            'id': endereco_criado.id,
            'criacao': endereco_criado.criacao.astimezone().isoformat(),
            'modificacao': endereco_criado.modificacao.astimezone().isoformat(),
            'is_principal': False,
            'perfil': perfil_url,
            'logradouro': endereco_criado.logradouro,
            'numero': endereco_criado.numero,
            'bairro': endereco_criado.bairro,
            'complemento': endereco_criado.complemento,
            'municipio': municipio_url,
            'cep': endereco_criado.cep,
            'endereco_completo': endereco_criado.endereco_completo
        }
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

        json_para_post['is_principal'] = "True"
        response = api_client.post(
            endpoint_url,
            data=json_para_post,
            format='json'
        )
        expected_json = {
            'non_field_errors': ['Somente um endereço principal por perfil.']
        }
        assert response.status_code == 400
        assert json.loads(response.content) == expected_json

    def test_delete(self,
                    db,
                    api_client,
                    usuario,
                    grupo_administradores,
                    grupo_colaboradores,
                    endereco,
                    outro_endereco):
        endpoint_url = reverse('endereco-detail', args=[endereco.id])

        endpoint_url_outro_endereco = \
            reverse('endereco-detail', args=[outro_endereco.id])

        # Por Anônimo
        response = api_client.delete(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.delete(endpoint_url)
        assert response.status_code == 204
        response = api_client.delete(endpoint_url_outro_endereco)
        assert response.status_code == 404
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.delete(endpoint_url_outro_endereco)
        assert response.status_code == 204


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

    def test_create(self,
                    db,
                    api_client,
                    usuario,
                    perfil,
                    telefone,
                    grupo_administradores,
                    grupo_colaboradores):
        endpoint_url = reverse('telefone-list')
        perfil_url = 'http://testserver' + reverse('perfil-detail',
                                                   args=[perfil.id])
        json_para_post = {
            'perfil': perfil_url,
            'numero': '(33) 3333-3333'
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
        telefone_criado = Telefone.objects.last()
        telefone_criado_url = 'http://testserver' + \
                              reverse('telefone-detail',
                                      args=[telefone_criado.id])
        expected_json = {
            'url': telefone_criado_url,
            'id': telefone_criado.id,
            'criacao': telefone_criado.criacao.astimezone().isoformat(),
            'modificacao': telefone_criado.modificacao.astimezone().isoformat(),
            'perfil': perfil_url,
            'numero': telefone_criado.numero
        }
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        json_para_post['numero'] = "(77) 77777-7777"
        response = api_client.post(
            endpoint_url,
            data=json_para_post,
            format='json'
        )
        telefone_criado = Telefone.objects.last()
        telefone_criado_url = 'http://testserver' + \
                              reverse('telefone-detail',
                                      args=[telefone_criado.id])
        expected_json = {
            'url': telefone_criado_url,
            'id': telefone_criado.id,
            'criacao': telefone_criado.criacao.astimezone().isoformat(),
            'modificacao': telefone_criado.modificacao.astimezone().isoformat(),
            'perfil': perfil_url,
            'numero': telefone_criado.numero
        }
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_delete(self,
                    db,
                    api_client,
                    usuario,
                    grupo_administradores,
                    grupo_colaboradores,
                    telefone,
                    outro_telefone):
        endpoint_url = reverse('telefone-detail', args=[telefone.id])

        endpoint_url_outro_telefone = \
            reverse('telefone-detail', args=[outro_telefone.id])

        # Por Anônimo
        response = api_client.delete(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.delete(endpoint_url)
        assert response.status_code == 204
        response = api_client.delete(endpoint_url_outro_telefone)
        assert response.status_code == 404
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.delete(endpoint_url_outro_telefone)
        assert response.status_code == 204


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
                    outro_perfil,
                    grupo_administradores,
                    grupo_colaboradores,
                    outro_email):
        endpoint_url = reverse('outroemail-detail', args=[outro_email.id])

        email_de_outro_perfil = baker.make('OutroEmail', perfil=outro_perfil)
        endpoint_url_email_de_outro_perfil = reverse('outroemail-detail', args=[email_de_outro_perfil.id])

        # Por Anônimo
        response = api_client.delete(endpoint_url)
        assert response.status_code == 401

        # Por Usuário autenticado
        api_client.force_authenticate(user=usuario)
        # do grupo Colaboradores
        usuario.groups.set([grupo_colaboradores.id])
        response = api_client.delete(endpoint_url)
        assert response.status_code == 204
        response = api_client.delete(endpoint_url_email_de_outro_perfil)
        assert response.status_code == 404
        # do grupo Administradores
        usuario.groups.set([grupo_administradores.id])
        response = api_client.delete(endpoint_url_email_de_outro_perfil)
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
