import re

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


class EnderecoSerializer(serializers.HyperlinkedModelSerializer):

    def validate_cep(self, value):
        cep_pattern = re.compile(r"^\d{5}-\d{3}$")
        if not cep_pattern.match(value):
            raise serializers.ValidationError("CEP inválido. Informe no formato: 57000-000")
        return value

    class Meta:
        model = Endereco
        fields = [
            'url',
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


class TelefoneSerializer(serializers.HyperlinkedModelSerializer):

    def validate_numero(self, value):
        numero_pattern = re.compile(r"^\(\d{2}\)\s\d{4,5}-\d{4}$")
        if not numero_pattern.match(value):
            raise serializers.ValidationError("Número inválido. Informe no formato:"
                                              "(DD) 0000-0000 ou (DD) 90000-0000")
        return value

    class Meta:
        model = Telefone
        fields = [
            'url',
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


class OutroEmailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OutroEmail
        fields = [
            'url',
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


class CargoSerializer(serializers.HyperlinkedModelSerializer):

    def validate_salario(self, value):
        if not value > 0:
            raise serializers.ValidationError("Valor precisa ser maior que zero.")
        return value

    class Meta:
        model = Cargo
        fields = [
            'url',
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model BaseParaModelsImportantes:
            'ativo',
            'usuario_modificacao',
            # Fields do model:
            'nome',
            'classe',
            'salario'
        ]
        read_only_fields = [
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model BaseParaModelsImportantes:
            'usuario_modificacao'
        ]


class CargoMudarAtivacaoSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        status_ativacao = validated_data['ativo']
        instance.ativo = status_ativacao
        instance.save()
        return instance

    class Meta:
        model = Cargo
        fields = [
            'id',
            'ativo'
        ]
        read_only_fields = [
            'id'
        ]


class DepartamentoSerializer(serializers.HyperlinkedModelSerializer):

    def to_representation(self, instance):
        request = self.context['request']
        data = super().to_representation(instance)
        if data['departamento_superior']:
            data['departamento_superior'] = DepartamentoSerializer(instance.departamento_superior,
                                                                   context={'request': request}).data
        return data

    def validate(self, data):

        if 'departamento_superior' in data:
            if self.instance.id == data['departamento_superior'].id:
                raise serializers.ValidationError("O departamento superior não pode "
                                                  "ser o próprio departamento.")
        if 'diretor' in data:
            if data['diretor'] == self.instance.diretor_substituto:
                raise serializers.ValidationError("O diretor titular e o substituto não podem ser a mesma pessoa.")

        if 'diretor_substituto' in data:
            if data['diretor_substituto'] == self.instance.diretor:
                raise serializers.ValidationError("O diretor titular e o substituto não podem ser a mesma pessoa.")

        if all(k in data for k in ("diretor", "diretor_substituto")):
            if data['diretor'] == data['diretor_substituto']:
                raise serializers.ValidationError("O diretor titular e o substituto não podem ser a mesma pessoa.")

        return data

    class Meta:
        model = Departamento
        fields = [
            'url',
            # Fields do model Base:
            'id',
            'criacao',
            'modificacao',
            # Fields do model BaseParaModelsImportantes:
            'ativo',
            'usuario_modificacao',
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
            # Fields do model BaseParaModelsImportantes:
            'usuario_modificacao'
        ]


class DepartamentoMudarAtivacaoSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        status_ativacao = validated_data['ativo']
        instance.ativo = status_ativacao
        instance.save()
        return instance

    class Meta:
        model = Departamento
        fields = [
            'id',
            'ativo'
        ]
        read_only_fields = [
            'id'
        ]


class PerfilSerializer(serializers.HyperlinkedModelSerializer):

    def validate_cpf(self, value):
        cpf_pattern = re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
        if not cpf_pattern.match(value):
            raise serializers.ValidationError("CPF inválido. Informe no formato: 000.000.000-00")
        return value

    def to_representation(self, instance):
        request = self.context['request']
        data = super().to_representation(instance)
        data['usuario'] = CustomUsuarioSerializer(instance.usuario,
                                                  context={'request': request}).data
        data['usuario_modificacao'] = CustomUsuarioSerializer(instance.usuario_modificacao,
                                                              context={'request': request}).data
        data['cargos'] = CargoSerializer(instance.cargos.all(),
                                         many=True,
                                         context={'request': self.context['request']}).data
        data['departamentos'] = DepartamentoSerializer(instance.departamentos.all(),
                                                       many=True,
                                                       context={'request': request}).data
        data['diretor_em'] = DepartamentoSerializer(instance.diretor_em.all(),
                                                    many=True,
                                                    context={'request': request}).data
        data['diretor_substituto_em'] = DepartamentoSerializer(instance.diretor_substituto_em.all(),
                                                               many=True,
                                                               context={'request': request}).data
        data['municipios_onde_trabalha'] = MunicipioSerializer(instance.municipios_onde_trabalha.all(),
                                                               many=True,
                                                               context={'request': request}).data
        data['enderecos'] = EnderecoSerializer(instance.enderecos.all(),
                                               many=True,
                                               context={'request': request}).data
        data['telefones'] = TelefoneSerializer(instance.telefones.all(),
                                               many=True,
                                               context={'request': request}).data
        data['outros_emails'] = OutroEmailSerializer(instance.outros_emails.all(),
                                                     many=True,
                                                     context={'request': request}).data
        return data

    class Meta:
        model = Perfil
        fields = [
            'url',
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
            'municipios_onde_trabalha',
            'departamentos',
            # Fields de related_names:
            'diretor_em',
            'diretor_substituto_em',
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
