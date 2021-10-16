import json

import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


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
        municipio = baker.make('Municipio', nome="Nova Metrópole")

        response = api_client.get(
            reverse('municipio-detail', args=[municipio.id])
        )
        assert response.status_code == 200
        assert json.loads(response.content)['nome'] == "Nova Metrópole"
