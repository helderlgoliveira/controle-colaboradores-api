from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password

from .models import CustomUsuario, PasswordResetToken


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = [
            'url',
            'id',
            'name'
        ]
        read_only_fields = [
            'id',
            'name'
        ]


class CustomUsuarioSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomUsuario
        fields = [
            'url',
            'id',
            'email',
            'password',
            'groups',
        ]
        read_only_fields = [
            'id',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        request = self.context['request']
        data = super().to_representation(instance)
        data['groups'] = GroupSerializer(instance.groups.all(),
                                         many=True,
                                         context={'request': request}).data
        return data

    def validate_password(self, value):
        validate_password(value)
        return value

    @transaction.atomic
    def create(self, validated_data):
        instance = CustomUsuario.objects.create_user(validated_data['email'],
                                                     validated_data['password'])
        groups = validated_data.pop('groups')
        instance.groups.set(groups)
        return instance


class CustomUsuarioMudarPasswordSerializer(serializers.ModelSerializer):
    nova_senha = serializers.CharField(min_length=8)

    def validate_password(self, value):
        senha_atual_confirmada = self.instance.check_password(value)
        if not senha_atual_confirmada:
            raise serializers.ValidationError("Senha atual incorreta.")
        return value

    def validate_nova_senha(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        nova_senha = validated_data.pop('nova_senha')
        instance.set_password(nova_senha)
        instance.save()
        return instance

    class Meta:
        model = CustomUsuario
        fields = [
            'id',
            'password',
            'nova_senha',
        ]
        read_only_fields = [
            'id'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'nova_senha': {'write_only': True}
        }


class CustomUsuarioMudarPasswordAposResetSerializer(serializers.ModelSerializer):
    nova_senha = serializers.CharField(min_length=8)

    def validate_nova_senha(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        nova_senha = validated_data['nova_senha']
        instance.set_password(nova_senha)
        instance.save()
        return instance

    class Meta:
        model = CustomUsuario
        fields = [
            'id',
            'nova_senha',
        ]
        read_only_fields = [
            'id'
        ]
        extra_kwargs = {
            'nova_senha': {'write_only': True}
        }


class CustomUsuarioMudarEmailSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.email(validated_data['email'])
        instance.save()
        return instance

    class Meta:
        model = CustomUsuario
        fields = [
            'id',
            'email',
        ]
        read_only_fields = [
            'id'
        ]


class CustomUsuarioMudarGrupoSerializer(serializers.ModelSerializer):

    def validate_groups(self, value):
        if value not in Group.objects.all():
            raise serializers.ValidationError("Grupo inexistente.")
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        groups = validated_data['groups']
        instance.groups.set(groups)
        instance.save()
        return instance

    class Meta:
        model = CustomUsuario
        fields = [
            'id',
            'groups',
        ]
        read_only_fields = [
            'id'
        ]
        extra_kwargs = {
            'groups': {'required': True}
        }


class CustomUsuarioMudarAtivacaoSerializer(serializers.ModelSerializer):

    @transaction.atomic
    def update(self, instance, validated_data):
        status_ativacao = validated_data['is_active']
        instance.is_active = status_ativacao
        instance.save()
        return instance

    class Meta:
        model = CustomUsuario
        fields = [
            'id',
            'is_active'
        ]
        read_only_fields = [
            'id'
        ]


class PasswordResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetToken
        fields = [
            'id',
            'criacao',
            'usuario',
            'token',
            'ativo'
        ]
        read_only_fields = [
            'id',
            'criacao',
            'token',
        ]

    def validate(self, data):
        if "token" in data:
            token_queryset = PasswordResetToken.objects.filter(usuario=data['usuario'], token=data['token'])
            token_existe = token_queryset.exists()
            if not token_existe:
                raise serializers.ValidationError("Token inválido.")
            token = token_queryset.get()
            if not token.ativo:
                raise serializers.ValidationError("Token inativo (já utilizado ou prazo expirou).")
            self.instance = token
        return data

    def to_representation(self, instance):
        request = self.context['request']
        data = super().to_representation(instance)
        data['usuario'] = CustomUsuarioSerializer(instance.usuario,
                                                  context={'request': request}).data
        return data

    def create(self, validated_data):
        tokens_ativos = PasswordResetToken.objects.filter(usuario=validated_data['usuario'],
                                                          ativo=True)
        token_pendente = [t for t in tokens_ativos if not t.expirado]
        if token_pendente:
            token = token_pendente[0]
            token.enviar_token_por_email()
            return token

        novo_token = PasswordResetToken.objects.create(usuario=validated_data['usuario'])
        return novo_token

    def update(self, instance, validated_data):
        instance.ativo = validated_data.get('ativo', instance.ativo)
        instance.save()
        return instance
