import json

import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from controle_colaboradores_api.apps.localidades_brasileiras.serializers import (
    MunicipioSerializer,
    UnidadeFederativaSerializer
)


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


class TestMunicipioSerializer:

    def test_serialize_model(self, db, api_request_factory):
        municipio = baker.prepare('Municipio',
                                  nome="Bela Cidade")
        request = api_request_factory.get(reverse('municipio-list'))
        serializer = MunicipioSerializer(municipio,
                                         context={'request': request})
        assert serializer.data

    def test_serialized_data(self, db, api_request_factory):
        uf = baker.make('UnidadeFederativa')
        valid_serialized_data = baker.prepare('Municipio', nome="Bela Cidade").__dict__
        valid_serialized_data['uf'] = uf.id
        serializer = MunicipioSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}
