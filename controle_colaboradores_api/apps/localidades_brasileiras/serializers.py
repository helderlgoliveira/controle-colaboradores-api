from rest_framework import serializers

from .models import UnidadeFederativa, Municipio


class UnidadeFederativaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnidadeFederativa
        fields = [
            'id',
            'nome',
            'sigla',
            'cod_ibge',
            'latitude',
            'longitude',
            'capital'
        ]
        read_only_fields = [
            'id'
        ]


class MunicipioSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        request = self.context['request']
        data = super().to_representation(instance)
        data['uf'] = UnidadeFederativaSerializer(instance.uf,
                                                 context={'request': request}).data
        return data

    class Meta:
        model = Municipio
        fields = [
            'url',
            'id',
            'nome',
            'cod_ibge',
            'uf',
            'latitude',
            'longitude',
            'ddd',
            'fuso_horario',
            'cod_siafi'
        ]
        read_only_fields = [
            'id'
        ]
