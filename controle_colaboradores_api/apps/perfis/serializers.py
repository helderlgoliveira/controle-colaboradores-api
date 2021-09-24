from rest_framework import serializers

from controle_colaboradores_api.apps.usuarios.serializers import CustomUsuarioSerializer
from controle_colaboradores_api.apps.localidades_brasileiras.serializers import MunicipioSerializer

from .models import (
    Perfil,
    Endereco,
    Telefone,
    OutroEmail,
    Cargo,
    Departamento)


class EnderecoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Endereco
        fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model:
            'perfil',
            'is_principal',
            'logradouro',
            'numero',
            'bairro',
            'complemento',
            'municipio',
            'cep'
        ]
        read_only_fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao'
        ]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.filter(is_principal=True),
                fields=('perfil', 'is_principal'),
                message="Somente um endereço principal por perfil."
            )
        ]


class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model:
            'perfil',
            'numero',
        ]
        read_only_fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao'
        ]


class OutroEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutroEmail
        fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model:
            'perfil',
            'email',
        ]
        read_only_fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao'
        ]


class CargoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cargo
        fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model:
            'nome',
            'classe',
            'salario'
        ]
        read_only_fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao'
        ]

        def validate_salario(self, value):
            if not value > 0:
                raise serializers.ValidationError("Valor precisa ser maior que zero.")
            return value


class DepartamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Departamento
        fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model:
            'nome',
            'diretor',
            'diretor_substituto',
            'departamento_superior'
        ]
        read_only_fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao'
        ]


class PerfilSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['usuario'] = CustomUsuarioSerializer(instance.usuario).data
        data['cargos'] = CargoSerializer(instance.cargos.all(), many=True).data
        data['departamentos'] = DepartamentoSerializer(instance.departamentos.all(), many=True).data
        data['municipios_onde_trabalha'] = MunicipioSerializer(instance.municipios_onde_trabalha.all(), many=True).data
        data['enderecos'] = EnderecoSerializer(instance.enderecos.all(), many=True).data
        data['telefones'] = TelefoneSerializer(instance.telefones.all(), many=True).data
        data['outros_emails'] = OutroEmailSerializer(instance.outros_emails.all(), many=True).data
        return data

    class Meta:
        model = Perfil
        fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model BaseParaModelsImportantes:
            'ativo',
            'usuario_modificacao',
            # Fields do model:
            'usuario',
            'nome',
            'sobrenome',
            'cpf',
            'contrato_identificador',
            'data_admissao',
            'data_demissao',
            'dados_bancarios_banco',
            'dados_bancarios_agencia',
            'dados_bancarios_conta',
            'cargos',
            'departamentos',
            'municipios_onde_trabalha',
            # Fields de related_names:
            'enderecos',
            'telefones',
            'outros_emails'
        ]
        read_only_fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model BaseParaModelsImportantes:
            'usuario_modificacao',
        ]
