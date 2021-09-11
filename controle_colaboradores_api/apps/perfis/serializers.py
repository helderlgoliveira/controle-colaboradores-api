from rest_framework import serializers

from controle_colaboradores_api.apps.usuarios.serializers import CustomUsuarioSerializer
from controle_colaboradores_api.apps.localidades_brasileiras.serializers import MunicipioSerializer
from controle_colaboradores_api.apps.localidades_brasileiras.models import Municipio

from .models import \
    Perfil, \
    Endereco, \
    Telefone, \
    OutroEmail, \
    Cargo, \
    Departamento, \
    MunicipioOndeTrabalha


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


class MunicipioOndeTrabalhaSerializer(serializers.ModelSerializer):
    perfil = serializers.PrimaryKeyRelatedField(many=True, queryset=Perfil.objects.all())
    municipio = serializers.PrimaryKeyRelatedField(many=True, queryset=Municipio.objects.all())

    class Meta:
        model = MunicipioOndeTrabalha
        fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model:
            'perfil',
            'municipio'
        ]
        read_only_fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao'
        ]
        extra_kwargs = {
            'perfil': {'write_only': True}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['municipio'] = MunicipioSerializer(instance.municipio).data
        return data


class PerfilSerializer(serializers.ModelSerializer):
    usuario = CustomUsuarioSerializer()
    municipios_onde_trabalha = MunicipioOndeTrabalhaSerializer(many=True)
    enderecos = EnderecoSerializer(many=True)
    telefones = TelefoneSerializer(many=True)
    outros_emails = OutroEmailSerializer(many=True)

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
