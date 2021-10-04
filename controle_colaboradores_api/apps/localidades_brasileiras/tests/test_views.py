import json

import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_forced_csrf():
    return APIClient(enforce_csrf_checks=True)

# TODO https://dev.to/sherlockcodes/pytest-with-django-rest-framework-from-zero-to-hero-8c4#:~:text=Now%2C%20let%27s%20proceed%20to%20test%20all%20endpoints%3A
#  https://www.django-rest-framework.org/api-guide/testing/#apiclient
#  https://stackoverflow.com/a/23091705 (test viewset)


class TestMunicipioViewSet:

    def test_list(self, db, api_client):
        baker.make('Municipio', _quantity=3)
        baker.make('Municipio', nome="Bela Cidade")

        response = api_client.get(
            reverse('municipio-list')
        )

        results = json.loads(response.content)['results']

        assert response.status_code == 200
        assert len(results) == 4
        assert results[3]['nome'] == "Bela Cidade"

    def test_retrieve(self, db, api_client):
        municipio = baker.make('Municipio', nome="Bela Cidade")

        response = api_client.get(
            reverse('municipio-detail', args=[municipio.id])
        )
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Bela Cidade"


    # def test_create(self, db, api_client):
    #     municipio = baker.prepare('Municipio')
    #     expected_json = {
    #         'nome': municipio.nome,
    #         'cod_ibge': municipio.cod_ibge,
    #         'uf': municipio.uf,
    #         'latitude': municipio.latitude,
    #         'longitude': municipio.longitude,
    #         'ddd': municipio.ddd,
    #         'fuso_horario': municipio.fuso_horario,
    #         'cod_siafi': municipio.cod_siafi,
    #     }
    #     response = api_client.post(
    #         reverse('municipio-create'),
    #         data=expected_json,
    #         format='json'
    #     )
    #
    #     assert response.status_code == 201
    #     assert json.loads(response.content) == expected_json



